"""Offline teaching controller. No network, credentials, writes, or LLM runtime."""
from dataclasses import dataclass, field
from time import monotonic
from math import isfinite
from typing import Callable, Protocol


class RateLimited(Exception):
    pass


class InvalidToolArguments(ValueError):
    pass


@dataclass(frozen=True)
class Claim:
    source: str
    section: str
    topic: str
    value: str


class Adapter(Protocol):
    """A real API adapter must enforce its own transport timeout and token cap."""
    def plan(self, question: str) -> dict: ...
    def compose(self, claims: list[Claim]) -> dict: ...


@dataclass
class Result:
    status: str
    reason: str
    answer: str = ''
    citations: list[str] = field(default_factory=list)
    trace: list[dict] = field(default_factory=list)
    mode: str = 'offline simulation; not a model test'
    usage: str = 'No model tokens or API charges; simulated work only'


class ReadOnlySearch:
    """Structured, pre-reviewed toy corpus; free text is never an instruction."""
    schema = {'name': 'search_sources', 'required': ['topic', 'source_ids'],
              'additionalProperties': False,
              'topic': 'string, 1..80 characters',
              'source_ids': 'nonempty unique list of allowed document IDs'}

    def __init__(self, documents):
        self.documents = documents
        self.calls = 0

    def search(self, arguments):
        if not isinstance(arguments, dict) or set(arguments) != {'topic', 'source_ids'}:
            raise InvalidToolArguments('exactly topic and source_ids required')
        topic, ids = arguments['topic'], arguments['source_ids']
        if not isinstance(topic, str) or not 1 <= len(topic) <= 80:
            raise InvalidToolArguments('invalid topic')
        if (not isinstance(ids, list) or not ids or
            any(not isinstance(x, str) or x not in self.documents for x in ids) or
            len(set(ids)) != len(ids)):
            raise InvalidToolArguments('invalid source allowlist')
        self.calls += 1
        claims = []
        for sid in ids:
            # Only reviewed facts participate. Untrusted body text is not parsed as code,
            # prompts, tool calls, or policy. This is NOT a general injection detector.
            for fact in self.documents[sid]['facts']:
                if fact['topic'] == topic:
                    claims.append(Claim(sid, fact['section'], topic, fact['value']))
        return claims


def run(question: str, adapter: Adapter, tool: ReadOnlySearch,
        approve: Callable[[dict], bool], *, approve_release=None, max_steps=8, max_retries=1,
        deadline_seconds=2.0, clock=monotonic) -> Result:
    """Finite controller; transient errors retry at most max_retries per operation.

    Deadline checks are cooperative, NOT a thread/process cancellation mechanism.
    A production adapter must independently enforce a transport deadline.
    """
    if (not isinstance(question, str) or not question.strip() or len(question) > 500
        or type(max_steps) is not int or not 1 <= max_steps <= 32
        or type(max_retries) is not int or not 0 <= max_retries <= 2
        or type(deadline_seconds) not in (int, float)
        or not 0 < deadline_seconds <= 30 or not isfinite(deadline_seconds)):
        return Result('refused', 'invalid_input_or_budget')
    start = clock()
    trace = []

    def stop(status, reason, answer='', citations=None):
        return Result(status, reason, answer, citations or [], trace)

    def step(name, call, retry=True, human_wait=False):
        nonlocal start
        retries = max_retries if retry else 0
        for attempt in range(retries + 1):
            elapsed = clock() - start
            if len(trace) >= max_steps:
                raise RuntimeError('step_budget')
            if elapsed >= deadline_seconds:
                raise RuntimeError('deadline')
            entry = {'state': name, 'attempt': attempt + 1, 'elapsed_ms': round(elapsed * 1000), 'status': 'started'}
            trace.append(entry)
            try:
                call_start = clock()
                value = call()
                call_end = clock()
                if human_wait:
                    start += call_end - call_start
                if call_end - start >= deadline_seconds:
                    entry['status'] = 'deadline'
                    raise RuntimeError('deadline')
                entry['status'] = 'ok'
                return value
            except (TimeoutError, RateLimited) as error:
                entry['status'] = 'timeout' if isinstance(error, TimeoutError) else 'rate_limit'
                if attempt == retries:
                    raise RuntimeError(entry['status']) from None
        raise AssertionError('unreachable')

    try:
        plan = step('plan', lambda: adapter.plan(question))
        if not isinstance(plan, dict) or set(plan) != {'tool', 'arguments'} or plan['tool'] != 'search_sources':
            return stop('refused', 'invalid_tool')
        # Approval is explicit and happens before any source access. Never retry it.
        approved = step('human_review', lambda: approve(plan) is True, retry=False, human_wait=True)
        if not approved:
            return stop('refused', 'human_denied')
        claims = step('read_only_search', lambda: tool.search(plan['arguments']))
        if not claims:
            return stop('refused', 'no_evidence')
        # Freeze host-owned evidence BEFORE invoking an adapter. Frozen dataclasses
        # alone do not make a list or nested values immutable. This toy schema
        # accepts only plain nonempty strings, never mutable nested claim values.
        if any(not isinstance(c, Claim) or any(type(v) is not str or not v
               for v in (c.source, c.section, c.topic, c.value)) for c in claims):
            return stop('refused', 'invalid_evidence')
        evidence = tuple((c.source, c.section, c.topic, c.value) for c in claims)
        expected_answer = evidence[0][3]
        allowed = frozenset(f'{source}#{section}' for source, section, _, _ in evidence)
        if len({value for _, _, _, value in evidence}) > 1:
            return stop('needs_review', 'conflicting_sources',
                        citations=[f'{source}#{section}' for source, section, _, _ in evidence])
        # A fresh list AND fresh Claim objects on every retry: adapter mutation
        # cannot rewrite validation evidence or contaminate the next attempt.
        draft = step('compose', lambda: adapter.compose([Claim(*row) for row in evidence]))
        # Exact supported fact only; not a general factuality guarantee.
        if (not isinstance(draft, dict) or set(draft) != {'answer', 'citations'} or
            type(draft['answer']) is not str or draft['answer'] != expected_answer or
            not isinstance(draft['citations'], list) or not draft['citations'] or
            any(type(c) is not str or c not in allowed for c in draft['citations'])):
            return stop('refused', 'unsupported_answer_or_citation')
        if approve_release is None:
            return stop('needs_review', 'release_review_required')
        # Detach validated output from adapter-owned lists before human review.
        answer, citations = draft['answer'], tuple(draft['citations'])
        candidate = {'answer': answer, 'citations': list(citations)}
        released = step('human_release_review', lambda: approve_release(candidate) is True,
                        retry=False, human_wait=True)
        if not released:
            return stop('refused', 'human_release_denied')
        return stop('answered', 'supported_exact_fact', answer, list(citations))
    except InvalidToolArguments:
        return stop('refused', 'invalid_tool_arguments')
    except RuntimeError as error:
        reason = str(error) if str(error) in {'step_budget', 'deadline', 'timeout', 'rate_limit'} else 'adapter_error'
        return stop('stopped', reason)
    except Exception:
        # Do not expose exceptions containing prompts, keys, or document contents.
        return stop('stopped', 'adapter_error')

"""Offline simulation contracts; these are not model-quality tests."""
import copy
import importlib.util
from pathlib import Path
import sys
import unittest

LAB = Path(__file__).resolve().parents[1] / 'learning' / 'qa-agent'
# Load with unique names to avoid changing global sys.path or shadowing other tests.
def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, LAB / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

core = load('ma_qa_core', 'core.py')
# adapters imports core when executed directly; temporarily expose it for loading.
previous = sys.modules.get('core')
sys.modules['core'] = core
adapters = load('ma_qa_adapters', 'adapters.py')
if previous is not None:
    sys.modules['core'] = previous
else:
    del sys.modules['core']

class AgentLabTests(unittest.TestCase):
    def execute(self, question='retention?', adapter=None, documents=None, approve=lambda p: True, approve_release=lambda p: True, **kwargs):
        return core.run(question, adapter or adapters.FakeAdapter(), core.ReadOnlySearch(documents or adapters.DOCUMENTS), approve, approve_release=approve_release, **kwargs)

    def test_success_and_citations(self):
        result = self.execute()
        self.assertEqual(result.status, 'answered')
        self.assertEqual(result.answer, '30 days / 30 天')
        self.assertEqual(result.citations, ['handbook#retention', 'policy#retention'])
        self.assertEqual([x['state'] for x in result.trace], ['plan', 'human_review', 'read_only_search', 'compose', 'human_release_review'])

    def test_chinese_question(self):
        self.assertEqual(self.execute('保留多久').status, 'answered')

    def test_no_evidence(self):
        self.assertEqual(self.execute('Who won an election?').reason, 'no_evidence')

    def test_conflict(self):
        docs = copy.deepcopy(adapters.DOCUMENTS)
        docs['policy']['facts'][0]['value'] = '90 days'
        result = self.execute(documents=docs)
        self.assertEqual(result.reason, 'conflicting_sources')
        self.assertEqual(result.answer, '')
        self.assertEqual(len(result.citations), 2)

    def test_timeout_bounded(self):
        adapter = adapters.FakeAdapter(['timeout'] * 10)
        self.assertEqual(self.execute(adapter=adapter).reason, 'timeout')
        self.assertEqual(adapter.plan_calls, 2)

    def test_rate_limit_bounded(self):
        adapter = adapters.FakeAdapter(['rate_limit'] * 10)
        self.assertEqual(self.execute(adapter=adapter).reason, 'rate_limit')
        self.assertEqual(adapter.plan_calls, 2)

    def test_transient_recovery(self):
        self.assertEqual(self.execute(adapter=adapters.FakeAdapter(['rate_limit'])).status, 'answered')

    def test_invalid_arguments(self):
        class Bad(adapters.FakeAdapter):
            def plan(self, question):
                return {'tool': 'search_sources', 'arguments': {'topic': 'retention', 'source_ids': ['../../secret']}}
        self.assertEqual(self.execute(adapter=Bad()).reason, 'invalid_tool_arguments')

    def test_schema_rejects_extra_and_wrong_types(self):
        tool = core.ReadOnlySearch(adapters.DOCUMENTS)
        for args in [{}, {'topic': 'retention', 'source_ids': ['handbook'], 'write': True},
                     {'topic': 3, 'source_ids': ['handbook']}, {'topic': 'x', 'source_ids': [None]},
                     {'topic': 'x', 'source_ids': ['handbook', 'handbook']}]:
            with self.assertRaises(core.InvalidToolArguments):
                tool.search(args)
        self.assertEqual(tool.calls, 0)

    def test_injection_is_not_executed(self):
        result = self.execute('Who is the owner?')
        self.assertEqual(result.answer, 'Research team / 研究团队')
        self.assertEqual(result.citations, ['notes#owner'])
        self.assertNotIn('attacker', str(result))

    def test_human_denied_before_read(self):
        tool = core.ReadOnlySearch(adapters.DOCUMENTS)
        result = core.run('retention', adapters.FakeAdapter(), tool, lambda p: False)
        self.assertEqual(result.reason, 'human_denied')
        self.assertEqual(tool.calls, 0)

    def test_truthy_value_is_not_approval(self):
        self.assertEqual(self.execute(approve=lambda p: 'yes').reason, 'human_denied')

    def test_step_budget(self):
        self.assertEqual(self.execute(max_steps=2).reason, 'step_budget')

    def test_deadline(self):
        values = iter([0, 0, 0, 3])
        self.assertEqual(self.execute(clock=lambda: next(values), deadline_seconds=2).reason, 'deadline')

    def test_human_wait_does_not_consume_execution_deadline(self):
        now = [0.0]
        def approve(plan):
            now[0] += 60
            return True
        self.assertEqual(self.execute(approve=approve, clock=lambda: now[0]).status, 'answered')

    def test_human_gate_never_retries(self):
        calls = []
        def approve(plan):
            calls.append(plan)
            raise TimeoutError('approval timeout')
        self.assertEqual(self.execute(approve=approve).reason, 'timeout')
        self.assertEqual(len(calls), 1)

    def test_final_release_denied(self):
        seen = []
        def review(candidate):
            seen.append(candidate)
            return False
        result = self.execute(approve_release=review)
        self.assertEqual(result.reason, 'human_release_denied')
        self.assertEqual(result.answer, '')
        self.assertEqual(seen[0]['answer'], '30 days / 30 天')
        self.assertEqual(seen[0]['citations'], ['handbook#retention', 'policy#retention'])

    def test_no_release_callback_fails_closed(self):
        result = self.execute(approve_release=None)
        self.assertEqual(result.reason, 'release_review_required')
        self.assertEqual(result.answer, '')

    def test_final_release_strict_boolean(self):
        self.assertEqual(self.execute(approve_release=lambda p: 'yes').reason, 'human_release_denied')

    def test_final_release_never_retries(self):
        calls = []
        def review(candidate):
            calls.append(candidate)
            raise TimeoutError('review timeout')
        self.assertEqual(self.execute(approve_release=review).reason, 'timeout')
        self.assertEqual(len(calls), 1)

    def test_final_release_wait_excluded(self):
        now = [0.0]
        def review(candidate):
            now[0] += 60
            return True
        self.assertEqual(self.execute(approve_release=review, clock=lambda: now[0]).status, 'answered')

    def test_invalid_budget(self):
        self.assertEqual(self.execute(max_retries=100).reason, 'invalid_input_or_budget')

    def test_deadline_type_and_finiteness_fail_closed(self):
        for value in [None, '2', True, False, float('nan'), float('inf'),
                      float('-inf'), 0, -1, 31, 10**1000]:
            with self.subTest(value=repr(value)):
                self.assertEqual(self.execute(deadline_seconds=value).reason, 'invalid_input_or_budget')
        for value in [1, 0.5, 30]:
            self.assertEqual(self.execute(deadline_seconds=value).status, 'answered')

    def test_unsupported_citation(self):
        class Bad(adapters.FakeAdapter):
            def compose(self, claims):
                return {'answer': claims[0].value, 'citations': ['invented#1']}
        self.assertEqual(self.execute(adapter=Bad()).reason, 'unsupported_answer_or_citation')

    def test_unsupported_answer(self):
        class Bad(adapters.FakeAdapter):
            def compose(self, claims):
                return {'answer': 'forever', 'citations': ['handbook#retention']}
        self.assertEqual(self.execute(adapter=Bad()).reason, 'unsupported_answer_or_citation')

    def test_compose_cannot_replace_evidence_list(self):
        class Mutating(adapters.FakeAdapter):
            def compose(self, claims):
                claims[:] = [core.Claim('invented', 'fake', 'retention', 'forever')]
                return {'answer': 'forever', 'citations': ['invented#fake']}
        result = self.execute(adapter=Mutating())
        self.assertEqual(result.reason, 'unsupported_answer_or_citation')
        self.assertEqual(result.answer, '')

    def test_compose_claim_objects_are_not_validation_objects(self):
        class Mutating(adapters.FakeAdapter):
            def compose(self, claims):
                # Even bypassing frozen dataclass assignment affects only a copy.
                object.__setattr__(claims[0], 'value', 'forever')
                object.__setattr__(claims[0], 'source', 'invented')
                return {'answer': 'forever', 'citations': ['invented#retention']}
        self.assertEqual(self.execute(adapter=Mutating()).reason, 'unsupported_answer_or_citation')

    def test_nested_mutable_evidence_rejected_before_compose(self):
        for value in [{'value': '30 days'}, ['30 days']]:
            docs = copy.deepcopy(adapters.DOCUMENTS)
            docs['handbook']['facts'][0]['value'] = value
            class NeverCompose(adapters.FakeAdapter):
                def compose(self, claims):
                    raise AssertionError('mutable nested evidence reached adapter')
            self.assertEqual(self.execute(adapter=NeverCompose(), documents=docs).reason, 'invalid_evidence')

    def test_mutating_document_source_during_compose_cannot_change_snapshot(self):
        docs = copy.deepcopy(adapters.DOCUMENTS)
        class Mutating(adapters.FakeAdapter):
            def compose(self, claims):
                docs['handbook']['facts'][0]['value'] = 'forever'
                docs['policy']['facts'][0]['value'] = 'forever'
                return {'answer': 'forever', 'citations': ['handbook#retention']}
        self.assertEqual(self.execute(adapter=Mutating(), documents=docs).reason, 'unsupported_answer_or_citation')

    def test_compose_retry_receives_fresh_evidence(self):
        class Retry(adapters.FakeAdapter):
            count = 0
            def compose(self, claims):
                self.count += 1
                if self.count == 1:
                    object.__setattr__(claims[0], 'value', 'forever')
                    claims.clear()
                    raise TimeoutError('simulated transient')
                return super().compose(claims)
        result = self.execute(adapter=Retry())
        self.assertEqual(result.status, 'answered')
        self.assertEqual(result.answer, '30 days / 30 天')

    def test_review_mutations_cannot_change_validated_output(self):
        class Retaining(adapters.FakeAdapter):
            def compose(self, claims):
                self.draft = super().compose(claims)
                return self.draft
        adapter = Retaining()
        def review(candidate):
            candidate['answer'] = 'forever'
            candidate['citations'].append('review-invented#fake')
            adapter.draft['answer'] = 'forever'
            adapter.draft['citations'][:] = ['adapter-invented#fake']
            return True
        result = self.execute(adapter=adapter, approve_release=review)
        self.assertEqual(result.status, 'answered')
        self.assertEqual(result.answer, '30 days / 30 天')
        self.assertEqual(result.citations, ['handbook#retention', 'policy#retention'])

    def test_log_does_not_record_question(self):
        result = self.execute('private-marker retention')
        self.assertNotIn('private-marker', str(result.trace))

    def test_unknown_tool_denied(self):
        class Bad(adapters.FakeAdapter):
            def plan(self, question):
                return {'tool': 'send_email', 'arguments': {}}
        self.assertEqual(self.execute(adapter=Bad()).reason, 'invalid_tool')

if __name__ == '__main__':
    unittest.main()

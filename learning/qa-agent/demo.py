"""Run from any directory: python learning/qa-agent/demo.py"""
import argparse
import json
from dataclasses import asdict
from adapters import DOCUMENTS, FakeAdapter
from core import ReadOnlySearch, run

parser = argparse.ArgumentParser(description='Offline QA Agent simulation / 离线资料问答模拟')
parser.add_argument('--question', default='How long is retention? / 保留多久？')
args = parser.parse_args()

def approval(plan):
    print('Read-only access plan / 只读访问计划:', json.dumps(plan, ensure_ascii=False))
    try:
        return input('Approve these synthetic sources? Type yes / 同意读取合成资料请输入 yes: ').strip() == 'yes'
    except EOFError:
        return False

def release_approval(candidate):
    print('Candidate answer and citations / 候选答案及引用:', json.dumps(candidate, ensure_ascii=False))
    try:
        return input('Release this answer? Type yes / 审核后同意发布此答案请输入 yes: ').strip() == 'yes'
    except EOFError:
        return False

print(json.dumps(asdict(run(args.question, FakeAdapter(), ReadOnlySearch(DOCUMENTS), approval,
                           approve_release=release_approval)), ensure_ascii=False, indent=2))

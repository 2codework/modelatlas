"""Run original fixtures; all outputs are algebra, not model predictions."""
import json
import argparse
from pathlib import Path
from core import calculate
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Original noise algebra; no model execution.')
    parser.add_argument('--include-transfer', action='store_true', help='Reveal T only after an independent attempt')
    args = parser.parse_args()
    fixtures = json.loads(Path(__file__).with_name('fixtures.json').read_text())
    if not args.include_transfer:
        fixtures.pop('transfer')
    print(json.dumps({key: calculate(**value) for key,value in fixtures.items()}, indent=2, allow_nan=False))

# Contributing to Zwonk

## Setup

```bash
git clone https://github.com/thezwonk/Zwonk.git
cd Zwonk
pip install -e ".[dev]"
pytest tests/ -v
```

## Commit Style

```
feat(module): description
fix(module): description
test(module): add test description
docs: description
chore: maintenance
```

## Adding a Signal

1. Add function to `zwonk/signals.py`
2. Register in `run_all_signals()`
3. Rebalance weights to sum to 1.0
4. Add minimum 5 tests in `tests/test_signals.py`
5. Update TypeScript types in `dashboard/src/types.ts`

## Rules

- No external dependencies in core
- All tests must pass before PR
- Keep the engine pure Python 3.10+

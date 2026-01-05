## Failure Rules

- Evaluator crash → BLOCK
- Invalid evaluator return → BLOCK
- Engine exception → BLOCK
- Missing fields → BLOCK
- No enforcement path may end without a decision

BLOCK is always safer than EXECUTE.

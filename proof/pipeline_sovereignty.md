# Pipeline Sovereignty Proof

## Rule
All assistant outputs must pass through enforcement_gateway.py.
No component may execute or respond directly.

## Verified Flow
User → Sankalp → enforcement_gateway → enforcement_engine → decision → Sankalp → User

## Bypass Prevention
- Sankalp cannot call enforcement_engine directly
- Backend routes only to enforcement_gateway
- UI has no execution authority

## Failure Case
If enforcement_gateway is unavailable:
- No output is produced
- Execution fails closed

## Execution Lock

- execution_gateway.py has been deleted
- All assistant outputs flow through enforcement_gateway.py
- Direct calls to enforcement_engine are forbidden at runtime
- Bypass attempts fail closed

## Conclusion
The enforcement gateway is sovereign and non-bypassable.

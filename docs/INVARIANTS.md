# Formal Safety Invariants

This document defines the formal safety properties enforced by the negotiation agent.

---

## Overview

The system enforces three core invariants derived from a TLA+ specification:

1. **INV_S1**: Unauthorized Commit Prevention
2. **INV_S2**: Monotonic Concessions
3. **INV_S3**: Terminal State Absorption

These are **runtime-enforced**, not just documentation.

---

## INV_S1: Unauthorized Commit Prevention

### Formal Statement

```
A negotiation may only transition to COMMIT if:
  (approval_valid = TRUE) OR (emergency_override = TRUE)
```

### TLA+ Specification

```tla
TypeInvariant ==
  /\ state = "COMMIT" => (approval_valid \/ emergency_override)
```

### Runtime Enforcement

See [engine/invariants.py](../engine/invariants.py):

```python
def check_unauthorized_commit(approval_valid, emergency_override, next_state):
    if next_state == NegotiationState.COMMIT:
        if not (approval_valid or emergency_override):
            raise InvariantViolation("INV_S1", "Cannot COMMIT without authorization")
```

### Why This Matters

Prevents autonomous execution. No contract can be finalized without explicit human approval or documented emergency override.

---

## INV_S2: Monotonic Concessions

### Formal Statement

```
Concessions must move in institution-favorable directions:
  - Unit price: new_price <= old_price (buyer favorable)
  - Volume: new_volume >= old_volume (seller favorable)
```

### TLA+ Specification

```tla
MonotonicConcessions ==
  /\ new_price <= old_price
  /\ new_volume >= old_volume
```

### Runtime Enforcement

See [engine/invariants.py](../engine/invariants.py):

```python
def check_monotonicity(old_terms, new_terms):
    if new_terms['unit_price'] > old_terms['unit_price']:
        raise InvariantViolation("INV_S2", "Concession reversal: Price cannot increase")
```

### Why This Matters

Prevents the LLM or vendor from reversing previously agreed concessions. Ensures negotiations only move in institution-favorable directions.

---

## INV_S3: Terminal State Absorption

### Formal Statement

```
Once a negotiation reaches COMMIT or ABORT, it cannot transition to any other state:
  state ∈ {COMMIT, ABORT} => state' = state
```

### TLA+ Specification

```tla
TerminalAbsorption ==
  /\ state \in {"COMMIT", "ABORT"} => state' = state
```

### Runtime Enforcement

See [engine/state_machine.py](../engine/state_machine.py):

```python
def transition(current_state, next_state):
    if current_state in TERMINAL_STATES:
        raise InvalidTransitionError("Cannot transition out of terminal state")
```

### Why This Matters

Ensures finality. Once committed or aborted, the negotiation cannot be modified or re-processed. Critical for audit integrity.

---

## Testing

All invariants are verified using property-based testing with Hypothesis.

See [tests/test_invariants.py](../tests/test_invariants.py) for examples.

### Example Test

```python
@given(states=state_sequence())
def test_terminal_states_are_absorbing(states):
    """Verifies INV_S3 under fuzzing."""
    for i in range(len(states) - 1):
        if states[i] in TERMINAL_STATES:
            with pytest.raises(InvalidTransitionError):
                transition(states[i], states[i + 1])
```

---

## Audit Traceability

Each invariant violation is logged with:
- Invariant ID (e.g., "INV_S1")
- Timestamp
- Negotiation context
- Violation details

This provides forensic evidence for compliance audits.

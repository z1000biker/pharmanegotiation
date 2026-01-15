# Contribution Guidelines

This repository demonstrates safety-critical patterns for regulated procurement.

## Core Principle: Safety First

Pull requests that introduce:
- Implicit state transitions
- Non-deterministic behavior
- Hidden authority
- Prompt-based enforcement (instead of invariant-based)

**will be rejected.**

## How to Contribute

1. **Preserve Invariants**: All changes must preserve or strengthen the explicit invariants defined in [INVARIANTS.md](docs/INVARIANTS.md).
2. **Deterministic Only**: No "magical" AI decisions. Every state change must be traceable and verifiable.
3. **Audit Integrity**: Do not modify hash chaining or log structures in a way that breaks non-repudiation.
4. **Testing**: Property-based tests (Hypothesis) are required for any new state logic.

This repository is maintained with the rigor of a safety-critical system. We welcome contributions that improve defensibility, durability, and formal verification coverage.

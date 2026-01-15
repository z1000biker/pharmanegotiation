# Runtime vs. Audit Replay Semantics

## Overview

The system distinguishes between **Live Negotiation (Runtime)** and **Historical Reconstruction (Audit Replay)**. This separation is critical for long-term auditability in regulated environments.

## The Problem: Temporal Validity

Negotiations often rely on time-bound artifacts:
- Approval tokens that expire after 24 hours.
- Replay windows for idempotency keys.
- NTP-synchronized clock drift checks.

If a vendor disputes a 2-year-old negotiation, a naive replay would fail these checks, making the audit trail useless for forensics.

## The Solution: Dual-Mode Execution

### 1. Runtime Mode (Strict Validation)
Used during active negotiations. Enforces all temporal and security constraints.
- **Approval tokens** must be current (not expired).
- **Idempotency keys** must be within the active window.
- **Sequence numbers** must be strictly increasing.

### 2. Audit Replay Mode (Forensic Validation)
Used by auditors to reconstruct the state from a signed log. 
- **Skips temporal checks**: Expiration of tokens is ignored (they were valid at the time).
- **Enforces cryptographic integrity**: Hashes and signatures are still verified.
- **Verifies Invariants**: Formal safety properties (like monotonicity) must still hold.

## Deterministic Guarantee

The system guarantees that:
```
State(Log) @ Runtime == State(Log) @ AuditReplay
```

This ensures that the "truth" recorded in the log is exactly what was executed, regardless of when it is reviewed.

## Audit Workflow

1. **Extraction**: Retrieve the Merklized audit log for the disputed negotiation.
2. **Reconstruction**: Run the system in `AUDIT_REPLAY` mode using the log as input.
3. **Verification**: Confirm that each transition hash matches the log and that the final state matches the committed terms.
4. **Validation**: Provide the cryptographically verified reconstruction to the auditor or legal team.

---

**Author**: Nik. Kontopoulos  
**Status**: Reference Implementation v1.0

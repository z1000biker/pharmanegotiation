# Threat Model

This document outlines the security threats considered in the system design and their mitigations.

---

## Threat Categories

1. **Replay Attacks**
2. **Duplicate Message Processing**
3. **Stale Approval Tokens**
4. **Forged Messages**
5. **Crash Recovery**

---

## T1: Replay Attacks

### Threat

An attacker intercepts a legitimate message and replays it later to:
- Duplicate a COMMIT transaction
- Re-execute a favorable negotiation round

### Mitigation

**Idempotency Keys**: Each transition has a deterministic ID based on:
```
transition_id = SHA256(negotiation_id : state : round : event)
```

**Enforcement**: Before executing a transition, check if `transition_id` has already been applied.

**Result**: Replaying the same transition is a no-op (idempotent).

---

## T2: Duplicate Message Processing

### Threat

Network retries or malicious actors send duplicate messages, causing:
- Multiple state transitions
- Inconsistent audit logs

### Mitigation

**Message Deduplication**: Track processed message hashes.

**Enforcement**: Reject messages with duplicate content hashes.

---

## T3: Stale Approval Tokens

### Threat

An approval token issued for old terms is used to approve modified terms.

### Mitigation

**Time-Bound Tokens**: Tokens expire after 24 hours (configurable).

**Term Binding**: Tokens include a hash of the exact terms being approved:
```
token.terms_hash = SHA256(json.dumps(terms, sort_keys=True))
```

**Enforcement**: Validate token expiry and term binding before COMMIT.

---

## T4: Forged Messages

### Threat

An attacker forges a vendor message with favorable terms.

### Mitigation

**Cryptographic Signatures**: All A2A messages are signed with HMAC-SHA256 (production uses Ed25519).

**Public Key Registry**: Sender identities are verified against a registry.

**Enforcement**: Reject messages with invalid signatures.

---

## T5: Crash Recovery

### Threat

System crashes mid-transaction, leaving negotiation in inconsistent state.

### Mitigation

**Write-Ahead Log (WAL)**: All transitions are logged before execution.

**Hash Chain Verification**: On recovery, verify WAL integrity via hash chain.

**Idempotent Replay**: Replay WAL events; duplicate transitions are no-ops.

**Enforcement**: System refuses to start if WAL integrity check fails.

---

## Runtime vs Audit Replay

### Threat

Historical messages fail validation during audit reconstruction due to:
- Expired tokens
- Replay window restrictions

### Mitigation

**Dual-Mode Execution**:
- **Runtime Mode**: Strict validation (replay window, token expiry)
- **Audit Replay Mode**: Relaxed validation (skip time-based checks)

**Enforcement**: Cryptographic integrity is verified in both modes.

---

## Out of Scope

The following threats are **not** mitigated in this reference implementation:

- **Distributed Consensus**: Single-node only (no Byzantine fault tolerance)
- **Quantum-Resistant Cryptography**: Uses HMAC-SHA256 (not post-quantum)
- **Side-Channel Attacks**: No timing attack mitigations
- **DDoS Protection**: No rate limiting or traffic shaping

Production deployments require additional hardening.

---

## Security Assumptions

1. **Clock Synchronization**: System clock is NTP-synchronized (±5 min tolerance)
2. **Filesystem Integrity**: No silent data corruption (use ECC memory + checksumming FS)
3. **Key Management**: Private keys are stored securely (HSM or secrets manager)
4. **Network Security**: TLS for all A2A communication

---

## Incident Response

If a security violation is detected:

1. **Halt**: Stop processing new negotiations
2. **Log**: Record violation details in immutable log
3. **Alert**: Notify security team
4. **Investigate**: Replay WAL to determine scope
5. **Remediate**: Fix vulnerability, rotate keys if needed

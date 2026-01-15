# Glossary

This glossary defines the core terminology used in the Medical Supplies Procurement Negotiation Agent.

---

## Technical Terms

### Invariant
A formal safety property that must hold true at all times during system operation. Invariants are derived from a TLA+ specification and enforced at runtime.

### Deterministic State Machine
A system where every state and transition is explicitly defined, ensuring that given the same input, it will always reach the exact same state.

### Write-Ahead Log (WAL)
An append-only file where all state transitions are recorded before they are executed. This ensures data durability and reconstruction capability.

### Hash Chaining
A technique where each record in a log contains a cryptographic hash of the previous record, creating a tamper-evident audit trail.

### Idempotency
An operation that can be applied multiple times without changing the result beyond the initial application. This is critical for preventing duplicate commits on retry.

### Monotonicity
In the context of negotiation, it refers to concessions moving in a single, predictable direction (e.g., price only decreases, volume only increases).

---

## Business & Governance Terms

### Non-Repudiation
The assurance that a party to a contract or communication cannot deny the authenticity of their signature or the sending of a message.

### Duty of Care
The legal obligation of an institution to ensure its systems (including AI) operate within defined safety and regulatory bounds.

### Emergency Override
A governed exception that allows high-level authority (e.g., CFO/CEO) to bypass normal approval flows during critical events (e.g., life safety).

### Audit Replay Mode
A specialized execution mode that relaxes time-based checks (like token expiry) to allow full reconstruction of historical negotiations for forensics.

### LLM Sandbox
A constrained environment where Large Language Models generate text but have zero authority to modify state, execute transactions, or bypass policy.

---

## Compliance Terms

### Defensibility
The property of a system's records being legally acceptable and forensicly sound in a court of law or regulatory audit.

### Separation of Duties
A security principle where more than one person is required to complete a critical task (e.g., AI proposes terms, Human approves commitment).

### Policy Version Pinning
The practice of locking a negotiation to the specific version of a procurement policy that was in effect when it started.

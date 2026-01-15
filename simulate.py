from engine.state_machine import NegotiationState, NegotiationContext, transition
from engine.invariants import check_all_invariants

print("=" * 60)
print("MEDICAL PROCUREMENT NEGOTIATION SIMULATION")
print("(Mocked data for demonstration purposes)")
print("=" * 60)

# Initialize negotiation
ctx = NegotiationContext(negotiation_id="SIM-001")
print(f"\n[OK] Negotiation initialized: {ctx.negotiation_id}")
print(f"     State: {ctx.state.value}")

# Capability discovery
print("\n[TRANSITION] INIT -> CAPABILITY_DISCOVERY")
ctx.state = transition(ctx.state, NegotiationState.CAPABILITY_DISCOVERY)
print(f"     State: {ctx.state.value}")

# Anchor proposed
print("\n[TRANSITION] CAPABILITY_DISCOVERY -> ANCHOR_PROPOSED")
ctx.state = transition(ctx.state, NegotiationState.ANCHOR_PROPOSED)
print(f"     State: {ctx.state.value}")
print(f"     Terms: [MOCKED - Policy-defined anchor]")

# Negotiating
print("\n[TRANSITION] ANCHOR_PROPOSED -> NEGOTIATING")
ctx.state = transition(ctx.state, NegotiationState.NEGOTIATING)
ctx.round = 1
print(f"     State: {ctx.state.value} (Round {ctx.round})")
print(f"     Vendor counter: [MOCKED]")
print(f"     Our response: [MOCKED - LLM-generated, policy-validated]")

# Agreement draft
print("\n[TRANSITION] NEGOTIATING -> AGREEMENT_DRAFT")
ctx.state = transition(ctx.state, NegotiationState.AGREEMENT_DRAFT)
print(f"     State: {ctx.state.value}")
print(f"     Final terms: [MOCKED]")

# Human approval
print("\n[TRANSITION] AGREEMENT_DRAFT -> HUMAN_APPROVAL")
ctx.state = transition(ctx.state, NegotiationState.HUMAN_APPROVAL)
print(f"     State: {ctx.state.value}")
print(f"     [WAITING] Human approval required...")

# Simulate approval
approval_valid = True
print(f"     [OK] Approval granted")

# Check invariants before commit
print("\n[CHECKING] Safety invariants...")
check_all_invariants(
    prev_state=ctx.state,
    next_state=NegotiationState.COMMIT,
    approval_valid=approval_valid
)
print(f"     [OK] All invariants satisfied")

# Commit
print("\n[TRANSITION] HUMAN_APPROVAL -> COMMIT")
ctx.state = transition(ctx.state, NegotiationState.COMMIT)
print(f"     State: {ctx.state.value}")
print(f"     [OK] Negotiation committed")

# Demonstrate terminal state absorption
print("\n[DEMONSTRATION] Attempting illegal transition from terminal state...")
try:
    transition(ctx.state, NegotiationState.NEGOTIATING)
    print("     [ERROR] Transition succeeded (should have failed)")
except Exception as e:
    print(f"     [OK] Transition rejected: {e}")

print("\n" + "=" * 60)
print("SIMULATION COMPLETE")
print("=" * 60)
print("\nNote: This simulation uses mocked data.")
print("Production system includes:")
print("  - Real policy validation")
print("  - Cryptographic message signing")
print("  - Immutable audit log")
print("  - Emergency override governance")

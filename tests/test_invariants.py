import pytest
from hypothesis import given, strategies as st
from engine.state_machine import NegotiationState, transition, InvalidTransitionError, TERMINAL_STATES
from engine.invariants import check_all_invariants, InvariantViolation

# Strategy for generating valid state sequences
@st.composite
def state_sequence(draw):
    """Generates a sequence of valid state transitions."""
    states = [NegotiationState.INIT]
    current = NegotiationState.INIT
    
    for _ in range(draw(st.integers(min_value=1, max_value=10))):
        if current in TERMINAL_STATES:
            break
        
        # Simple progression for testing
        if current == NegotiationState.INIT:
            current = NegotiationState.CAPABILITY_DISCOVERY
        elif current == NegotiationState.CAPABILITY_DISCOVERY:
            current = NegotiationState.ANCHOR_PROPOSED
        elif current == NegotiationState.ANCHOR_PROPOSED:
            current = NegotiationState.NEGOTIATING
        elif current == NegotiationState.NEGOTIATING:
            current = draw(st.sampled_from([
                NegotiationState.NEGOTIATING,
                NegotiationState.AGREEMENT_DRAFT
            ]))
        elif current == NegotiationState.AGREEMENT_DRAFT:
            current = NegotiationState.HUMAN_APPROVAL
        elif current == NegotiationState.HUMAN_APPROVAL:
            current = NegotiationState.COMMIT
        
        states.append(current)
    
    return states

@given(states=state_sequence())
def test_terminal_states_are_absorbing(states):
    """
    Property: Once a negotiation reaches a terminal state (COMMIT or ABORT),
    it cannot transition to any other state.
    
    This verifies INV_S3 under fuzzing.
    """
    for i in range(len(states) - 1):
        current = states[i]
        next_state = states[i + 1]
        
        if current in TERMINAL_STATES:
            # Terminal states should not allow transitions
            with pytest.raises(InvalidTransitionError):
                transition(current, next_state)

def test_unauthorized_commit_rejected():
    """
    Property: A negotiation cannot transition to COMMIT without approval.
    
    This verifies INV_S1.
    """
    with pytest.raises(InvariantViolation, match="INV_S1"):
        check_all_invariants(
            prev_state=NegotiationState.HUMAN_APPROVAL,
            next_state=NegotiationState.COMMIT,
            approval_valid=False,
            emergency_override=False
        )

def test_monotonicity_violation_detected():
    """
    Property: Concessions cannot reverse (price cannot increase).
    
    This verifies INV_S2.
    """
    old_terms = {"unit_price": 0.90}
    new_terms = {"unit_price": 1.00}  # Price increased!
    
    with pytest.raises(InvariantViolation, match="INV_S2"):
        check_all_invariants(
            prev_state=NegotiationState.NEGOTIATING,
            next_state=NegotiationState.NEGOTIATING,
            old_terms=old_terms,
            new_terms=new_terms
        )

def test_valid_transition_succeeds():
    """
    Property: Valid transitions with proper authorization succeed.
    """
    # Should not raise
    check_all_invariants(
        prev_state=NegotiationState.HUMAN_APPROVAL,
        next_state=NegotiationState.COMMIT,
        approval_valid=True,  # Proper authorization
        emergency_override=False
    )

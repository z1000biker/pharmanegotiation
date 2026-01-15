from engine.state_machine import NegotiationState, TERMINAL_STATES

class InvariantViolation(Exception):
    """Raised when a safety invariant is violated."""
    def __init__(self, invariant_id: str, message: str):
        self.invariant_id = invariant_id
        super().__init__(f"[{invariant_id}] {message}")

def check_terminal_absorption(prev_state: NegotiationState, next_state: NegotiationState):
    """
    INV_S3: Terminal State Absorption
    
    Once a negotiation reaches COMMIT or ABORT, it cannot transition to any other state.
    This ensures finality and prevents post-commitment modification.
    
    Raises:
        InvariantViolation: If attempting to transition out of terminal state
    """
    if prev_state in TERMINAL_STATES and prev_state != next_state:
        raise InvariantViolation(
            "INV_S3",
            f"Cannot transition out of terminal state {prev_state.value}"
        )

def check_unauthorized_commit(approval_valid: bool, emergency_override: bool, next_state: NegotiationState):
    """
    INV_S1: Unauthorized Commit Prevention
    
    A negotiation may only transition to COMMIT if:
    - A valid human approval token exists, OR
    - An emergency override has been issued
    
    This prevents autonomous execution without human authority.
    
    Raises:
        InvariantViolation: If attempting to COMMIT without authorization
    """
    if next_state == NegotiationState.COMMIT:
        if not (approval_valid or emergency_override):
            raise InvariantViolation(
                "INV_S1",
                "Cannot COMMIT without valid approval or emergency override"
            )

def check_monotonicity(old_terms: dict, new_terms: dict):
    """
    INV_S2: Monotonic Concessions
    
    Concessions must move in institution-favorable directions:
    - Unit price: must decrease (buyer favorable)
    - Volume: must increase (seller favorable)
    
    This prevents concession reversals that harm the institution.
    
    Note: Production version includes policy-specific monotonicity rules.
    
    Raises:
        InvariantViolation: If concession reversal is detected
    """
    if not old_terms or not new_terms:
        return
    
    # Example check (production has policy-driven logic)
    if 'unit_price' in old_terms and 'unit_price' in new_terms:
        if new_terms['unit_price'] > old_terms['unit_price']:
            raise InvariantViolation(
                "INV_S2",
                "Concession reversal: Price cannot increase"
            )

# Public interface for invariant checking
def check_all_invariants(
    prev_state: NegotiationState,
    next_state: NegotiationState,
    approval_valid: bool = False,
    emergency_override: bool = False,
    old_terms: dict = None,
    new_terms: dict = None
):
    """
    Checks all safety invariants before allowing a transition.
    
    This is the runtime enforcement point for formal safety properties.
    """
    check_terminal_absorption(prev_state, next_state)
    check_unauthorized_commit(approval_valid, emergency_override, next_state)
    
    if old_terms and new_terms:
        check_monotonicity(old_terms, new_terms)

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime

class NegotiationState(Enum):
    """
    Explicit states in the negotiation state machine.
    Transitions are deterministic and policy-governed.
    """
    INIT = "INIT"
    CAPABILITY_DISCOVERY = "CAPABILITY_DISCOVERY"
    ANCHOR_PROPOSED = "ANCHOR_PROPOSED"
    NEGOTIATING = "NEGOTIATING"
    STALLED = "STALLED"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    AGREEMENT_DRAFT = "AGREEMENT_DRAFT"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    COMMIT = "COMMIT"
    ABORT = "ABORT"

# Terminal states (absorbing)
TERMINAL_STATES = {NegotiationState.COMMIT, NegotiationState.ABORT}

# Allowed transitions (simplified for public reference)
ALLOWED_TRANSITIONS = {
    NegotiationState.INIT: {NegotiationState.CAPABILITY_DISCOVERY},
    NegotiationState.CAPABILITY_DISCOVERY: {NegotiationState.ANCHOR_PROPOSED},
    NegotiationState.ANCHOR_PROPOSED: {NegotiationState.NEGOTIATING},
    NegotiationState.NEGOTIATING: {
        NegotiationState.NEGOTIATING,
        NegotiationState.STALLED,
        NegotiationState.POLICY_VIOLATION,
        NegotiationState.AGREEMENT_DRAFT
    },
    NegotiationState.STALLED: {NegotiationState.NEGOTIATING, NegotiationState.ABORT},
    NegotiationState.POLICY_VIOLATION: {NegotiationState.NEGOTIATING, NegotiationState.ABORT},
    NegotiationState.AGREEMENT_DRAFT: {NegotiationState.HUMAN_APPROVAL},
    NegotiationState.HUMAN_APPROVAL: {NegotiationState.COMMIT, NegotiationState.ABORT},
    NegotiationState.COMMIT: set(),  # Terminal
    NegotiationState.ABORT: set()    # Terminal
}

class InvalidTransitionError(Exception):
    """Raised when an illegal state transition is attempted."""
    pass

def transition(current_state: NegotiationState, next_state: NegotiationState) -> NegotiationState:
    """
    Validates and executes a state transition.
    
    Args:
        current_state: Current negotiation state
        next_state: Desired next state
        
    Returns:
        The next state if transition is valid
        
    Raises:
        InvalidTransitionError: If transition is not allowed
    """
    # Check terminal state absorption (INV_S3)
    if current_state in TERMINAL_STATES:
        raise InvalidTransitionError(
            f"Cannot transition out of terminal state {current_state.value}"
        )
    
    # Check if transition is allowed
    if next_state not in ALLOWED_TRANSITIONS.get(current_state, set()):
        raise InvalidTransitionError(
            f"Illegal transition: {current_state.value} -> {next_state.value}"
        )
    
    return next_state

@dataclass
class NegotiationContext:
    """
    Minimal negotiation context for public reference.
    Production version includes policy bindings, approval tokens, etc.
    """
    negotiation_id: str
    state: NegotiationState = NegotiationState.INIT
    round: int = 0
    
    # Redacted: policy_version_hash, approval_token, emergency_override, etc.

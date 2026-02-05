"""
Safety constraints for the assistive robot.

This module implements HARD RULES that prevent dangerous or nonsensical actions.
These constraints act as a "safety layer" that blocks actions before they can be
executed, ensuring the robot doesn't enter catastrophic states.

This file represents the robot's built-in safety mechanisms
that exist regardless of the decision-making AI's choices.

Key concepts:
- Hard constraints: Actions are completely blocked (return False)
- Soft constraints: Actions allowed but warnings issued (via get_constraint_warnings)
"""

from core.actions import Action
from core.state import RobotState


def is_action_allowed(action: Action, state: RobotState) -> tuple[bool, str]:
    """
    Check if an action is allowed given the current state.
    
    Validates that an action can be safely executed given the robot's
    current state. Hard constraints that return False will prevent the
    action from being executed entirely.
    
    Args:
        action: The Action being considered for execution
        state: Current RobotState containing battery, urgency, etc.
    
    Returns:
        tuple[bool, str]: A tuple of (allowed, reason) where:
            - allowed: True if action can be executed, False if blocked
            - reason: Human-readable explanation of the decision
                     (e.g., "Action allowed" or "Cannot help: battery too low")
                     
    Example:
        >>> allowed, reason = is_action_allowed(Action.HELP_USER, state)
        >>> if not allowed:
        >>>     print(f"Blocked: {reason}")
    """
    
    # Constraint 1: Cannot help if battery is depleted
    if action == Action.HELP_USER and state.is_battery_depleted():
        return False, "Cannot help user: battery depleted"
    
    # Constraint 2: Cannot help if battery is below minimum threshold
    if action == Action.HELP_USER and state.battery < 10:
        return False, "Cannot help user: battery too low (need 10%)"
    
    # Constraint 3: If battery is critical (<20) and not charging, strongly prefer recharge
    # (This is a soft constraint we'll enforce as a warning, not a block)
    
    # Constraint 4: Cannot wait if urgency is critical AND battery allows helping
    if (action == Action.WAIT and 
        state.user_urgency >= 3 and 
        state.battery >= 15):
        return False, "Cannot wait: user urgency is critical and we can help"
    
    # Constraint 5: Cannot recharge if already fully charged
    if action == Action.RECHARGE and state.battery >= 95:
        return False, "Already fully charged"
    
    # All checks passed
    return True, "Action allowed"


def get_constraint_warnings(action: Action, state: RobotState) -> list[str]:
    """
    Get warnings (not blockers) about a potentially risky action.
    
    Unlike is_action_allowed(), these warnings don't prevent the action
    from being executed. They're logged to inform the user that the AI
    is taking a calculated risk or making a questionable choice.
    
    Args:
        action: The Action being considered
        state: Current RobotState
        
    Returns:
        list[str]: List of warning messages (empty list if no warnings)
                   Each warning is a human-readable string describing
                   the potential risk.
                   
    Example:
        >>> warnings = get_constraint_warnings(Action.HELP_USER, state)
        >>> for warning in warnings:
        >>>     print(f"⚠️ {warning}")
    """
    warnings = []
    
    # Warning: Helping with low battery
    if action == Action.HELP_USER and state.is_battery_critical():
        warnings.append("WARNING: Helping with critically low battery (risk of depletion)")
    
    # Warning: Recharging when user is urgent
    if action == Action.RECHARGE and state.has_urgent_user():
        warnings.append("WARNING: Recharging while user needs urgent help")
    
    # Warning: Waiting when urgency is high
    if action == Action.WAIT and state.user_urgency >= 2:
        warnings.append("WARNING: Waiting while user urgency is high")
    
    return warnings


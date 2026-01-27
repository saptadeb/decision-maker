"""
Safety constraints for the assistive robot.

These are HARD RULES that prevent dangerous or nonsensical actions.
Students don't edit this — it's the "safety layer."
"""

from core.actions import Action
from core.state import RobotState


def is_action_allowed(action: Action, state: RobotState) -> tuple[bool, str]:
    """
    Check if an action is allowed given the current state.
    
    Returns:
        (allowed, reason) — if not allowed, reason explains why
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
    Get warnings (not blockers) about an action.
    
    These are logged but don't prevent the action.
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


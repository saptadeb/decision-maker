"""
Available actions for the assistive robot.

Each action has costs, benefits, and requirements.
"""

from enum import Enum


class Action(Enum):
    """
    All possible robot actions.
    
    Enumeration of the four actions the assistive robot can take:
    - HELP_USER: Assist the user (costs battery, reduces urgency)
    - RECHARGE: Go to charging station (gains battery, takes time)
    - WAIT: Do nothing and observe (costs small battery, increases urgency)
    - CALL_FOR_HELP: Request human assistance (ends scenario)
    """
    
    HELP_USER = "help_user"
    RECHARGE = "recharge"
    WAIT = "wait"
    CALL_FOR_HELP = "call_for_help"
    
    def __str__(self) -> str:
        """
        Return uppercase string representation of the action.
        
        Returns:
            str: Uppercase action name (e.g., "HELP_USER")
        """
        return self.value.upper()


# Action properties (used by simulator)
# Each action has associated costs, benefits, and requirements that
# define its effects on the robot state and environment.
ACTION_PROPERTIES = {
    Action.HELP_USER: {
        "battery_cost": 15,
        "time_cost": 1,
        "urgency_reduction": 1,
        "description": "Assist the user with their need",
        "requires_battery": 10,  # Minimum battery to attempt
    },
    Action.RECHARGE: {
        "battery_gain": 50,
        "time_cost": 2,
        "urgency_change": 1,  # User urgency may increase while waiting
        "description": "Go to charging station and recharge",
        "requires_battery": 0,
    },
    Action.WAIT: {
        "battery_cost": 2,
        "time_cost": 1,
        "urgency_change": 1,  # Risk: urgency increases
        "description": "Do nothing, observe situation",
        "requires_battery": 0,
    },
    Action.CALL_FOR_HELP: {
        "battery_cost": 5,
        "time_cost": 1,
        "description": "Request human assistance (gives up task)",
        "requires_battery": 0,
        "ends_scenario": True,
    },
}


def get_action_description(action: Action) -> str:
    """
    Get human-readable description of an action.
    
    Args:
        action: The Action enum value to describe
        
    Returns:
        str: A descriptive sentence explaining what the action does
        
    Example:
        >>> get_action_description(Action.HELP_USER)
        'Assist the user with their need'
    """
    return ACTION_PROPERTIES[action]["description"]


def get_battery_cost(action: Action) -> int:
    """
    Get the net battery cost of performing an action.
    
    Args:
        action: The Action enum value to query
        
    Returns:
        int: Net battery change (positive = cost, negative = gain)
             For example, HELP_USER returns 15, RECHARGE returns -50
             
    Example:
        >>> get_battery_cost(Action.HELP_USER)
        15
        >>> get_battery_cost(Action.RECHARGE)
        -50
    """
    props = ACTION_PROPERTIES[action]
    return props.get("battery_cost", 0) - props.get("battery_gain", 0)


def requires_battery(action: Action) -> int:
    """
    Get the minimum battery level required to perform an action.
    
    Some actions have battery prerequisites (e.g., HELP_USER requires
    at least 10% battery to even attempt). This function returns that
    minimum threshold.
    
    Args:
        action: The Action enum value to query
        
    Returns:
        int: Minimum battery percentage required (0 if no requirement)
        
    Example:
        >>> requires_battery(Action.HELP_USER)
        10
        >>> requires_battery(Action.WAIT)
        0
    """
    return ACTION_PROPERTIES[action].get("requires_battery", 0)


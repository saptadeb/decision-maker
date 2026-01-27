"""
Available actions for the assistive robot.

Each action has costs, benefits, and requirements.
"""

from enum import Enum


class Action(Enum):
    """All possible robot actions."""
    
    HELP_USER = "help_user"
    RECHARGE = "recharge"
    WAIT = "wait"
    CALL_FOR_HELP = "call_for_help"
    
    def __str__(self) -> str:
        return self.value.upper()


# Action properties (used by simulator)
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
    """Get human-readable description of an action."""
    return ACTION_PROPERTIES[action]["description"]


def get_battery_cost(action: Action) -> int:
    """Get battery cost of an action (negative = gain)."""
    props = ACTION_PROPERTIES[action]
    return props.get("battery_cost", 0) - props.get("battery_gain", 0)


def requires_battery(action: Action) -> int:
    """Get minimum battery required to perform action."""
    return ACTION_PROPERTIES[action].get("requires_battery", 0)


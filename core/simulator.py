"""
Simulation engine for the assistive robot.

This module applies action effects and updates the world state.
"""

import random
from core.actions import Action, ACTION_PROPERTIES
from core.state import RobotState, ActionResult


class RobotSimulator:
    """Simulates the effects of robot actions."""
    
    def __init__(self, initial_state: RobotState, max_steps: int = 10):
        self.state = initial_state
        self.max_steps = max_steps
        self.history = []
        self.scenario_ended = False
        
    def apply_action(self, action: Action) -> ActionResult:
        """
        Execute an action and update state.
        
        Returns details about what happened.
        """
        props = ACTION_PROPERTIES[action]
        result = ActionResult(success=True, message="")
        
        # Apply effects based on action type
        if action == Action.HELP_USER:
            result = self._apply_help_user(props)
        elif action == Action.RECHARGE:
            result = self._apply_recharge(props)
        elif action == Action.WAIT:
            result = self._apply_wait(props)
        elif action == Action.CALL_FOR_HELP:
            result = self._apply_call_for_help(props)
        
        # Update time
        self.state.time_step += props.get("time_cost", 1)
        
        # Clamp values
        self.state.battery = max(0, min(100, self.state.battery))
        self.state.user_urgency = max(0, min(3, self.state.user_urgency))
        
        # Check for scenario end conditions
        if props.get("ends_scenario", False):
            self.scenario_ended = True
        
        if self.state.time_step >= self.max_steps:
            self.scenario_ended = True
            result.message += " [TIME LIMIT REACHED]"
        
        # Record history
        self.history.append({
            "step": self.state.time_step,
            "action": action,
            "state": str(self.state),
            "result": result.message,
        })
        
        return result
    
    def _apply_help_user(self, props: dict) -> ActionResult:
        """Apply HELP_USER action."""
        self.state.battery -= props["battery_cost"]
        
        # Reduce urgency (success!)
        old_urgency = self.state.user_urgency
        self.state.user_urgency = max(0, self.state.user_urgency - props["urgency_reduction"])
        
        self.state.current_task = "helping"
        
        if self.state.user_urgency == 0:
            message = f"Helped user successfully! (urgency {old_urgency}->0)"
        else:
            message = f"Helped user (urgency {old_urgency}->{self.state.user_urgency})"
        
        return ActionResult(
            success=True,
            message=message,
            battery_change=-props["battery_cost"],
            urgency_change=-props["urgency_reduction"],
        )
    
    def _apply_recharge(self, props: dict) -> ActionResult:
        """Apply RECHARGE action."""
        old_battery = self.state.battery
        self.state.battery += props["battery_gain"]
        
        # While recharging, user urgency may increase (with probability)
        urgency_increased = False
        if random.random() < 0.4 and self.state.user_urgency < 3:
            self.state.user_urgency += 1
            urgency_increased = True
        
        self.state.current_task = "navigating"
        
        message = f"Recharged battery ({old_battery}->{self.state.battery}%)"
        if urgency_increased:
            message += f" [User urgency increased to {self.state.user_urgency}]"
        
        return ActionResult(
            success=True,
            message=message,
            battery_change=props["battery_gain"],
        )
    
    def _apply_wait(self, props: dict) -> ActionResult:
        """Apply WAIT action."""
        self.state.battery -= props["battery_cost"]
        
        # Risk: urgency may increase
        urgency_increased = False
        if random.random() < 0.5 and self.state.user_urgency < 3:
            self.state.user_urgency += 1
            urgency_increased = True
        
        self.state.current_task = "idle"
        
        message = "Waited and observed"
        if urgency_increased:
            message += f" [User urgency increased to {self.state.user_urgency}!]"
        
        return ActionResult(
            success=True,
            message=message,
            battery_change=-props["battery_cost"],
        )
    
    def _apply_call_for_help(self, props: dict) -> ActionResult:
        """Apply CALL_FOR_HELP action."""
        self.state.battery -= props["battery_cost"]
        self.state.current_task = "idle"
        
        message = "Called for human assistance (scenario ended)"
        
        return ActionResult(
            success=True,
            message=message,
            battery_change=-props["battery_cost"],
        )
    
    def get_summary(self) -> dict:
        """Generate summary of simulation results."""
        return {
            "total_steps": self.state.time_step,
            "final_battery": self.state.battery,
            "final_urgency": self.state.user_urgency,
            "user_helped": self.state.user_urgency == 0,
            "battery_depleted": self.state.is_battery_depleted(),
        }


"""
Simulation engine for the assistive robot.

This module implements the simulation engine that applies action effects
and updates the world state. It provides deterministic, reproducible simulations
with no randomness, ensuring consistent testing and comparison of different
AI implementations.

The simulator:
- Executes actions and updates robot state
- Tracks battery consumption and user urgency changes
- Maintains history of all actions and results
- Detects scenario end conditions (success, failure, timeout)
- Ensures all state changes follow defined rules deterministically
"""

from core.actions import Action, ACTION_PROPERTIES
from core.state import RobotState, ActionResult


class RobotSimulator:
    """
    Simulates the effects of robot actions on state.
    
    The simulator maintains the robot's state and executes actions,
    applying their effects deterministically. It tracks history and
    detects end conditions.
    
    Attributes:
        state: Current RobotState
        max_steps: Maximum steps before timeout
        history: List of all actions and their results
        scenario_ended: Whether the scenario has reached an end condition
    """
    
    def __init__(self, initial_state: RobotState, max_steps: int = 10):
        self.state = initial_state
        self.max_steps = max_steps
        self.history = []
        self.scenario_ended = False
        
    def apply_action(self, action: Action) -> ActionResult:
        """
        Execute an action and update state.
        
        Applies the action's effects to the robot state, updates time,
        clamps values to valid ranges, checks for end conditions, and
        records the action in history.
        
        Args:
            action: The Action to execute
            
        Returns:
            ActionResult: Object containing:
                - success (bool): Whether action completed successfully
                - message (str): Human-readable description of what happened
                - battery_change (int): Battery level change
                - urgency_change (int): Urgency level change
                - task_change (str): New task state if changed
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
        """
        Apply HELP_USER action effects.
        
        Args:
            props: Action properties from ACTION_PROPERTIES
            
        Returns:
            ActionResult: Details of the help action result
        """
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
        """
        Apply RECHARGE action effects.
        
        Note: This implementation is deterministic - urgency does NOT
        increase during recharge (removed randomness for consistent testing).
        
        Args:
            props: Action properties from ACTION_PROPERTIES
            
        Returns:
            ActionResult: Details of the recharge action result
        """
        old_battery = self.state.battery
        self.state.battery += props["battery_gain"]
        
        # Deterministic: No urgency increase during recharge
        # (Removed randomness for consistent testing)
        
        self.state.current_task = "navigating"
        
        message = f"Recharged battery ({old_battery}->{self.state.battery}%)"
        
        return ActionResult(
            success=True,
            message=message,
            battery_change=props["battery_gain"],
        )
    
    def _apply_wait(self, props: dict) -> ActionResult:
        """
        Apply WAIT action effects.
        
        Note: Waiting ALWAYS increases urgency if possible (deterministic).
        This makes WAIT consistently risky, unlike real-world scenarios
        where waiting might sometimes be safe.
        
        Args:
            props: Action properties from ACTION_PROPERTIES
            
        Returns:
            ActionResult: Details of the wait action result
        """
        self.state.battery -= props["battery_cost"]
        
        # Deterministic: Waiting ALWAYS increases urgency if possible
        # (Makes WAIT consistently risky - removed randomness)
        urgency_increased = False
        if self.state.user_urgency < 3:
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
        """
        Apply CALL_FOR_HELP action effects.
        
        This action ends the scenario, representing the robot giving up
        and requesting human assistance.
        
        Args:
            props: Action properties from ACTION_PROPERTIES
            
        Returns:
            ActionResult: Details of the call for help result
        """
        self.state.battery -= props["battery_cost"]
        self.state.current_task = "idle"
        
        message = "Called for human assistance (scenario ended)"
        
        return ActionResult(
            success=True,
            message=message,
            battery_change=-props["battery_cost"],
        )
    
    def get_summary(self) -> dict:
        """
        Generate summary of simulation results.
        
        Returns:
            dict: Summary containing:
                - total_steps (int): Number of steps executed
                - final_battery (int): Battery level at end (0-100)
                - final_urgency (int): User urgency at end (0-3)
                - user_helped (bool): True if urgency reached 0
                - battery_depleted (bool): True if battery reached 0
        """
        return {
            "total_steps": self.state.time_step,
            "final_battery": self.state.battery,
            "final_urgency": self.state.user_urgency,
            "user_helped": self.state.user_urgency == 0,
            "battery_depleted": self.state.is_battery_depleted(),
        }


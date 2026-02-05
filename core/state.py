"""
State representation for the assistive robot simulation.

This module defines the robot's "world view" — everything it knows
when making decisions.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class RobotState:
    """
    Complete state of the robot and its environment.
    
    This dataclass represents everything the robot knows when making
    a decision. It includes both the robot's internal state (battery,
    current task) and environmental factors (user urgency, distances).
    
    Attributes:
        battery (int): Current battery level (0-100%)
        user_urgency (int): User need urgency (0=none, 1=low, 2=medium, 3=critical)
        current_task (str): Current task mode ("idle", "helping", "navigating")
        distance_to_user (float): Distance to user in meters
        distance_to_charger (float): Distance to charging station in meters
        time_pressure (bool): Whether there's a deadline/time constraint
        time_step (int): Current simulation step number
    """
    
    # Robot's internal state (required fields first)
    battery: int  # 0-100
    user_urgency: int  # 0 (none) to 3 (critical)
    
    # Optional fields with defaults
    current_task: Literal["idle", "helping", "navigating"] = "idle"
    distance_to_user: float = 5.0  # meters
    distance_to_charger: float = 10.0  # meters
    time_pressure: bool = False  # Is there a deadline?
    time_step: int = 0
    
    def __str__(self) -> str:
        """
        Human-readable state description.
        
        Returns:
            str: Formatted string showing key state information
        """
        urgency_labels = ["NONE", "LOW", "MEDIUM", "HIGH"]
        urgency_str = urgency_labels[self.user_urgency]
        
        return (
            f"[Step {self.time_step}] "
            f"Battery={self.battery}%, "
            f"Task={self.current_task}, "
            f"Urgency={urgency_str}, "
            f"Distance to user={self.distance_to_user:.1f}m"
        )
    
    def is_battery_critical(self) -> bool:
        """
        Check if battery is dangerously low.
        
        Returns:
            bool: True if battery < 20% (critical threshold)
        """
        return self.battery < 20
    
    def is_battery_depleted(self) -> bool:
        """
        Check if battery is completely empty (failure condition).
        
        Returns:
            bool: True if battery <= 0%
        """
        return self.battery <= 0
    
    def has_urgent_user(self) -> bool:
        """
        Check if user needs immediate help.
        
        Returns:
            bool: True if urgency >= 2 (medium or critical)
        """
        return self.user_urgency >= 2
    
    def can_help_safely(self) -> bool:
        """
        Quick check: is it safe to help right now?
        
        A convenient helper method that combines multiple safety checks.
        
        Returns:
            bool: True if battery > 30% and not depleted
        """
        return self.battery > 30 and not self.is_battery_depleted()


@dataclass
class ActionResult:
    """
    Result of executing an action.
    
    Encapsulates what happened when an action was executed, including
    success status, descriptive message, and state changes.
    
    Attributes:
        success (bool): Whether the action executed successfully
        message (str): Human-readable description of what happened
        battery_change (int): Change in battery level (negative = loss)
        urgency_change (int): Change in urgency level
        task_change (str): New task state if changed
    """
    
    success: bool
    message: str
    battery_change: int = 0
    urgency_change: int = 0
    task_change: str = ""


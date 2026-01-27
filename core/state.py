"""
State representation for the assistive robot simulation.

This module defines the robot's "world view" — everything it knows
when making decisions.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class RobotState:
    """Complete state of the robot and its environment."""
    
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
        """Human-readable state description."""
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
        """Check if battery is dangerously low."""
        return self.battery < 20
    
    def is_battery_depleted(self) -> bool:
        """Check if battery is completely empty."""
        return self.battery <= 0
    
    def has_urgent_user(self) -> bool:
        """Check if user needs immediate help."""
        return self.user_urgency >= 2
    
    def can_help_safely(self) -> bool:
        """Quick check: is it safe to help right now?"""
        return self.battery > 30 and not self.is_battery_depleted()


@dataclass
class ActionResult:
    """Result of executing an action."""
    
    success: bool
    message: str
    battery_change: int = 0
    urgency_change: int = 0
    task_change: str = ""


"""
Core framework for the Assistive Robot Decision-Making System.

This package contains the simulation engine and environment definitions
used to test AI implementations.
"""

from core.state import RobotState, ActionResult
from core.actions import Action, ACTION_PROPERTIES
from core.simulator import RobotSimulator
from core.constraints import is_action_allowed, get_constraint_warnings
from core.metrics import PerformanceMetrics

__all__ = [
    'RobotState',
    'ActionResult',
    'Action',
    'ACTION_PROPERTIES',
    'RobotSimulator',
    'is_action_allowed',
    'get_constraint_warnings',
    'PerformanceMetrics',
]
"""
Action scoring and evaluation system.

This module implements the scoring logic that evaluates the quality of
each possible action in a given state. The score_action() function returns
higher scores for more desirable actions, enabling the decision-making
system to select optimal behaviors.
"""

from core.actions import Action
from core.state import RobotState


def score_action(action: Action, state: RobotState) -> float:
    """
    Evaluate how good an action is in the current state.
    
    Returns a score (higher = better).
    Range: typically -100 to +100, but you can use any scale.
    
    Args:
        action: The action to evaluate
        state: Current robot and environment state
    
    Returns:
        score: How good this action is (higher = better)
    
    HINT: Consider these factors:
        - Safety (battery level)
        - Helpfulness (user urgency)
        - Efficiency (battery cost)
        - Risk (what could go wrong?)
    """
    
    # TODO: Replace this placeholder with your scoring logic!
    
    # Placeholder implementation (very simple and naive!)
    score = 0.0
    
    if action == Action.HELP_USER:
        # Naive logic: always want to help if there's any urgency
        # Completely ignores battery safety!
        if state.user_urgency > 0:
            score = 50
        else:
            score = 10
    
    elif action == Action.RECHARGE:
        # Naive logic: only care about recharge if battery is VERY low
        # Otherwise prefer to keep helping
        if state.battery < 15:
            score = 60
        else:
            score = 0
    
    elif action == Action.WAIT:
        # Naive logic: waiting seems okay sometimes?
        score = 20
    
    elif action == Action.CALL_FOR_HELP:
        # Naive logic: never call for help
        score = -100
    
    return score


def score_safety(action: Action, state: RobotState) -> float:
    """
    TODO (OPTIONAL): Score an action based on safety.
    
    Safety considerations:
    - Avoid battery depletion
    - Don't abandon urgent users
    - Prefer reversible actions
    
    Returns: safety score (higher = safer)
    """
    # TODO: Implement if you want to break down scoring by dimension
    return 0.0


def score_helpfulness(action: Action, state: RobotState) -> float:
    """
    TODO (OPTIONAL): Score an action based on helpfulness.
    
    Helpfulness considerations:
    - Reduce user urgency
    - Respond quickly to needs
    - Complete tasks successfully
    
    Returns: helpfulness score (higher = more helpful)
    """
    # TODO: Implement if you want to break down scoring by dimension
    return 0.0


def score_efficiency(action: Action, state: RobotState) -> float:
    """
    TODO (OPTIONAL): Score an action based on efficiency.
    
    Efficiency considerations:
    - Minimize battery waste
    - Minimize time spent
    - Avoid redundant actions
    
    Returns: efficiency score (higher = more efficient)
    """
    # TODO: Implement if you want to break down scoring by dimension
    return 0.0


# ============================================================================
# DISCUSSION QUESTIONS (answer these after implementing!)
# ============================================================================
#
# 1. What values did you prioritize? (safety, helpfulness, efficiency)
#
# 2. When should the robot "give up" and call for help?
#
# 3. Is it ever okay to let the battery reach 0?
#
# 4. How did you handle situations with no "good" option?
#
# 5. How would your scoring change for different types of users?
#    (elderly person vs. child vs. busy adult)
#
# ============================================================================


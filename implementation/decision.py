"""
Decision-making logic for the assistive robot.

This module implements the core decision-making algorithm that selects
the best action based on the current state. Customize the choose_action()
function to define the robot's behavior and decision strategy.
"""

from core.actions import Action
from core.state import RobotState
from implementation.scoring import score_action
from core.constraints import is_action_allowed


def choose_action(state: RobotState) -> Action:
    """
    Choose the best action for the robot given the current state.
    
    This is called every time step. Your implementation should:
    1. Consider all possible actions
    2. Evaluate each action (using scoring.py)
    3. Choose the best one
    4. Respect safety constraints
    
    Args:
        state: Current robot and environment state
    
    Returns:
        action: The chosen action
    
    HINT: You can use score_action() from scoring.py to help decide!
    """
    
    # TODO: Replace this placeholder with your decision logic!
    
    # Placeholder implementation (simple but not very smart!)
    
    # Get all possible actions
    possible_actions = list(Action)
    
    # Filter out actions that violate constraints
    valid_actions = []
    for action in possible_actions:
        allowed, reason = is_action_allowed(action, state)
        if allowed:
            valid_actions.append(action)
    
    # If no valid actions (shouldn't happen), call for help
    if not valid_actions:
        return Action.CALL_FOR_HELP
    
    # Score each valid action
    best_action = None
    best_score = float('-inf')
    
    for action in valid_actions:
        score = score_action(action, state)
        if score > best_score:
            best_score = score
            best_action = action
    
    return best_action


def evaluate_options(state: RobotState) -> dict[Action, float]:
    """
    TODO (OPTIONAL): Evaluate all actions and return their scores.
    
    This is useful for:
    - Debugging (see what the AI is "thinking")
    - Explaining decisions
    - Advanced decision strategies
    
    Returns:
        dict mapping each Action to its score
    """
    # TODO: Implement if you want to see all scores at once
    scores = {}
    for action in Action:
        scores[action] = score_action(action, state)
    return scores


def make_risky_decision(state: RobotState) -> Action:
    """
    TODO (OPTIONAL): Alternative decision strategy that takes more risks.
    
    Example: Prioritize helping user even with low battery
    
    This is useful for exploring different AI "personalities"!
    """
    # TODO: Implement an alternative decision style
    return choose_action(state)  # Placeholder


def make_conservative_decision(state: RobotState) -> Action:
    """
    TODO (OPTIONAL): Alternative decision strategy that plays it safe.
    
    Example: Always prioritize battery safety over helping
    
    This is useful for exploring different AI "personalities"!
    """
    # TODO: Implement an alternative decision style
    return choose_action(state)  # Placeholder


# ============================================================================
# DISCUSSION QUESTIONS (answer these after implementing!)
# ============================================================================
#
# 1. How does your AI behave differently from your classmates'?
#
# 2. What surprised you about your AI's decisions?
#
# 3. Did your AI ever make a choice you disagreed with? Why?
#
# 4. How would you change your AI for a life-or-death scenario?
#
# 5. What real-world assistive robots exist? How do they decide?
#
# ============================================================================


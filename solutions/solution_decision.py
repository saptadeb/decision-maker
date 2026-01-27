"""
SOLUTION: Advanced decision-making implementation

This demonstrates a more sophisticated decision strategy.
Students should develop their own approach - this is just one example!
"""

from core.actions import Action
from core.state import RobotState
from solutions.solution_scoring import score_action
from core.constraints import is_action_allowed


def choose_action(state: RobotState) -> Action:
    """
    Advanced decision-making with strategic thinking.
    
    This implementation:
    1. Evaluates all valid actions
    2. Applies strategic rules for critical situations
    3. Uses scoring as a tiebreaker
    4. Considers future states (simple lookahead)
    """
    
    # Critical situation handling: override scoring with rules
    
    # Rule 1: If battery is critically low, must recharge immediately
    # (unless user is in critical need and we have just enough battery)
    if state.battery < 15:
        if state.user_urgency >= 3 and state.battery >= 10:
            # Emergency help: user is critical and we can help once
            return Action.HELP_USER
        elif state.battery >= 10:
            # Must recharge before we're completely depleted
            return Action.RECHARGE
        else:
            # Too depleted to do anything useful
            return Action.CALL_FOR_HELP
    
    # Rule 2: If user urgency is critical and we have battery, help now!
    if state.user_urgency >= 3 and state.battery >= 20:
        return Action.HELP_USER
    
    # Rule 3: If battery is low-ish and no immediate urgency, recharge proactively
    if state.battery < 30 and state.user_urgency <= 1:
        return Action.RECHARGE
    
    # For non-critical situations, use scoring-based decision
    return choose_by_scoring(state)


def choose_by_scoring(state: RobotState) -> Action:
    """
    Choose action based on scoring all options.
    """
    possible_actions = list(Action)
    
    # Filter out actions that violate constraints
    valid_actions = []
    for action in possible_actions:
        allowed, reason = is_action_allowed(action, state)
        if allowed:
            valid_actions.append(action)
    
    # If no valid actions, call for help
    if not valid_actions:
        return Action.CALL_FOR_HELP
    
    # Score each valid action
    best_action = None
    best_score = float('-inf')
    
    for action in valid_actions:
        score = score_action(action, state)
        
        # Tiebreaker: prefer helping over waiting
        if score == best_score:
            if action == Action.HELP_USER:
                best_action = action
        
        if score > best_score:
            best_score = score
            best_action = action
    
    return best_action


def evaluate_options(state: RobotState) -> dict[Action, float]:
    """
    Evaluate all actions and return their scores.
    Useful for debugging and understanding decisions.
    """
    scores = {}
    for action in Action:
        allowed, _ = is_action_allowed(action, state)
        if allowed:
            scores[action] = score_action(action, state)
        else:
            scores[action] = float('-inf')  # Mark as invalid
    return scores


def explain_decision(state: RobotState, chosen_action: Action) -> str:
    """
    Generate human-readable explanation of why an action was chosen.
    """
    all_scores = evaluate_options(state)
    
    explanation = f"Chose {chosen_action} because:\n"
    
    # Critical rules
    if state.battery < 15:
        explanation += "  - Battery critically low (emergency protocols)\n"
    if state.user_urgency >= 3:
        explanation += "  - User urgency is critical\n"
    
    # Scoring breakdown
    explanation += f"  - Score: {all_scores[chosen_action]:.1f}\n"
    explanation += "  - Alternative scores:\n"
    
    for action, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
        if action != chosen_action and score > float('-inf'):
            explanation += f"    * {action}: {score:.1f}\n"
    
    return explanation


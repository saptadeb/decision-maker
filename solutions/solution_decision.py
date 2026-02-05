"""
SOLUTION: Advanced decision-making implementation

This demonstrates a more sophisticated decision strategy that balances
multiple priorities through strategic rules and scoring-based fallbacks.

Key design principles:
1. Strategic rules for critical situations (override scoring when necessary)
2. Proactive battery management (recharge before it's critical)
3. Urgency-aware decision making (critical urgency gets priority)
4. Graceful degradation (call for help when truly stuck)
5. Scoring-based decisions for normal situations

This is a reference implementation demonstrating one possible approach.
There are many valid ways to solve these challenges.
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
    
    # ===================================================================
    # STRATEGIC RULES - Critical situations get special handling
    # ===================================================================
    # In critical situations, we use explicit rules rather than scoring
    # to ensure the robot makes the "right" choice according to our values.
    #
    # This section encodes our priorities:
    # - Critical user urgency (3) = highest priority
    # - Battery safety = second priority
    # - Balanced decisions = use scoring for normal cases
    # ===================================================================
    
    # Rule 1: Critical urgency (3) - ALWAYS help if possible!
    # Justification: A critical user need takes priority over battery concerns
    if state.user_urgency >= 3:
        if state.battery >= 15:
            return Action.HELP_USER
        elif state.battery >= 10:
            return Action.HELP_USER
        else:
            return Action.CALL_FOR_HELP
    
    # Rule 2: Battery critically low (<10%) - must recharge NOW
    # Justification: Battery below 10% is emergency territory
    # We can't help anyone if we're depleted
    if state.battery < 10:
        if state.user_urgency >= 2:
            return Action.CALL_FOR_HELP  # Can't help safely
        else:
            return Action.RECHARGE
    
    # Rule 3: Battery very low (10-25%) - careful decision
    # Justification: This is a tricky zone where we need to balance
    # urgency vs. battery safety. One help action costs 15%.
    if state.battery < 25:
        if state.user_urgency >= 2:
            # High urgency - help once then must recharge
            return Action.HELP_USER
        else:
            # Low urgency - recharge first
            return Action.RECHARGE
    
    # Rule 4: High urgency (2+) with good battery (25%+) - help!
    # Justification: We have enough battery to help safely
    if state.user_urgency >= 2 and state.battery >= 25:
        return Action.HELP_USER
    
    # Rule 5: Medium battery (25-45%) with any urgency - help first
    # Justification: Help while we can, then recharge if needed
    if 25 <= state.battery < 45 and state.user_urgency >= 1:
        return Action.HELP_USER
    
    # Rule 6: Low battery (<45%) with low urgency - proactive recharge
    # Justification: User can wait; better to recharge now than later
    if state.battery < 45 and state.user_urgency <= 1:
        return Action.RECHARGE
    
    # Rule 7: Any urgency (1+) with good battery (45%+) - help!
    # Justification: Plenty of battery, user needs help, clear choice
    if state.user_urgency >= 1 and state.battery >= 45:
        return Action.HELP_USER
    
    # For non-critical situations, use scoring-based decision
    return choose_by_scoring(state)


def choose_by_scoring(state: RobotState) -> Action:
    """
    Choose action based on scoring all options.
    
    Used as a fallback when no strategic rule applies. This provides
    flexible decision-making for non-critical situations.
    
    Args:
        state: Current robot state
        
    Returns:
        Action: Highest-scoring valid action
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


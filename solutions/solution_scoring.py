"""
SOLUTION: Advanced scoring implementation

This demonstrates a more sophisticated approach to action evaluation using
multi-dimensional scoring with dynamic weighting.

Key design principles:
1. Multi-dimensional evaluation (safety, helpfulness, efficiency)
2. Dynamic weighting based on context (adjusts priorities by situation)
3. Explicit consideration of tradeoffs
4. Graduated scoring (not just binary good/bad)

Architecture:
- score_action() = Main entry point, combines dimensions with weights
- score_safety() = Evaluates battery safety and risk
- score_helpfulness() = Evaluates user assistance value
- score_efficiency() = Evaluates resource usage

This is a reference implementation demonstrating one possible approach.
"""

from core.actions import Action, get_battery_cost
from core.state import RobotState


def score_action(action: Action, state: RobotState) -> float:
    """
    Advanced scoring that balances multiple priorities.
    
    This implementation uses weighted scoring across multiple dimensions:
    - Safety (avoiding battery depletion)
    - Helpfulness (addressing user urgency)
    - Efficiency (minimizing wasted resources)
    - Risk management (avoiding bad outcomes)
    """
    
    # Calculate individual dimension scores
    safety = score_safety(action, state)
    helpfulness = score_helpfulness(action, state)
    efficiency = score_efficiency(action, state)
    
    # ===================================================================
    # DYNAMIC WEIGHTING - Priorities shift based on context
    # ===================================================================
    # The relative importance of safety, helpfulness, and efficiency
    # changes depending on the current situation.
    #
    # This encodes our value judgment: critical urgency overrides
    # efficiency concerns, while low battery overrides helpfulness.
    # ===================================================================
    
    # Context 1: Critical user urgency (3+)
    # Priority: Helpfulness >> Safety >> Efficiency
    if state.user_urgency >= 3:
        weights = (0.20, 0.70, 0.10)  # Strongly favor helping critical user
    # Context 2: High user urgency (2)
    # Priority: Helpfulness >> Safety >> Efficiency
    elif state.user_urgency >= 2:
        weights = (0.25, 0.60, 0.15)  # Favor helping urgent user
    
    # Context 3: Critical battery (<20%)
    # Priority: Safety >> Helpfulness >> Efficiency
    elif state.battery < 20:
        weights = (0.70, 0.20, 0.10)  # Strongly favor safety when battery critical
    # Context 4: Low battery (20-35%)
    # Priority: Safety >> Helpfulness >> Efficiency
    elif state.battery < 35:
        weights = (0.55, 0.30, 0.15)  # Favor safety when battery low
    
    # Context 5: Normal conditions (good battery, low/medium urgency)
    # Priority: Helpfulness > Safety > Efficiency
    else:
        weights = (0.25, 0.55, 0.20)  # Favor helping when safe
    
    total_score = (
        safety * weights[0] +
        helpfulness * weights[1] +
        efficiency * weights[2]
    )
    
    return total_score


def score_safety(action: Action, state: RobotState) -> float:
    """
    Score based on safety considerations.
    
    Safety focuses on avoiding catastrophic failures (battery depletion)
    and maintaining safe operating margins. Higher score = safer action.
    
    Args:
        action: Action to evaluate
        state: Current state
        
    Returns:
        float: Safety score (typically 0-100+, higher = safer)
    """
    score = 50.0  # Neutral baseline
    
    if action == Action.HELP_USER:
        # Helping is risky if battery is low
        if state.battery < 10:
            score -= 100  # Extremely dangerous!
        elif state.battery < 20:
            score -= 60  # Very dangerous
        elif state.battery < 30:
            score -= 30  # Risky
        elif state.battery < 45:
            score -= 10  # Somewhat risky
        else:
            score += 20  # Safe to help
    
    elif action == Action.RECHARGE:
        # Recharging is safe, especially with low battery
        if state.battery < 20:
            score += 80  # Critical to recharge
        elif state.battery < 35:
            score += 60  # Very good to recharge
        elif state.battery < 50:
            score += 40  # Good preventive action
        elif state.battery < 70:
            score += 15  # Reasonable
        else:
            score -= 10  # Less necessary at high battery
    
    elif action == Action.WAIT:
        # Waiting is risky - urgency increases
        if state.battery > 50:
            score += 10
        else:
            score -= 30  # Risky to wait with low battery
    
    elif action == Action.CALL_FOR_HELP:
        # Calling for help is safe but admission of failure
        score += 20
    
    return score


def score_helpfulness(action: Action, state: RobotState) -> float:
    """
    Score based on helpfulness to user.
    
    Helpfulness measures how well an action addresses user needs,
    considering urgency level and response time. Higher score = more helpful.
    
    Args:
        action: Action to evaluate
        state: Current state with urgency level
        
    Returns:
        float: Helpfulness score (higher = more helpful to user)
    """
    score = 0.0
    
    # Urgency multiplier: more urgent = more important to help
    urgency_weight = [0, 1.5, 3.0, 5.0]  # Strong exponential urgency scaling
    
    if action == Action.HELP_USER:
        # Direct help is good, especially when urgent
        base_help_score = 100  # High base score
        score = base_help_score * urgency_weight[state.user_urgency]
        
        # Bonus for helping when we can afford it
        if state.battery > 45:
            score += 40
        elif state.battery > 30:
            score += 20
        
        # Extra bonus for critical urgency
        if state.user_urgency >= 3:
            score += 80
        elif state.user_urgency >= 2:
            score += 40
    
    elif action == Action.RECHARGE:
        # Recharging delays help, but necessary for future help
        score = 40  # Base value: necessary for future help
        
        if state.user_urgency >= 3:
            score -= 100  # Huge penalty for delaying critical help
        elif state.user_urgency >= 2:
            score -= 60  # Big penalty for delaying urgent help
        elif state.user_urgency == 1:
            score -= 20  # Penalty for delaying
        
        # But necessary if battery is low
        if state.battery < 15:
            score += 80  # Critical to recharge
        elif state.battery < 25:
            score += 60  # Very important to recharge
        elif state.battery < 40:
            score += 35  # Important to recharge
    
    elif action == Action.WAIT:
        # Waiting is only okay if nothing is urgent
        if state.user_urgency == 0:
            score = 20  # Reasonable to wait if no need
        elif state.user_urgency == 1:
            score = -25  # Not great to wait
        elif state.user_urgency == 2:
            score = -70  # Bad to wait when urgent
        else:
            score = -100  # Very bad to wait when critical!
    
    elif action == Action.CALL_FOR_HELP:
        # Last resort: helps user but we failed
        if state.user_urgency >= 2:
            score = 40  # Better than nothing for urgent cases
        else:
            score = -40  # Giving up too early
    
    return score


def score_efficiency(action: Action, state: RobotState) -> float:
    """
    Score based on resource efficiency.
    
    Efficiency measures how well an action uses resources (battery, time)
    relative to the situation. Avoids waste and redundancy.
    Higher score = more efficient.
    
    Args:
        action: Action to evaluate
        state: Current state
        
    Returns:
        float: Efficiency score (higher = better resource usage)
    """
    score = 50.0  # Neutral baseline
    
    if action == Action.HELP_USER:
        # Efficient if user needs help
        if state.user_urgency > 0:
            score += 30
        else:
            score -= 20  # Wasteful to help when not needed
        
        # Check if we have enough battery for the cost
        battery_cost = get_battery_cost(Action.HELP_USER)
        if state.battery - battery_cost < 20:
            score -= 25  # Inefficient to drain battery too low
    
    elif action == Action.RECHARGE:
        # Efficient if battery is actually low
        if state.battery < 30:
            score += 40  # Good time to recharge
        elif state.battery < 50:
            score += 20  # Reasonable
        elif state.battery < 70:
            score -= 10  # Premature
        else:
            score -= 40  # Very wasteful!
    
    elif action == Action.WAIT:
        # Usually inefficient unless we're truly stuck
        score -= 20
        if state.battery < 15 and state.user_urgency == 0:
            score += 30  # Okay to wait if can't do anything anyway
    
    elif action == Action.CALL_FOR_HELP:
        # Very inefficient unless necessary
        score -= 40
        if state.battery < 10 or (state.battery < 20 and state.user_urgency >= 2):
            score += 50  # Actually efficient if we're stuck
    
    return score


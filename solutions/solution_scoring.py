"""
SOLUTION: Advanced scoring implementation

This demonstrates a more sophisticated approach to action evaluation.
Students should develop their own approach - this is just one example!
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
    
    # Weighted combination - you can tune these weights!
    total_score = (
        safety * 0.35 +          # Safety is important but not everything
        helpfulness * 0.45 +     # Primary mission is helping
        efficiency * 0.20        # Efficiency matters but less than safety/help
    )
    
    return total_score


def score_safety(action: Action, state: RobotState) -> float:
    """
    Score based on safety considerations.
    Higher score = safer action.
    """
    score = 50.0  # Neutral baseline
    
    if action == Action.HELP_USER:
        # Helping is risky if battery is low
        if state.battery < 15:
            score -= 80  # Very dangerous!
        elif state.battery < 25:
            score -= 40  # Risky
        elif state.battery < 40:
            score -= 15  # Somewhat risky
        else:
            score += 10  # Safe to help
    
    elif action == Action.RECHARGE:
        # Recharging is safe, especially with low battery
        if state.battery < 30:
            score += 50  # Very safe choice when low
        elif state.battery < 50:
            score += 30  # Good preventive action
        else:
            score += 10  # Always somewhat safe
    
    elif action == Action.WAIT:
        # Waiting is safe if battery is okay
        if state.battery > 40:
            score += 20
        else:
            score -= 10  # Risky to wait with low battery
    
    elif action == Action.CALL_FOR_HELP:
        # Calling for help is safe but admission of failure
        score += 30
    
    return score


def score_helpfulness(action: Action, state: RobotState) -> float:
    """
    Score based on helpfulness to user.
    Higher score = more helpful.
    """
    score = 0.0
    
    # Urgency multiplier: more urgent = more important to help
    urgency_weight = [0, 1.0, 2.0, 3.5]  # Exponential urgency scaling
    
    if action == Action.HELP_USER:
        # Direct help is good, especially when urgent
        base_help_score = 60
        score = base_help_score * urgency_weight[state.user_urgency]
        
        # Bonus for helping when we can afford it
        if state.battery > 40:
            score += 20
    
    elif action == Action.RECHARGE:
        # Recharging delays help, bad if urgent
        score = 20  # Base value: necessary for future help
        
        if state.user_urgency >= 2:
            score -= 40  # Big penalty for delaying urgent help
        elif state.user_urgency == 1:
            score -= 10  # Small penalty for delaying
        
        # But necessary if battery is critical
        if state.battery < 25:
            score += 30  # Must recharge to help later
    
    elif action == Action.WAIT:
        # Waiting is only okay if nothing is urgent
        if state.user_urgency == 0:
            score = 15  # Reasonable to wait if no need
        elif state.user_urgency == 1:
            score = -15  # Not great to wait
        else:
            score = -50  # Very bad to wait when urgent!
    
    elif action == Action.CALL_FOR_HELP:
        # Last resort: helps user but we failed
        if state.user_urgency >= 2:
            score = 30  # Better than nothing for urgent cases
        else:
            score = -30  # Giving up too early
    
    return score


def score_efficiency(action: Action, state: RobotState) -> float:
    """
    Score based on resource efficiency.
    Higher score = more efficient use of resources.
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


"""
Test file to compare current implementation vs reference solution.

This script runs all 12 test scenarios with both implementations and displays
a detailed comparison of their performance across multiple metrics.

Usage:
    python test_comparison.py

What it tests:
    - Task completion rate
    - Battery efficiency
    - Urgency response
    - Risk management
    - Overall performance score

The custom implementation starts with conservative default settings that are
intentionally suboptimal. This demonstrates the value of parameter tuning.

Expected results with defaults:
    - Solution wins: ~2-3 scenarios
    - Ties: ~9-10 scenarios
    - Overall: Solution wins with ~1-2% advantage

Use tuning_gui.py to optimize the custom implementation parameters!
"""

import sys
from pathlib import Path

from core.state import RobotState
from core.actions import Action
from core.simulator import RobotSimulator
from core.metrics import PerformanceMetrics
from core.constraints import is_action_allowed
from config.scenarios import load_scenarios

# Import both implementations
from implementation import decision as impl_decision
from solutions import solution_decision


def run_scenario_with_implementation(name: str, initial_state: RobotState, 
                                     max_steps: int, decision_fn) -> dict:
    """
    Run a single scenario with a specific decision implementation.
    
    Args:
        name: Scenario name
        initial_state: Starting state
        max_steps: Maximum steps allowed
        decision_fn: Decision function to use
        
    Returns:
        dict: Scenario results
    """
    # Store initial values
    initial_battery = initial_state.battery
    initial_urgency = initial_state.user_urgency
    
    sim = RobotSimulator(initial_state, max_steps)
    
    # Simulation loop
    step = 0
    while not sim.scenario_ended and step < max_steps:
        step += 1
        
        # Choose action using provided decision function
        chosen_action = decision_fn(sim.state)
        
        # Check constraints
        allowed, reason = is_action_allowed(chosen_action, sim.state)
        
        if not allowed:
            # Force a safe action if blocked
            chosen_action = Action.CALL_FOR_HELP
        
        # Execute action
        result = sim.apply_action(chosen_action)
        
        # Check for completion
        if sim.state.user_urgency == 0:
            break
        
        if sim.state.is_battery_depleted():
            break
    
    # Get summary
    summary = sim.get_summary()
    
    return {
        'name': name,
        'initial_battery': initial_battery,
        'initial_urgency': initial_urgency,
        'steps': summary['total_steps'],
        'final_battery': summary['final_battery'],
        'user_helped': summary['user_helped'],
        'battery_depleted': summary['battery_depleted'],
    }


def get_test_scenarios():
    """Load all test scenarios from configuration."""
    return load_scenarios('standard')


def main():
    """Run comparison test between implementations."""
    
    print("=" * 80)
    print("  IMPLEMENTATION COMPARISON TEST")
    print("=" * 80)
    print("\nComparing Custom Implementation vs Reference Solution\n")
    
    scenarios = get_test_scenarios()
    
    impl_results = []
    solution_results = []
    
    # Run all scenarios with both implementations
    for name, initial_state, max_steps in scenarios:
        # Run with custom implementation
        impl_state = RobotState(
            battery=initial_state.battery,
            user_urgency=initial_state.user_urgency,
            distance_to_user=initial_state.distance_to_user,
            distance_to_charger=initial_state.distance_to_charger,
            time_pressure=initial_state.time_pressure
        )
        impl_result = run_scenario_with_implementation(
            name, impl_state, max_steps, impl_decision.choose_action
        )
        impl_results.append(impl_result)
        
        # Run with solution implementation
        soln_state = RobotState(
            battery=initial_state.battery,
            user_urgency=initial_state.user_urgency,
            distance_to_user=initial_state.distance_to_user,
            distance_to_charger=initial_state.distance_to_charger,
            time_pressure=initial_state.time_pressure
        )
        solution_result = run_scenario_with_implementation(
            name, soln_state, max_steps, solution_decision.choose_action
        )
        solution_results.append(solution_result)
    
    # Display scenario-by-scenario comparison
    print("\n" + "=" * 80)
    print("  SCENARIO-BY-SCENARIO COMPARISON")
    print("=" * 80)
    print(f"{'Scenario':<28} {'Custom':<20} {'Solution':<20} {'Winner':<12}")
    print("-" * 80)
    
    impl_wins = 0
    solution_wins = 0
    ties = 0
    
    for impl_res, soln_res in zip(impl_results, solution_results):
        name = impl_res['name'][:26]
        
        impl_str = f"Steps:{impl_res['steps']} Bat:{impl_res['final_battery']}%"
        soln_str = f"Steps:{soln_res['steps']} Bat:{soln_res['final_battery']}%"
        
        # Determine winner based on multiple factors
        impl_score = 0
        soln_score = 0
        
        # Success is most important
        if impl_res['user_helped'] and not soln_res['user_helped']:
            impl_score += 100
        elif soln_res['user_helped'] and not impl_res['user_helped']:
            soln_score += 100
        
        # Battery efficiency (if both succeeded)
        if impl_res['user_helped'] and soln_res['user_helped']:
            if impl_res['final_battery'] > soln_res['final_battery']:
                impl_score += 10
            elif soln_res['final_battery'] > impl_res['final_battery']:
                soln_score += 10
            
            # Steps (fewer is better)
            if impl_res['steps'] < soln_res['steps']:
                impl_score += 5
            elif soln_res['steps'] < impl_res['steps']:
                soln_score += 5
        
        # Determine winner
        if impl_score > soln_score:
            winner = "Custom WIN"
            impl_wins += 1
        elif soln_score > impl_score:
            winner = "Solution WIN"
            solution_wins += 1
        else:
            winner = "Tie"
            ties += 1
        
        print(f"{name:<28} {impl_str:<20} {soln_str:<20} {winner:<12}")
    
    print("-" * 80)
    print(f"Implementation Wins: {impl_wins}  |  Solution Wins: {solution_wins}  |  Ties: {ties}")
    print("=" * 80)
    
    # Calculate and compare metrics
    impl_metrics = PerformanceMetrics()
    solution_metrics = PerformanceMetrics()
    
    for result in impl_results:
        impl_metrics.add_scenario(result)
    
    for result in solution_results:
        solution_metrics.add_scenario(result)
    
    # Display detailed metrics comparison
    print("\n" + "=" * 80)
    print("  DETAILED METRICS COMPARISON")
    print("=" * 80)
    
    impl_data = impl_metrics.calculate_all_metrics()
    soln_data = solution_metrics.calculate_all_metrics()
    
    metrics_list = [
        ('Task Completion', 'completion_score'),
        ('Battery Efficiency', 'battery_efficiency'),
        ('Urgency Response', 'urgency_response'),
        ('Risk Management', 'risk_score'),
        ('Overall Score', 'overall_score'),
    ]
    
    print(f"\n{'Metric':<25} {'Custom':<15} {'Solution':<15} {'Winner':<15}")
    print("-" * 80)
    
    for name, key in metrics_list:
        impl_val = impl_data[key]
        soln_val = soln_data[key]
        
        if abs(impl_val - soln_val) < 0.5:
            winner = "Tie"
        elif impl_val > soln_val:
            winner = f"Custom (+{impl_val - soln_val:.1f})"
        else:
            winner = f"Solution (+{soln_val - impl_val:.1f})"
        
        print(f"{name:<25} {impl_val:>6.1f}%{'':<8} {soln_val:>6.1f}%{'':<8} {winner:<15}")
    
    print("-" * 80)
    
    # Overall summary
    if impl_data['overall_score'] > soln_data['overall_score']:
        print(f"\n>> Custom Implementation wins overall: {impl_data['overall_score']:.1f}% vs {soln_data['overall_score']:.1f}%")
    elif soln_data['overall_score'] > impl_data['overall_score']:
        print(f"\n>> Reference Solution wins overall: {soln_data['overall_score']:.1f}% vs {impl_data['overall_score']:.1f}%")
    else:
        print(f"\n== Overall tie: Both scored {impl_data['overall_score']:.1f}%")
    
    print("\n" + "=" * 80)
    print("\nNOTE: The custom implementation uses default conservative settings.")
    print("These settings prioritize safety over efficiency, resulting in:")
    print("  - More recharging (lower battery efficiency)")
    print("  - Higher safety margins (lower risk management score)")
    print("  - Similar task completion but less optimal paths")
    print("\nUse the Parameter Tuning GUI (tuning_gui.py) to optimize these settings!")
    print("Optimal ranges: RECHARGE_THRESHOLD=30-35, CRITICAL_BATTERY=15-18")
    print("                HELP_MIN_BATTERY=20-25, SAFETY_WEIGHT=0.35-0.45")
    print("=" * 80)


if __name__ == "__main__":
    main()

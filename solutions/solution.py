"""
SOLUTION: Complete simulation with advanced AI implementation

This script runs the same scenarios as main.py but uses the reference
Reference AI implementation instead of the placeholder. It demonstrates
one approach to solving the decision-making challenges.

Key features of this solution:
- Strategic rules for critical situations
- Multi-dimensional scoring (safety, helpfulness, efficiency)
- Proactive battery management
- Dynamic weight adjustment based on context
- Graceful handling of edge cases

Usage:
    python solutions/solution.py
    
Note: This is ONE valid approach, not THE correct approach!
Alternative strategies can be developed and compared.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import the main modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.state import RobotState
from core.actions import Action
from core.simulator import RobotSimulator
from core.constraints import is_action_allowed, get_constraint_warnings
from core.metrics import PerformanceMetrics

# Import the solution implementations
from solutions import solution_decision


def run_scenario(name: str, initial_state: RobotState, max_steps: int = 10) -> dict:
    """
    Run a single scenario with the Reference AI.
    
    Args:
        name: Human-readable scenario name
        initial_state: Starting robot state
        max_steps: Maximum steps before timeout
        
    Returns:
        dict: Scenario results including steps, battery, success status
    """
    print(f"\n{'='*60}")
    print(f"  Scenario: {name}")
    print(f"{'='*60}")
    print(f"Initial State: {initial_state}\n")
    
    # Store initial values before simulation modifies state
    initial_battery = initial_state.battery
    initial_urgency = initial_state.user_urgency
    
    sim = RobotSimulator(initial_state, max_steps)
    
    # Simulation loop
    step = 0
    while not sim.scenario_ended and step < max_steps:
        step += 1
        
        # Reference AI chooses an action
        chosen_action = solution_decision.choose_action(sim.state)
        
        # Check constraints
        allowed, reason = is_action_allowed(chosen_action, sim.state)
        warnings = get_constraint_warnings(chosen_action, sim.state)
        
        if not allowed:
            print(f"Step {step}: [BLOCKED] {chosen_action} — {reason}")
            # Force a safe action
            chosen_action = Action.CALL_FOR_HELP
        
        # Display decision
        print(f"Step {step}: {sim.state}")
        print(f"  -> Decision: {chosen_action}")
        
        # Display warnings
        for warning in warnings:
            print(f"    {warning}")
        
        # Execute action
        result = sim.apply_action(chosen_action)
        print(f"    {result.message}")
        
        # Check for user success
        if sim.state.user_urgency == 0:
            print(f"\n[SUCCESS] User need fully resolved.")
            break
        
        # Check for battery depletion
        if sim.state.is_battery_depleted():
            print(f"\n[FAILURE] Battery depleted!")
            break
    
    # Display summary
    print(f"\n{'-'*60}")
    print("Scenario Summary:")
    summary = sim.get_summary()
    print(f"  Total steps: {summary['total_steps']}")
    print(f"  Final battery: {summary['final_battery']}%")
    print(f"  Final urgency: {summary['final_urgency']}")
    print(f"  User helped: {'Yes' if summary['user_helped'] else 'No'}")
    print(f"  Battery depleted: {'Yes' if summary['battery_depleted'] else 'No'}")
    print(f"{'-'*60}\n")
    
    # Return results for summary table
    return {
        'name': name,
        'initial_battery': initial_battery,
        'initial_urgency': initial_urgency,
        'steps': summary['total_steps'],
        'final_battery': summary['final_battery'],
        'user_helped': summary['user_helped'],
        'battery_depleted': summary['battery_depleted'],
    }


def main():
    """
    Run all test scenarios with Reference AI.
    
    Executes multiple scenarios demonstrating different challenge types,
    calculates performance metrics, and optionally compares with the
    custom implementation if available.
    """
    
    print("="*60)
    print("  ASSISTIVE ROBOT AI - SOLUTION IMPLEMENTATION")
    print("="*60)
    print("\nThis demonstrates an advanced AI implementation.")
    print("Compare these results with the placeholder in main.py!\n")
    
    results = []
    
    # Scenario 1: Balanced situation
    results.append(run_scenario(
        name="Balanced Start",
        initial_state=RobotState(
            battery=50,
            user_urgency=1,
            distance_to_user=5.0,
            distance_to_charger=10.0,
        ),
        max_steps=8,
    ))
    
    # Scenario 2: Low battery, high urgency (the hard one!)
    results.append(run_scenario(
        name="Low Battery, Urgent User",
        initial_state=RobotState(
            battery=25,
            user_urgency=2,
            distance_to_user=3.0,
            distance_to_charger=15.0,
            time_pressure=True,
        ),
        max_steps=6,
    ))
    
    # Scenario 3: Critical battery
    results.append(run_scenario(
        name="Critical Battery",
        initial_state=RobotState(
            battery=15,
            user_urgency=1,
            distance_to_user=8.0,
            distance_to_charger=5.0,
        ),
        max_steps=8,
    ))
    
    # Scenario 4: High urgency, good battery
    results.append(run_scenario(
        name="Urgent User, Good Battery",
        initial_state=RobotState(
            battery=80,
            user_urgency=3,
            distance_to_user=2.0,
            distance_to_charger=20.0,
            time_pressure=True,
        ),
        max_steps=6,
    ))
    
    # Display summary table
    print("\n" + "="*80)
    print("  SOLUTION PERFORMANCE SUMMARY")
    print("="*80)
    print(f"{'Scenario':<28} {'Start':<12} {'Steps':<7} {'End Bat':<9} {'Success':<9} {'Status'}")
    print("-"*80)
    
    total_success = 0
    total_failures = 0
    
    for result in results:
        name = result['name'][:26]
        start = f"B:{result['initial_battery']}% U:{result['initial_urgency']}"
        steps = str(result['steps'])
        end_bat = f"{result['final_battery']}%"
        success = "YES" if result['user_helped'] else "NO"
        
        if result['battery_depleted']:
            status = "DEPLETED"
            total_failures += 1
        elif result['user_helped']:
            status = "OK"
            total_success += 1
        else:
            status = "INCOMPLETE"
            total_failures += 1
        
        print(f"{name:<28} {start:<12} {steps:<7} {end_bat:<9} {success:<9} {status}")
    
    print("-"*80)
    print(f"Overall: {total_success}/4 scenarios completed successfully")
    print("="*80)
    
    # Calculate and display metrics
    metrics = PerformanceMetrics()
    for result in results:
        metrics.add_scenario(result)
    
    metrics.display_metrics("Reference AI PERFORMANCE METRICS")
    
    # Save solution metrics
    metrics.save_to_file("output/solution_metrics.json")
    
    # Try to compare with custom implementation if it exists
    try:
        custom_metrics = PerformanceMetrics.load_from_file("output/my_metrics.json")
        print("\n" + "="*80)
        print("  COMPARISON: Your AI vs Reference AI")
        print("="*80)
        custom_metrics.compare_with(metrics, "Reference AI")
    except FileNotFoundError:
        print("\nRun main.py first to compare your AI with this solution!")
    
    print("\n" + "="*60)
    print("  Key Differences from Placeholder AI:")
    print("="*60)
    print("- Strategic rules for critical situations")
    print("- Multi-dimensional scoring (safety/help/efficiency)")
    print("- Proactive battery management")
    print("- Better handling of urgency vs. battery tradeoffs")
    print("="*60)


if __name__ == "__main__":
    main()


"""
Main simulation runner for the Assistive Robot AI Workshop.

Run this file to test your AI implementation!
"""

from state import RobotState
from actions import Action
from simulator import RobotSimulator
from decision import choose_action
from constraints import is_action_allowed, get_constraint_warnings
from metrics import PerformanceMetrics


def run_scenario(name: str, initial_state: RobotState, max_steps: int = 10) -> dict:
    """
    Run a single scenario and display results.
    
    Args:
        name: Scenario name
        initial_state: Starting robot state
        max_steps: Maximum number of time steps
    
    Returns:
        dict: Scenario results for summary table
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
        
        # AI chooses an action
        chosen_action = choose_action(sim.state)
        
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
    """Run all test scenarios."""
    
    print("ASSISTIVE ROBOT AI WORKSHOP")
    print("Testing your decision-making implementation...\n")
    
    results = []
    
    # Scenario 1: Balanced situation
    results.append(run_scenario(
        name="Balanced Start",
        initial_state=RobotState(
            battery=50,
            user_urgency=1,  # Low urgency
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
            user_urgency=2,  # High urgency
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
            user_urgency=1,  # Medium urgency
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
            user_urgency=3,  # Critical urgency
            distance_to_user=2.0,
            distance_to_charger=20.0,
            time_pressure=True,
        ),
        max_steps=6,
    ))
    
    # Display summary table
    print("\n" + "="*80)
    print("  PERFORMANCE SUMMARY")
    print("="*80)
    print(f"{'Scenario':<28} {'Start':<12} {'Steps':<7} {'End Bat':<9} {'Success':<9} {'Status'}")
    print("-"*80)
    
    total_success = 0
    total_failures = 0
    
    for result in results:
        name = result['name'][:26]  # Truncate if too long
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
    
    metrics.display_metrics("YOUR AI PERFORMANCE METRICS")
    
    # Optionally save metrics for comparison
    metrics.save_to_file("my_metrics.json")
    
    print("\nNext step: Edit decision.py and scoring.py to improve behavior!")
    print("Compare with solution: python solutions/solution.py")


if __name__ == "__main__":
    main()


"""
Scenario loader for test scenarios.

Loads scenarios from scenarios.yml configuration file.
"""

import yaml
from pathlib import Path
from typing import List, Tuple
from core.state import RobotState


def get_scenarios_path() -> Path:
    """Get the path to the scenarios.yml file."""
    return Path(__file__).parent / 'scenarios.yml'


def load_scenarios(scenario_set: str = 'standard') -> List[Tuple[str, RobotState, int]]:
    """
    Load scenarios from YAML configuration.
    
    Args:
        scenario_set: Which set of scenarios to load ('standard', 'gui_full', or 'all')
        
    Returns:
        List of tuples: (name, initial_state, max_steps)
    """
    scenarios_path = get_scenarios_path()
    
    with open(scenarios_path, 'r') as f:
        config = yaml.safe_load(f)
    
    all_scenarios = config['scenarios']
    scenario_sets = config.get('scenario_sets', {})
    
    # Determine which scenarios to include
    if scenario_set == 'all':
        selected_names = [s['name'] for s in all_scenarios]
    else:
        selected_names = scenario_sets.get(scenario_set, [s['name'] for s in all_scenarios])
    
    # Build scenario list
    result = []
    for scenario in all_scenarios:
        if scenario['name'] in selected_names:
            state = RobotState(
                battery=scenario['battery'],
                user_urgency=scenario['user_urgency'],
                distance_to_user=scenario['distance_to_user'],
                distance_to_charger=scenario['distance_to_charger'],
                time_pressure=scenario.get('time_pressure', False)
            )
            result.append((scenario['name'], state, scenario['max_steps']))
    
    return result


def get_scenario_by_name(name: str) -> Tuple[str, RobotState, int]:
    """
    Get a single scenario by name.
    
    Args:
        name: Scenario name
        
    Returns:
        Tuple of (name, initial_state, max_steps)
        
    Raises:
        ValueError: If scenario not found
    """
    scenarios_path = get_scenarios_path()
    
    with open(scenarios_path, 'r') as f:
        config = yaml.safe_load(f)
    
    for scenario in config['scenarios']:
        if scenario['name'] == name:
            state = RobotState(
                battery=scenario['battery'],
                user_urgency=scenario['user_urgency'],
                distance_to_user=scenario['distance_to_user'],
                distance_to_charger=scenario['distance_to_charger'],
                time_pressure=scenario.get('time_pressure', False)
            )
            return (scenario['name'], state, scenario['max_steps'])
    
    raise ValueError(f"Scenario '{name}' not found")


def list_scenario_sets() -> List[str]:
    """List available scenario sets."""
    scenarios_path = get_scenarios_path()
    
    with open(scenarios_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return list(config.get('scenario_sets', {}).keys()) + ['all']

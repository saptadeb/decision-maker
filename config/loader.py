"""
Centralized configuration loader.

This module provides a single source of truth for loading default parameters
from the YAML configuration file. All modules that need parameters should
import from here to avoid code duplication.
"""

import os
import yaml
from pathlib import Path


# Default parameter values (fallback if config file missing)
DEFAULT_PARAMS = {
    'recharge_threshold': 30,
    'critical_battery': 15,
    'help_min_battery': 20,
    'safety_weight': 0.4,
    'helpfulness_weight': 0.6,
    'proactive_recharge': False,
    'risk_tolerance': 'Medium'
}

# Risk buffer mapping
RISK_BUFFER_MAP = {
    'Low': 1.2,     # Very cautious
    'Medium': 1.0,  # Balanced
    'High': 0.8     # Aggressive
}


def get_config_path() -> Path:
    """Get the path to the default_params.yml config file."""
    # Find the config directory relative to this file
    config_dir = Path(__file__).parent
    return config_dir / 'default_params.yml'


def load_params() -> dict:
    """
    Load parameters from YAML config with fallback to defaults.
    
    Returns:
        dict: Parameter dictionary with all configuration values
    """
    params = DEFAULT_PARAMS.copy()
    config_path = get_config_path()
    
    try:
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if config:
                    params.update(config)
    except Exception as e:
        print(f"Warning: Could not load config from {config_path}: {e}")
        print("Using default parameters instead.")
    
    return params


def get_risk_buffer(risk_tolerance: str = 'Medium') -> float:
    """
    Get the risk buffer multiplier for a given risk tolerance level.
    
    Args:
        risk_tolerance: Risk level ('Low', 'Medium', or 'High')
        
    Returns:
        float: Risk buffer multiplier
    """
    return RISK_BUFFER_MAP.get(risk_tolerance, 1.0)


# Load parameters once at module import
PARAMS = load_params()

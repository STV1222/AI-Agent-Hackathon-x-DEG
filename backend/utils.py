"""
Utility functions for data loading, weather API integration, etc.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

# Path to data directory (parent of backend directory)
DATA_DIR = Path(__file__).parent.parent / "data"


def load_assets(location: str = "London") -> List[Dict[str, Any]]:
    """
    Load DEG assets from JSON file.
    TODO: Filter by location if needed.
    """
    assets_file = DATA_DIR / "assets.json"
    with open(assets_file, "r") as f:
        assets = json.load(f)
    return assets


def load_scenarios() -> Dict[str, Any]:
    """Load predefined scenarios from JSON file."""
    scenarios_file = DATA_DIR / "scenarios.json"
    with open(scenarios_file, "r") as f:
        scenarios = json.load(f)
    return scenarios


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    """Get a specific scenario by ID."""
    scenarios = load_scenarios()
    return scenarios.get(scenario_id)


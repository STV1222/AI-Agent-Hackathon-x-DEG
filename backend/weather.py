"""
Weather data module - mock weather data for scenarios.
Later can be extended to use Open-Meteo or OpenWeather API.
"""

from typing import Dict, Any
from datetime import datetime


def get_mock_weather(scenario: Dict[str, Any], location: str) -> Dict[str, Any]:
    """
    Get mock weather data for a scenario.
    
    Args:
        scenario: Scenario request with event_type, start_date, duration_hours
        location: Location string (e.g., "London")
    
    Returns:
        Dictionary with weather data
    """
    event_type = scenario.get("event_type", "heatwave")
    
    if event_type == "heatwave":
        # Mock heatwave data
        return {
            "max_temp_celsius": 37,
            "min_temp_celsius": 22,
            "avg_temp_celsius": 30,
            "humidity_percent": 65,
            "event_type": "heatwave",
            "duration_hours": scenario.get("duration_hours", 72)
        }
    elif event_type == "flood":
        # Mock flood data
        return {
            "total_rainfall_mm": 80,
            "max_rainfall_per_hour_mm": 15,
            "wind_speed_kmh": 45,
            "event_type": "flood",
            "duration_hours": scenario.get("duration_hours", 24)
        }
    else:
        # Default/unknown event type
        return {
            "event_type": event_type,
            "duration_hours": scenario.get("duration_hours", 24)
        }


def get_weather_for_scenario(scenario_request: Any) -> Dict[str, Any]:
    """
    Get weather data from scenario request.
    Converts Pydantic model to dict for processing.
    """
    scenario_dict = {
        "event_type": scenario_request.event_type,
        "start_date": scenario_request.start_date,
        "duration_hours": scenario_request.duration_hours
    }
    return get_mock_weather(scenario_dict, scenario_request.location)


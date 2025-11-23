"""
Risk engine - calculates risk levels for DEG assets based on weather scenarios.
"""

from typing import List, Dict, Any


def calculate_risk_for_asset(asset: Dict[str, Any], weather_data: Dict[str, Any], event_type: str) -> Dict[str, Any]:
    """
    Calculate risk level for a single asset based on weather data.
    
    Args:
        asset: Asset dictionary
        weather_data: Weather data dictionary
        event_type: "heatwave" or "flood"
    
    Returns:
        RiskResult dictionary or None if no risk
    """
    risk_level = None
    reason = ""
    expected_impact = ""
    
    if event_type == "heatwave":
        max_temp = weather_data.get("max_temp_celsius", 0)
        duration_hours = weather_data.get("duration_hours", 0)
        asset_type = asset.get("type", "")
        criticality = asset.get("criticality", "medium")
        
        # Risk calculation for heatwave
        if max_temp >= 35:
            # High temperature risk -> Grid Congestion Risk
            if asset_type == "substation":
                # Substations are sensitive to overheating AND load spikes
                if max_temp >= 37 and duration_hours >= 48:
                    risk_level = "CRITICAL"
                    reason = f"Projected Load > 120% Capacity (A/C Spike at {max_temp}°C)"
                    expected_impact = "Immediate feeder overload risk, potential thermal runaway"
                elif max_temp >= 36:
                    risk_level = "HIGH"
                    reason = f"Projected Load > 105% Capacity (High A/C Demand)"
                    expected_impact = "Transformer aging acceleration, voltage sag risk"
                else:
                    risk_level = "MEDIUM"
                    reason = f"Projected Load approaching 95% Capacity"
                    expected_impact = "Monitor reserve margins"
                
                # Increase risk for critical assets
                if risk_level == "MEDIUM" and criticality == "high":
                    risk_level = "HIGH"
                    reason += " (critical feeder)"
            elif asset_type == "ev_hub":
                # EV hubs -> Coincident Peak Contributors
                if max_temp >= 37 and duration_hours >= 48:
                    risk_level = "HIGH"
                    reason = f"Coincident Peak Contributor: EV Charging + Grid Stress"
                    expected_impact = "Local feeder congestion likely during evening peak"
                elif max_temp >= 36:
                    risk_level = "MEDIUM"
                    reason = f"Potential Peak Contributor"
                    expected_impact = "Monitor coincident load"
            elif asset_type == "solar_farm":
                # Solar farms: high temp can reduce efficiency -> Supply shortfall
                if max_temp >= 37:
                    risk_level = "MEDIUM"
                    reason = f"Thermal derating: PV efficiency drop predicted"
                    expected_impact = "Reduced local generation capacity (~5-10%)"
    
    elif event_type == "flood":
        total_rainfall = weather_data.get("total_rainfall_mm", 0)
        max_rainfall_per_hour = weather_data.get("max_rainfall_per_hour_mm", 0)
        asset_type = asset.get("type", "")
        is_flood_zone = asset.get("flood_zone", False)
        criticality = asset.get("criticality", "medium")
        
        # Risk calculation for flood
        if is_flood_zone:
            if total_rainfall >= 60 and max_rainfall_per_hour >= 10:
                risk_level = "CRITICAL"
                reason = f"Located in flood zone, forecast {total_rainfall}mm rainfall"
                expected_impact = "Flooding risk, equipment damage possible"
            elif total_rainfall >= 40:
                risk_level = "HIGH"
                reason = f"Located in flood zone, forecast {total_rainfall}mm rainfall"
                expected_impact = "High flood risk, prepare protective measures"
        else:
            if total_rainfall >= 80 and max_rainfall_per_hour >= 15:
                risk_level = "HIGH"
                reason = f"Heavy rainfall forecast: {total_rainfall}mm"
                expected_impact = "Flash flooding possible, monitor drainage"
            elif total_rainfall >= 60:
                risk_level = "MEDIUM"
                reason = f"Forecast {total_rainfall}mm rainfall"
                expected_impact = "Monitor local flooding conditions"
        
        # All electrical assets at risk from flooding
        if asset_type in ["substation", "ev_hub"] and risk_level is None:
            if total_rainfall >= 50:
                risk_level = "MEDIUM"
                reason = f"Forecast {total_rainfall}mm rainfall may affect electrical infrastructure"
                expected_impact = "Water ingress risk to electrical equipment"
    
    # Return risk result if risk exists
    if risk_level:
        # Add zone/location info for better impact description
        if asset.get("feeds"):
            expected_impact += f" affecting {asset.get('feeds')}"
        
        return {
            "asset_id": asset.get("id"),
            "risk_level": risk_level,
            "reason": reason,
            "expected_impact": expected_impact
        }
    
    return None


def simulate_risk(event_type: str, weather_data: Dict[str, Any], assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Run risk simulation for all assets.
    
    Args:
        event_type: "heatwave" or "flood"
        weather_data: Weather data dictionary
        assets: List of asset dictionaries
    
    Returns:
        List of RiskResult dictionaries
    """
    risks = []
    
    for asset in assets:
        risk = calculate_risk_for_asset(asset, weather_data, event_type)
        if risk:
            risks.append(risk)
    
    # Sort by risk level (CRITICAL first)
    risk_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    risks.sort(key=lambda x: risk_order.get(x["risk_level"], 99))
    
    return risks


# API Contracts & JSON Schemas

This document defines the JSON contracts between backend, AI agent, and frontend.

## Core Entities

### Asset (DEG)
```json
{
  "id": "SUB_001",
  "name": "Westminster Substation",
  "type": "substation",
  "lat": 51.5074,
  "lon": -0.1278,
  "capacity_kw": 5000,
  "criticality": "high"
}
```

### RiskResult
```json
{
  "asset_id": "SUB_001",
  "risk_level": "CRITICAL",
  "reason": "Forecast 37°C for 48h, > design 35°C",
  "expected_impact": "Possible transformer overheating, outages in Zone A"
}
```

### MitigationAction (Agent Output)
```json
{
  "asset_id": "SUB_001",
  "action_type": "deploy_mobile_generator",
  "urgency": "high",
  "justification": "Critical substation feeding hospital, high heat stress.",
  "target_time": "2025-11-26T08:00:00Z"
}
```

### BecknServiceResult
```json
{
  "provider_id": "GENSET_UK_01",
  "name": "UK Mobile Gensets Ltd",
  "eta_hours": 4,
  "price_estimate": 1200
}
```

## API Endpoints

### POST /scenario/run

**Request:**
```json
{
  "location": "London",
  "event_type": "heatwave",
  "start_date": "2025-11-26T00:00:00Z",
  "duration_hours": 72
}
```

**Response:**
```json
{
  "scenario": { ... },
  "assets": [ ... ],
  "risks": [ ... ]
}
```

### POST /agent/mitigate

**Request:**
```json
{
  "scenario": { ... },
  "risks": [ ... ],
  "assets": [ ... ]
}
```

**Response:**
```json
{
  "summary_text": "AI analysis summary...",
  "mitigation_actions": [ ... ]
}
```

### POST /beckn/execute

**Request:**
```json
{
  "actions": [ ... ]
}
```

**Response:**
```json
{
  "log": [
    {
      "asset_id": "SUB_001",
      "service_type": "mobile_generator",
      "provider": "GENSET_UK_01",
      "status": "confirmed"
    }
  ]
}
```


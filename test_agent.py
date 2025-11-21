import requests
import json

url = "http://localhost:8001/agent/mitigate"

data = {
  "scenario": {
    "location": "London",
    "event_type": "heatwave",
    "start_date": "2025-07-15T00:00:00Z",
    "duration_hours": 48
  },
  "assets": [
    {
      "id": "sub_1",
      "name": "North Substation",
      "type": "substation",
      "lat": 51.5074,
      "lon": -0.1278,
      "capacity_kw": 5000,
      "criticality": "high"
    }
  ],
  "risks": [
    {
      "asset_id": "sub_1",
      "risk_level": "HIGH",
      "reason": "Temperature exceeds 35C",
      "expected_impact": "Overheating"
    }
  ]
}

try:
    print("Sending request to agent...")
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Failed to connect: {e}")


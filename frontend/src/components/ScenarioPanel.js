import React, { useState } from 'react';
import './ScenarioPanel.css';

const ScenarioPanel = ({ onRunScenario }) => {
  const [location, setLocation] = useState('London');
  const [eventType, setEventType] = useState('heatwave');
  const [startDate, setStartDate] = useState('2025-11-26T00:00');
  const [durationHours, setDurationHours] = useState(72);

  const predefinedScenarios = [
    { id: 'london_heatwave_3d', name: 'London Heatwave - 3 Days', location: 'London', eventType: 'heatwave', duration: 72 },
    { id: 'london_flood_24h', name: 'London Flood - 24 Hours', location: 'London', eventType: 'flood', duration: 24 },
    { id: 'london_heatwave_5d', name: 'London Heatwave - 5 Days', location: 'London', eventType: 'heatwave', duration: 120 },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    const scenarioData = {
      location,
      event_type: eventType,
      start_date: new Date(startDate).toISOString(),
      duration_hours: parseInt(durationHours),
    };
    onRunScenario(scenarioData);
  };

  const handlePredefinedScenario = (scenario) => {
    setLocation(scenario.location);
    setEventType(scenario.eventType);
    setDurationHours(scenario.duration);
    const scenarioData = {
      location: scenario.location,
      event_type: scenario.eventType,
      start_date: new Date().toISOString(),
      duration_hours: scenario.duration,
    };
    onRunScenario(scenarioData);
  };

  return (
    <div className="scenario-panel">
      <h2>🌍 Scenario Configuration</h2>
      
      <div className="predefined-scenarios">
        <h3>Quick Scenarios</h3>
        {predefinedScenarios.map((scenario) => (
          <button
            key={scenario.id}
            className="scenario-btn"
            onClick={() => handlePredefinedScenario(scenario)}
          >
            {scenario.name}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="scenario-form">
        <h3>Custom Scenario</h3>
        
        <div className="form-group">
          <label>Location</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="London"
          />
        </div>

        <div className="form-group">
          <label>Event Type</label>
          <select
            value={eventType}
            onChange={(e) => setEventType(e.target.value)}
          >
            <option value="heatwave">Heatwave</option>
            <option value="flood">Flood</option>
          </select>
        </div>

        <div className="form-group">
          <label>Start Date & Time</label>
          <input
            type="datetime-local"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Duration (hours)</label>
          <input
            type="number"
            value={durationHours}
            onChange={(e) => setDurationHours(e.target.value)}
            min="1"
            max="168"
          />
        </div>

        <button type="submit" className="run-btn">
          ▶️ Run Simulation
        </button>
      </form>

      <div className="info-box">
        <p><strong>Data powered by:</strong></p>
        <p>DEG asset registry (mocked)</p>
      </div>
    </div>
  );
};

export default ScenarioPanel;


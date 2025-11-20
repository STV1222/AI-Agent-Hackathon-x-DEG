import React, { useState } from 'react';
import './App.css';
import ScenarioPanel from './components/ScenarioPanel';
import MapView from './components/MapView';
import RiskPanel from './components/RiskPanel';
import BecknLog from './components/BecknLog';

function App() {
  const [scenario, setScenario] = useState(null);
  const [risks, setRisks] = useState([]);
  const [assets, setAssets] = useState([]);
  const [mitigationPlan, setMitigationPlan] = useState(null);
  const [becknLog, setBecknLog] = useState([]);

  const API_BASE_URL = 'http://localhost:8000';

  const handleRunScenario = async (scenarioData) => {
    setScenario(scenarioData);
    try {
      const response = await fetch(`${API_BASE_URL}/scenario/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(scenarioData),
      });
      const result = await response.json();
      setAssets(result.assets || []);
      setRisks(result.risks || []);
    } catch (error) {
      console.error('Error running scenario:', error);
      alert('Failed to run scenario. Make sure backend is running.');
    }
  };

  const handleGetMitigation = async () => {
    if (!scenario || risks.length === 0) {
      alert('Please run a scenario first.');
      return;
    }
    try {
      const response = await fetch(`${API_BASE_URL}/agent/mitigate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scenario,
          risks,
          assets,
        }),
      });
      const result = await response.json();
      setMitigationPlan(result);
    } catch (error) {
      console.error('Error getting mitigation plan:', error);
      alert('Failed to get mitigation plan.');
    }
  };

  const handleExecuteBeckn = async () => {
    if (!mitigationPlan || !mitigationPlan.mitigation_actions) {
      alert('Please get mitigation plan first.');
      return;
    }
    try {
      const response = await fetch(`${API_BASE_URL}/beckn/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          actions: mitigationPlan.mitigation_actions,
        }),
      });
      const result = await response.json();
      setBecknLog(result.log || []);
    } catch (error) {
      console.error('Error executing Beckn services:', error);
      alert('Failed to execute Beckn services.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌡️ Extreme Weather Resilience Agent</h1>
        <p>AI-powered energy grid resilience on Digital Energy Grid (DEG)</p>
      </header>
      
      <div className="App-layout">
        <div className="left-panel">
          <ScenarioPanel onRunScenario={handleRunScenario} />
        </div>
        
        <div className="center-panel">
          <MapView assets={assets} risks={risks} />
        </div>
        
        <div className="right-panel">
          <RiskPanel
            risks={risks}
            mitigationPlan={mitigationPlan}
            onGetMitigation={handleGetMitigation}
            onExecuteBeckn={handleExecuteBeckn}
          />
        </div>
      </div>
      
      <div className="bottom-panel">
        <BecknLog log={becknLog} />
      </div>
    </div>
  );
}

export default App;


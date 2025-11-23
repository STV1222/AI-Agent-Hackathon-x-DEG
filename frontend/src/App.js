import React, { useState } from 'react';
import './App.css';
import ScenarioPanel from './components/ScenarioPanel';
import MapView from './components/MapView';
import RiskPanel from './components/RiskPanel';
import BecknLog from './components/BecknLog';

const STEPS = {
  SIMULATION: 'simulation',
  RISK_ASSESSMENT: 'risk_assessment',
  BECKN_NETWORK: 'beckn_network'
};

function App() {
  const [currentStep, setCurrentStep] = useState(STEPS.SIMULATION);
  const [scenario, setScenario] = useState(null);
  const [risks, setRisks] = useState([]);
  const [assets, setAssets] = useState([]);
  const [mitigationPlan, setMitigationPlan] = useState(null);
  const [becknLog, setBecknLog] = useState([]);
  const [loading, setLoading] = useState({
    scenario: false,
    mitigation: false,
    beckn: false
  });

  const API_BASE_URL = 'http://localhost:8000';

  const handleRestart = () => {
    setCurrentStep(STEPS.SIMULATION);
    setScenario(null);
    setRisks([]);
    setAssets([]);
    setMitigationPlan(null);
    setBecknLog([]);
  };

  const handleRunScenario = async (scenarioData) => {
    setLoading(prev => ({ ...prev, scenario: true }));
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
      setLoading(prev => ({ ...prev, scenario: false }));
      // Move to risk assessment step
      setTimeout(() => {
        setCurrentStep(STEPS.RISK_ASSESSMENT);
      }, 500);
    } catch (error) {
      console.error('Error running scenario:', error);
      setLoading(prev => ({ ...prev, scenario: false }));
      alert('Failed to run scenario. Make sure backend is running.');
    }
  };

  const handleGetMitigation = async () => {
    if (!scenario || risks.length === 0) {
      alert('Please run a scenario first.');
      return;
    }
    setLoading(prev => ({ ...prev, mitigation: true }));
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
      setLoading(prev => ({ ...prev, mitigation: false }));
    } catch (error) {
      console.error('Error getting mitigation plan:', error);
      setLoading(prev => ({ ...prev, mitigation: false }));
      alert('Failed to get mitigation plan.');
    }
  };

  const handleExecuteBeckn = async () => {
    if (!mitigationPlan || !mitigationPlan.mitigation_actions) {
      alert('Please get mitigation plan first.');
      return;
    }
    setLoading(prev => ({ ...prev, beckn: true }));
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
      setLoading(prev => ({ ...prev, beckn: false }));
      // Move to Beckn network step
      setTimeout(() => {
        setCurrentStep(STEPS.BECKN_NETWORK);
      }, 500);
    } catch (error) {
      console.error('Error executing Beckn services:', error);
      setLoading(prev => ({ ...prev, beckn: false }));
      alert('Failed to execute Beckn services.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div>
            <h1>🌡️ Extreme Weather Resilience Agent</h1>
            <p>AI-powered energy grid resilience on Digital Energy Grid (DEG)</p>
          </div>
          <button className="restart-btn" onClick={handleRestart}>
            <span>🔄</span>
            Restart
          </button>
        </div>
      </header>
      
      {/* Step Indicator */}
      <div className="step-indicator">
        <div className={`step ${currentStep === STEPS.SIMULATION ? 'active' : currentStep === STEPS.RISK_ASSESSMENT || currentStep === STEPS.BECKN_NETWORK ? 'completed' : ''} ${loading.scenario ? 'processing' : ''}`}>
          <div className="step-number">1</div>
          <div className="step-label">Simulation</div>
        </div>
        <div className={`step ${currentStep === STEPS.RISK_ASSESSMENT ? 'active' : currentStep === STEPS.BECKN_NETWORK ? 'completed' : ''} ${loading.mitigation ? 'processing' : ''}`}>
          <div className="step-number">2</div>
          <div className="step-label">Risk Assessment</div>
        </div>
        <div className={`step ${currentStep === STEPS.BECKN_NETWORK ? 'active' : ''} ${loading.beckn ? 'processing' : ''}`}>
          <div className="step-number">3</div>
          <div className="step-label">Beckn Network</div>
        </div>
      </div>

      {/* Global Loading Overlay */}
      {(loading.scenario || loading.mitigation || loading.beckn) && (
        <div className="global-loading-overlay">
          <div className="loading-message">
            <div className="loading-message-spinner"></div>
            <div className="loading-message-text">
              {loading.scenario && 'Running scenario simulation...'}
              {loading.mitigation && 'Generating AI mitigation plan...'}
              {loading.beckn && 'Executing Beckn network services...'}
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="main-content">
        {/* Simulation Step */}
        <div className={`step-panel ${currentStep === STEPS.SIMULATION ? 'active' : currentStep !== STEPS.SIMULATION ? 'hidden' : ''}`}>
          <div className="step-content-wrapper">
            <div className="step-panel-left">
              <ScenarioPanel 
                onRunScenario={handleRunScenario}
                loading={loading.scenario}
              />
            </div>
            <div className="step-panel-right map-panel">
              <MapView assets={assets} risks={risks} />
            </div>
          </div>
        </div>

        {/* Risk Assessment Step */}
        <div className={`step-panel ${currentStep === STEPS.RISK_ASSESSMENT ? 'active' : currentStep !== STEPS.RISK_ASSESSMENT ? 'hidden' : ''}`}>
          <div className="step-content-wrapper">
            <div className="step-panel-left">
              <RiskPanel
                risks={risks}
                mitigationPlan={mitigationPlan}
                onGetMitigation={handleGetMitigation}
                onExecuteBeckn={handleExecuteBeckn}
                loadingMitigation={loading.mitigation}
                loadingBeckn={loading.beckn}
              />
            </div>
            <div className="step-panel-right map-panel">
              <MapView assets={assets} risks={risks} />
            </div>
          </div>
        </div>

        {/* Beckn Network Step */}
        <div className={`step-panel ${currentStep === STEPS.BECKN_NETWORK ? 'active' : currentStep !== STEPS.BECKN_NETWORK ? 'hidden' : ''}`}>
          <div className="step-content-wrapper">
            <div className="step-panel-left">
              <BecknLog log={becknLog} />
            </div>
            <div className="step-panel-right map-panel">
              <MapView assets={assets} risks={risks} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;


import React from 'react';
import './RiskPanel.css';

const RiskPanel = ({ risks, mitigationPlan, onGetMitigation, onExecuteBeckn }) => {
  const getRiskBadgeClass = (level) => {
    switch (level) {
      case 'CRITICAL':
        return 'badge-critical';
      case 'HIGH':
        return 'badge-high';
      case 'MEDIUM':
        return 'badge-medium';
      case 'LOW':
        return 'badge-low';
      default:
        return 'badge-none';
    }
  };

  return (
    <div className="risk-panel">
      <h2>📊 Risk Assessment</h2>
      
      <div className="risks-section">
        <h3>Affected Assets ({risks.length})</h3>
        {risks.length === 0 ? (
          <p className="empty-state">No risks detected. Run a scenario to see results.</p>
        ) : (
          <div className="risks-list">
            {risks.map((risk, index) => (
              <div key={index} className="risk-item">
                <div className="risk-header">
                  <span className={`risk-badge ${getRiskBadgeClass(risk.risk_level)}`}>
                    {risk.risk_level}
                  </span>
                  <span className="asset-id">{risk.asset_id}</span>
                </div>
                <p className="risk-reason">{risk.reason}</p>
                <p className="risk-impact">{risk.expected_impact}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {risks.length > 0 && (
        <div className="ai-section">
          <h3>🤖 AI Mitigation Plan</h3>
          {!mitigationPlan ? (
            <button className="ai-btn" onClick={onGetMitigation}>
              Get AI Mitigation Plan
            </button>
          ) : (
            <div className="mitigation-content">
              <div className="ai-summary">
                <p>{mitigationPlan.summary_text}</p>
              </div>
              
              {mitigationPlan.mitigation_actions && mitigationPlan.mitigation_actions.length > 0 && (
                <div className="actions-list">
                  <h4>Recommended Actions</h4>
                  {mitigationPlan.mitigation_actions.map((action, index) => (
                    <div key={index} className="action-item">
                      <div className="action-header">
                        <span className="action-asset">{action.asset_id}</span>
                        <span className={`urgency-badge urgency-${action.urgency}`}>
                          {action.urgency}
                        </span>
                      </div>
                      <p className="action-type">{action.action_type}</p>
                      <p className="action-justification">{action.justification}</p>
                      <p className="action-time">Target: {new Date(action.target_time).toLocaleString()}</p>
                    </div>
                  ))}
                </div>
              )}

              {mitigationPlan.mitigation_actions && mitigationPlan.mitigation_actions.length > 0 && (
                <button className="beckn-btn" onClick={onExecuteBeckn}>
                  🚀 Execute via Beckn Network
                </button>
              )}
            </div>
          )}
        </div>
      )}

      <div className="info-box">
        <p><strong>Powered by:</strong></p>
        <p>AI Resilience Agent</p>
        <p>Beckn-compliant open network</p>
      </div>
    </div>
  );
};

export default RiskPanel;


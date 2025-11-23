import React from 'react';
import './RiskPanel.css';
import './LoadingSpinner.css';

const RiskPanel = ({ risks, mitigationPlan, onGetMitigation, onExecuteBeckn, loadingMitigation, loadingBeckn }) => {
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
      <div className="risk-panel-content">
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
            {loadingMitigation ? (
              <div className="mitigation-content">
                <div className="loading-state">
                  <div className="loading-spinner-large"></div>
                  <p>Generating AI mitigation plan...</p>
                </div>
              </div>
            ) : !mitigationPlan ? (
              <div className="mitigation-content">
                <p className="mitigation-placeholder">Click the button below to generate AI mitigation plan.</p>
              </div>
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
              </div>
            )}
          </div>
        )}
      </div>
      <div className="risk-panel-footer">
        {risks.length > 0 && (
          <div className="button-group">
            {!mitigationPlan ? (
              <button 
                className={`ai-btn ${loadingMitigation ? 'loading' : ''}`}
                onClick={onGetMitigation}
                disabled={loadingMitigation}
              >
                {loadingMitigation ? (
                  <>
                    <span className="loading-spinner"></span>
                    Processing...
                  </>
                ) : (
                  <>Get AI Mitigation Plan</>
                )}
              </button>
            ) : (
              mitigationPlan.mitigation_actions && mitigationPlan.mitigation_actions.length > 0 && (
                <button 
                  className={`beckn-btn ${loadingBeckn ? 'loading' : ''}`}
                  onClick={onExecuteBeckn}
                  disabled={loadingBeckn}
                >
                  {loadingBeckn ? (
                    <>
                      <span className="loading-spinner"></span>
                      Executing...
                    </>
                  ) : (
                    <>🚀 Execute via Beckn Network</>
                  )}
                </button>
              )
            )}
          </div>
        )}
        <div className="info-box">
          <p><strong>Powered by:</strong> AI Resilience Agent • Beckn-compliant open network</p>
        </div>
      </div>
    </div>
  );
};

export default RiskPanel;


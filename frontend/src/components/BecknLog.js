import React from 'react';
import './BecknLog.css';

const BecknLog = ({ log }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed':
        return '#48bb78';
      case 'searched':
        return '#ecc94b';
      case 'failed':
        return '#e53e3e';
      default:
        return '#cbd5e0';
    }
  };

  return (
    <div className="beckn-log">
      <h3>📡 Beckn Network Activity Log</h3>
      <div className="beckn-log-content">
        {log.length === 0 ? (
          <p className="empty-log">No Beckn network activity yet. Execute mitigation plan to see logs.</p>
        ) : (
          <div className="log-entries">
            {log.map((entry, index) => (
              <div key={index} className="log-entry" data-status={entry.status}>
                <div className="log-header">
                  <span className="log-asset">{entry.asset_id}</span>
                  <span
                    className="log-status"
                    data-status={entry.status}
                  >
                    {entry.status.toUpperCase()}
                  </span>
                </div>
                <div className="log-details">
                  <span className="log-service">{entry.service_type}</span>
                  {entry.provider && (
                    <span className="log-provider">Provider: {entry.provider}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="beckn-log-footer">
        {log.length > 0 && (
          <div className="log-info">
            <p>✅ Mitigation dispatched via Beckn-compliant open network calls</p>
          </div>
        )}
        <div className="info-box">
          <p><strong>Powered by:</strong> Beckn-compliant open network</p>
        </div>
      </div>
    </div>
  );
};

export default BecknLog;


import React from 'react';
import './FalsePositives.css';

const FalsePositives = () => (
    <div className="false-positives-container">
        <h3 className="false-header">⚠️ False Positives</h3>
        <div className="stats">
            <div className="stat-item">
                <p>🔹 <b>Daily False Alerts:</b></p>
                <span className="highlight">135</span>
            </div>

            <div className="stat-item">
                <p>🔹 <b>Whitelisting Trend:</b></p>
                <span className="highlight">⬇️ Down by 5%</span>
            </div>

            <div className="detailed-info">
                ❗ <b>Impact:</b> Increased manual review required due to recent spikes in domain variations.
            </div>
        </div>
    </div>
);

export default FalsePositives;

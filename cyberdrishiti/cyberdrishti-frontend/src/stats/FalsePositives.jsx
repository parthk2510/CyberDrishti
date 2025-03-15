import React from 'react';
import './FalsePositives.css';

const FalsePositives = () => (
    <div className="false-positives-container">
        <h3>⚠️ False Positives</h3>
        <div className="stats">
            <p>🔹 Daily False Alerts: <span>135</span></p>
            <p>🔹 Whitelisting Trend: <span>⬇️ Down by 5%</span></p>
        </div>
    </div>
);

export default FalsePositives;

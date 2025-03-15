import React from 'react';
import { FaGlobe, FaShieldAlt, FaCheckCircle, FaClock } from 'react-icons/fa';
import './DomainStatistics.css';

const DomainStatistics = () => {
    return (
        <div className="domain-stats-container">
            <h3>🌐 Domain Statistics</h3>

            <div className="stats-section total-domains">
                <h4>Total Detected Domains</h4>
                <div className="stats-item">
                    <FaClock className="icon" />
                    Last 24h: <strong>1,235</strong>
                </div>
                <div className="stats-item">
                    <FaClock className="icon" />
                    Last 7d: <strong>8,950</strong>
                </div>
                <div className="stats-item">
                    <FaClock className="icon" />
                    Last 30d: <strong>32,700</strong>
                </div>
            </div>

            <div className="stats-section status-breakdown">
                <h4>Breakdown by Status</h4>
                <div className="status-item pending">
                    <FaClock className="icon" />
                    Pending: <strong>2,000</strong>
                </div>
                <div className="status-item blocked">
                    <FaShieldAlt className="icon" />
                    Blocked: <strong>7,800</strong>
                </div>
                <div className="status-item whitelisted">
                    <FaCheckCircle className="icon" />
                    Whitelisted: <strong>500</strong>
                </div>
            </div>
        </div>
    );
};

export default DomainStatistics;

import React from 'react';
import { FaArrowUp, FaMobileAlt, FaUniversity } from 'react-icons/fa';
import './PhishingTrendCards.css';

const PhishingTrendCards = () => {
    const trends = [
        { icon: <FaArrowUp className="phishing-trend-icon" />, label: 'Phishing Websites', change: '+14%', description: 'Increase in past month' },
        { icon: <FaMobileAlt className="phishing-trend-icon" />, label: 'Mobile Phishing Attacks', change: '+9%', description: 'Rise in mobile threats' },
        { icon: <FaUniversity className="phishing-trend-icon" />, label: 'Banking Fraud Cases', change: '+6%', description: 'Targeted bank scams increased' }
    ];

    return (
        <div id="phishing-trend-cards-container">
            {trends.map((trend, index) => (
                <div key={index} className="phishing-trend-card">
                    <div className="phishing-trend-icon">{trend.icon}</div>
                    <div className="phishing-trend-info">
                        <h3>{trend.change}</h3>
                        <p>{trend.label}</p>
                        <span>{trend.description}</span>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default PhishingTrendCards;

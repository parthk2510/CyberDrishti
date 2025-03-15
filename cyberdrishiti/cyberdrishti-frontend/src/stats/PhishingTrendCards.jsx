import React from 'react';
import { FaArrowUp, FaMobileAlt, FaUniversity } from 'react-icons/fa';
import './PhishingTrendCards.css';

const PhishingTrendCards = () => {
    const trends = [
        { icon: <FaArrowUp />, label: 'Phishing Websites', change: '+14%', description: 'Increase in past month' },
        { icon: <FaMobileAlt />, label: 'Mobile Phishing Attacks', change: '+9%', description: 'Rise in mobile threats' },
        { icon: <FaUniversity />, label: 'Banking Fraud Cases', change: '+6%', description: 'Targeted bank scams increased' }
    ];

    return (
        <div className="trend-cards-container">
            {trends.map((trend, index) => (
                <div key={index} className="trend-card">
                    <div className="icon">{trend.icon}</div>
                    <div className="info">
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

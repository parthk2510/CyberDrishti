import React from 'react';
import { FaUniversity, FaPaypal, FaAmazon, FaMousePointer } from 'react-icons/fa';
import './PhishingWebsitesList.css';

const phishingWebsites = [
    { icon: <FaUniversity className="bank-icon" />, url: 'secure-banking-login.com', impersonating: 'Bank A' },
    { icon: <FaPaypal className="paypal-icon" />, url: 'paypal-verification.info', impersonating: 'PayPal' },
    { icon: <FaAmazon className="amazon-icon" />, url: 'amazon-refund.support', impersonating: 'Amazon' }
];

const clickProneWebsite = {
    icon: <FaMousePointer className="click-icon" />,
    url: 'fake-login.co',
    clicks: '12,400 clicks in the last 24 hours'
};

const PhishingWebsitesList = () => {
    return (
        <div className="phishing-websites-container">
            <h3 className="section-title">⚠️ Top 3 Phishing Websites</h3>
            <div className="website-cards">
                {phishingWebsites.map((site, index) => (
                    <div key={index} className="website-card">
                        <div className="icon">{site.icon}</div>
                        <div className="details">
                            <strong>{site.url}</strong>
                            <span>(Impersonating {site.impersonating})</span>
                        </div>
                    </div>
                ))}
            </div>

            <h3 className="section-title">🔥 Click-Prone Phishing Website</h3>
            <div className="website-card click-prone">
                <div className="icon">{clickProneWebsite.icon}</div>
                <div className="details">
                    <strong>{clickProneWebsite.url}</strong>
                    <span>{clickProneWebsite.clicks}</span>
                </div>
            </div>
        </div>
    );
};

export default PhishingWebsitesList;

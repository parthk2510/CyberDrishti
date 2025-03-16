import React from 'react';
import { FaUniversity, FaPaypal, FaAmazon, FaMousePointer } from 'react-icons/fa';
import './PhishingWebsitesList.css';

const phishingWebsites = [
    { icon: <FaUniversity />, url: 'secure-banking-login.com', impersonating: 'Bank A' },
    { icon: <FaPaypal />, url: 'paypal-verification.info', impersonating: 'PayPal' },
    { icon: <FaAmazon />, url: 'amazon-refund.support', impersonating: 'Amazon' }
];

const clickProneWebsite = {
    icon: <FaMousePointer />,
    url: 'fake-login.co',
    clicks: '12,400 clicks in the last 24 hours'
};

const PhishingWebsitesList = () => {
    return (
        <div className="phishing-websites-container">
            <h3>Top 3 Phishing Websites</h3>
            <ul className="website-list">
                {phishingWebsites.map((site, index) => (
                    <li key={index} className="website-item">
                        <div className="icon">{site.icon}</div>
                        <div className="details">
                            <strong>{site.url}</strong>
                            <span>(Impersonating {site.impersonating})</span>
                        </div>
                    </li>
                ))}
            </ul>

            <h3 className="click-prone-title">Click-Prone Phishing Website</h3>
            <div className="website-item click-prone">
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

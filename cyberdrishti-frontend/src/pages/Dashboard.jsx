import React, { useState } from 'react';
import './styles/Dashboard.css';
import DomainStatistics from '../stats/DomainStatistics';
import PhishingChart from '../stats/PhishingChart';
import PhishingWebsitesList from '../stats/PhishingWebsitesList';
import ThreatSeverityChart from '../stats/ThreatSeverityChart';
import TopTargetedBanksChart from '../stats/TopTargetedBanksChart';
import PhishingTrendChart from '../stats/PhishingTrendChart';
import FeatureImportanceChart from '../stats/FeatureImportanceChart';
import Auth from './Auth';

const Dashboard = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="dashboard-container">
            <PhishingChart />
            <PhishingWebsitesList />
            <DomainStatistics />
            <ThreatSeverityChart />
            <TopTargetedBanksChart />
            <PhishingTrendChart />
            <FeatureImportanceChart />
        </div>
    );
};

export default Dashboard;
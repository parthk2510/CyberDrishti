import React, { useState } from 'react';
import './styles/Dashboard.css';
import PhishingChart from '../stats/PhishingChart';
import PhishingTrendCards from '../stats/PhishingTrendCards';
import PhishingWebsitesList from '../stats/PhishingWebsitesList';
import DomainStatistics from '../stats/DomainStatistics';
import ThreatSeverityChart from '../stats/ThreatSeverityChart';
import TopTargetedBanksChart from '../stats/TopTargetedBanksChart';
import ResponseTimeMetrics from '../stats/ResponseTimeMetrics';
import GeoBlockingProgress from '../stats/GeoBlockingProgress';
import NonCooperativeList from '../stats/NonCooperativeList';
import PhishingTrendChart from '../stats/PhishingTrendChart';
import AttackVectorDistribution from '../stats/AttackVectorDistribution';
import Forecasting from '../stats/Forecasting';
import ModelAccuracy from '../stats/GaugeChart';
import FalsePositives from '../stats/FalsePositives';
import FeatureImportanceChart from '../stats/FeatureImportanceChart';
import Auth from './Auth';

const Dashboard = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="dashboard-container">
            <h1>Welcome to the Dashboard</h1>
            <PhishingChart />
            <PhishingTrendCards />
            <PhishingWebsitesList />
            <DomainStatistics />
            <ThreatSeverityChart />
            <TopTargetedBanksChart />
            <ResponseTimeMetrics />
            <NonCooperativeList />
            <GeoBlockingProgress />
            <PhishingTrendChart />
            <AttackVectorDistribution />
            <Forecasting />
            <ModelAccuracy />
            <FeatureImportanceChart />
            <FalsePositives />
        </div>
    );
};

export default Dashboard;

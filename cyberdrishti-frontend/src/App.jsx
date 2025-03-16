import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import CloningDetection from './pages/CloningDetection';
import WebsiteReconnaissance from './pages/WebsiteReconnaissance';
import SEORanking from './pages/SEORanking';
import ReportPage from './pages/ReportPage';
import './App.css';

const App = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    return (
        <Router>
            <Header toggleSidebar={toggleSidebar} />
            <Sidebar isOpen={sidebarOpen} />
            <div className={`content ${sidebarOpen ? 'content-expanded' : 'content-collapsed'}`}>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/cloning-detection" element={<CloningDetection />} />
                    <Route path="/website-reconnaissance" element={<WebsiteReconnaissance />} />
                    <Route path="/seo-ranking" element={<SEORanking />} />
                    <Route path="/report-page" element={<ReportPage />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;

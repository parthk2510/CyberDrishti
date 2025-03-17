import React, { useEffect, useState } from 'react';
import { FaUniversity } from 'react-icons/fa';
import './TopTargetedBanksChart.css';

const TopTargetedBanksChart = () => {
    const data = [
        { bank: 'Axis Bank', cases: 2500, color: '#e53935' },
        { bank: 'ICICI Bank', cases: 1800, color: '#f57c00' },
        { bank: 'SBI', cases: 1450, color: '#43a047' }
    ];

    const [counters, setCounters] = useState([0, 0, 0]);

    useEffect(() => {
        const interval = setInterval(() => {
            setCounters(prevCounters => prevCounters.map((count, i) =>
                count < data[i].cases ? count + Math.ceil(data[i].cases / 50) : data[i].cases
            ));
        }, 20);

        return () => clearInterval(interval);
    }, []);

    return (
        <div id="top-banks-container">
            <h3 id="top-banks-title">🏦 Top Targeted Banks</h3>
            {data.map((item, index) => (
                <div key={index} className="bank-card" style={{ borderColor: item.color }}>
                    <div className="bank-info">
                        <div className="bank-icon"><FaUniversity /></div>
                        <div className="bank-details">
                            <strong className='bank-name'>{item.bank}</strong>
                            <span>{counters[index]} Cases</span>
                        </div>
                    </div>
                    <div className="progress-bar" style={{ backgroundColor: item.color, width: `${(counters[index] / 2500) * 100}%` }}></div>
                </div>
            ))}
        </div>
    );
};

export default TopTargetedBanksChart;

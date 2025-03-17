import React, { useEffect, useState } from 'react';
import './DomainStatistics.css';

const data = [
    { status: 'Pending', value: 2000, color: '#FFA726' },
    { status: 'Blocked', value: 7800, color: '#FF5252' },
    { status: 'Whitelisted', value: 500, color: '#42A5F5' }
];

const Counter = ({ endValue, color, status }) => {
    const [count, setCount] = useState(0);

    useEffect(() => {
        const increment = Math.ceil(endValue / 100);
        const interval = setInterval(() => {
            setCount(prevCount => {
                const nextValue = prevCount + increment;
                if (nextValue >= endValue) {
                    clearInterval(interval);
                    return endValue;
                }
                return nextValue;
            });
        }, 20);

        return () => clearInterval(interval);
    }, [endValue]);

    return (
        <div className="counter-card" style={{ borderColor: color }}>
            <h3 className="counter-value" style={{ color }}>{count}</h3>
            <p className="counter-status">{status}</p>
        </div>
    );
};

const DomainStatistics = () => {
    return (
        <div id="domain-stats-container">
            <h2 id="domain-stats-title">🌐 Domain Statistics</h2>
            <div id="counter-grid">
                {data.map((item, index) => (
                    <Counter 
                        key={index} 
                        endValue={item.value} 
                        color={item.color} 
                        status={item.status} 
                    />
                ))}
            </div>
        </div>
    );
};

export default DomainStatistics;

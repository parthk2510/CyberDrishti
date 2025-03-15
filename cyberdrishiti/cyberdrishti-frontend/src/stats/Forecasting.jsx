import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './Forecasting.css';

const Forecasting = () => {
    const ringRef = useRef();
    const [counter, setCounter] = useState(0);

    useEffect(() => {
        const progress = 12; // 12% Increase
        const targetValue = 38500; // Expected phishing domains

        // Counter Animation
        const duration = 1500; 
        const step = targetValue / (duration / 10);

        const animateCounter = () => {
            let currentValue = 0;
            const interval = setInterval(() => {
                currentValue += step;
                if (currentValue >= targetValue) {
                    setCounter(targetValue);
                    clearInterval(interval);
                } else {
                    setCounter(Math.floor(currentValue));
                }
            }, 10);
        };

        animateCounter();

        // Progress Ring Animation
        const width = 200;
        const height = 200;
        const radius = Math.min(width, height) / 2;

        const svg = d3.select(ringRef.current)
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);

        const arc = d3.arc()
            .innerRadius(radius - 30)
            .outerRadius(radius)
            .startAngle(0)
            .endAngle((progress / 100) * 2 * Math.PI);

        svg.append('path')
            .attr('d', arc)
            .attr('fill', '#4CAF50')
            .transition()
            .duration(1500)
            .attrTween('d', function (d) {
                const interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, { startAngle: 0, endAngle: (progress / 100) * 2 * Math.PI });
                return function (t) {
                    return arc(interpolate(t));
                };
            });

        svg.append('text')
            .attr('x', 0)
            .attr('y', 10)
            .attr('text-anchor', 'middle')
            .text(`+${progress}%`)
            .style('fill', '#ffffff')
            .style('font-size', '20px')
            .style('font-weight', 'bold');
    }, []);

    return (
        <div className="forecast-container">
            <h3>📊 AI-Predicted Threat Forecast</h3>
            <div className="forecast-content">
                <svg ref={ringRef}></svg>
                <div className="forecast-stats">
                    <h4>Expected Phishing Domains</h4>
                    <p className="counter">{counter.toLocaleString()}</p>
                </div>
            </div>
        </div>
    );
};

export default Forecasting;

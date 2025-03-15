import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './DomainStatistics.css';

const data = [
    { timeframe: '24h', domains: 1235, change: '+5%' },
    { timeframe: '7d', domains: 8950, change: '+14%' },
    { timeframe: '30d', domains: 32700, change: '+22%' }
];

const DomainStatistics = () => {
    const chartRef = useRef();

    useEffect(() => {
        const svg = d3.select(chartRef.current)
            .attr('width', 450)
            .attr('height', 250);

        svg.selectAll('*').remove(); // Clear previous content

        data.forEach((d, index) => {
            const yPosition = 50 + index * 60;

            // Title
            svg.append('text')
                .attr('x', 20)
                .attr('y', yPosition - 10)
                .attr('class', 'chart-title')
                .text(`${d.timeframe}:`);

            // Background Bar
            svg.append('rect')
                .attr('x', 100)
                .attr('y', yPosition - 15)
                .attr('width', 300)
                .attr('height', 30)
                .attr('fill', '#333');

            // Animated Progress Bar
            svg.append('rect')
                .attr('x', 100)
                .attr('y', yPosition - 15)
                .attr('width', 0)
                .attr('height', 30)
                .attr('fill', 'url(#gradient)')
                .transition()
                .duration(1000)
                .attr('width', (d.domains / 35000) * 300);

            // Domain Value
            svg.append('text')
                .attr('x', 260)
                .attr('y', yPosition + 5)
                .attr('text-anchor', 'middle')
                .attr('class', 'chart-value')
                .text(`${d.domains}`);

            // Percentage Change Indicator
            svg.append('text')
                .attr('x', 350)
                .attr('y', yPosition + 5)
                .attr('text-anchor', 'middle')
                .attr('class', 'change-indicator')
                .text(`(${d.change})`);
        });

        // Gradient for Bar Chart
        svg.append('defs')
            .append('linearGradient')
            .attr('id', 'gradient')
            .attr('x1', '0%')
            .attr('y1', '0%')
            .attr('x2', '100%')
            .attr('y2', '0%')
            .selectAll('stop')
            .data([
                { offset: '0%', color: '#FFA726' },
                { offset: '100%', color: '#FF5252' }
            ])
            .enter().append('stop')
            .attr('offset', d => d.offset)
            .attr('stop-color', d => d.color);
    }, []);

    return (
        <div id="domain-stats-container">
            <h2 className="domain-stats-title">🌐 Domain Statistics</h2>
            <svg ref={chartRef}></svg>

            {/* Legend for Understanding */}
            <div className="legend-container">
                <div className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: '#FFA726' }}></div>
                    Moderate Growth
                </div>
                <div className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: '#FF5252' }}></div>
                    Significant Increase
                </div>
            </div>
        </div>
    );
};

export default DomainStatistics;

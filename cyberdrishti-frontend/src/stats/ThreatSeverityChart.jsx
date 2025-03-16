import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './ThreatSeverityChart.css';

const ThreatSeverityChart = () => {
    const chartRef = useRef();

    useEffect(() => {
        const data = [
            { label: 'Critical', value: 45, color: '#e53935' },
            { label: 'High', value: 30, color: '#f57c00' },
            { label: 'Medium', value: 25, color: '#43a047' }
        ];

        const width = 300;
        const height = 300;
        const radius = Math.min(width, height) / 2;

        const svg = d3.select(chartRef.current)
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);

        const pie = d3.pie().value(d => d.value);
        const arc = d3.arc().innerRadius(70).outerRadius(radius);

        svg.selectAll('path')
            .data(pie(data))
            .enter()
            .append('path')
            .attr('d', arc)
            .attr('fill', d => d.data.color)
            .transition()
            .duration(1000)
            .attrTween('d', function (d) {
                const i = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
                return function (t) {
                    return arc(i(t));
                };
            });

        svg.selectAll('text')
            .data(pie(data))
            .enter()
            .append('text')
            .attr('transform', d => `translate(${arc.centroid(d)[0] * 0.8}, ${arc.centroid(d)[1] * 0.8})`)
            .attr('text-anchor', 'middle')
            .attr('dy', '0.35em')
            .text(d => `${d.data.value}%`)
            .style('fill', '#fff')
            .style('font-weight', 'bold')
            .style('font-size', '14px');
    }, []);

    return (
        <div className="chart-container">
            <h3>🔥 Threat Severity Distribution</h3>
            <svg ref={chartRef}></svg>
            <div className="legend">
                <div className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: '#e53935' }}></div>
                    <span>Critical</span>
                </div>
                <div className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: '#f57c00' }}></div>
                    <span>High</span>
                </div>
                <div className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: '#43a047' }}></div>
                    <span>Medium</span>
                </div>
            </div>
        </div>
    );
};

export default ThreatSeverityChart;

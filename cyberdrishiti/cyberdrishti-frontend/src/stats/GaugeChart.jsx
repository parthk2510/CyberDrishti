import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './GaugeChart.css';

const GaugeChart = ({ label, value, color }) => {
    const gaugeRef = useRef();

    useEffect(() => {
        const width = 200;
        const height = 120;
        const radius = Math.min(width, height) / 2;

        const svg = d3.select(gaugeRef.current)
            .attr('width', width)
            .attr('height', height);

        const arc = d3.arc()
            .innerRadius(radius - 10)
            .outerRadius(radius)
            .startAngle(-Math.PI / 2)
            .endAngle((value / 100) * Math.PI - Math.PI / 2);

        svg.append('path')
            .attr('d', arc)
            .attr('fill', color)
            .attr('transform', `translate(${width / 2}, ${height})`);

        svg.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2 - 15)  // Raised % value text
            .attr('text-anchor', 'middle')
            .attr('id', 'gauge-value')
            .text(`${value}%`);

        svg.append('text')
            .attr('x', width / 2)
            .attr('y', height - 5)
            .attr('text-anchor', 'middle')
            .attr('id', 'gauge-label')
            .text(label);
    }, [value, color]);

    return <svg ref={gaugeRef}></svg>;
};

const ModelAccuracy = () => (
    <div id="gauge-container">
        <h3 id="gauge-title">🎯 Model Accuracy</h3>
        <div id="gauge-charts">
            <GaugeChart label="Precision" value={94.2} color="#4CAF50" />
            <GaugeChart label="Recall" value={91.8} color="#FFA726" />
        </div>
    </div>
);

export default ModelAccuracy;

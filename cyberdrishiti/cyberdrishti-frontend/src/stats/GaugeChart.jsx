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
            .attr('y', height / 2 + 10)
            .attr('text-anchor', 'middle')
            .text(`${value}%`)
            .style('fill', '#ffffff')
            .style('font-size', '20px')
            .style('font-weight', 'bold');

        svg.append('text')
            .attr('x', width / 2)
            .attr('y', height - 10)
            .attr('text-anchor', 'middle')
            .text(label)
            .style('fill', '#ffffff')
            .style('font-size', '14px');
    }, [value, color]);

    return <svg ref={gaugeRef}></svg>;
};

const ModelAccuracy = () => (
    <div className="gauge-container">
        <h3>🎯 Model Accuracy</h3>
        <div className="gauge-charts">
            <GaugeChart label="Precision" value={94.2} color="#4CAF50" />
            <GaugeChart label="Recall" value={91.8} color="#FFA726" />
        </div>
    </div>
);

export default ModelAccuracy;

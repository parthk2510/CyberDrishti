import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './GeoBlockingProgress.css';

const GeoBlockingProgress = () => {
    const circleRef = useRef();

    useEffect(() => {
        const width = 200;
        const height = 200;
        const percentage = 94;

        const svg = d3.select(circleRef.current)
            .attr('width', width)
            .attr('height', height);

        // Background circle (Grey)
        svg.append('circle')
            .attr('cx', width / 2)
            .attr('cy', height / 2)
            .attr('r', 90)
            .attr('fill', 'none')
            .attr('stroke', '#666')
            .attr('stroke-width', 15);

        // Progress Arc (Green)
        const arc = d3.arc()
            .innerRadius(70)
            .outerRadius(90)
            .startAngle(0)
            .endAngle((percentage / 100) * 2 * Math.PI);

        svg.append('path')
            .attr('d', arc)
            .attr('fill', '#4CAF50')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);

        // Percentage Text
        svg.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2 + 10)
            .attr('text-anchor', 'middle')
            .text(`${percentage}%`)
            .style('fill', '#ffffff')
            .style('font-weight', 'bold')
            .style('font-size', '24px');
    }, []);

    return (
        <div className="geo-container">
            <h3 className="geo-title">🌍 Geo-Blocking Effectiveness (India)</h3>
            <svg ref={circleRef}></svg>
        </div>
    );
};

export default GeoBlockingProgress;

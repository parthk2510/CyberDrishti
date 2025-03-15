import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './AttackVectorDistribution.css';

const AttackVectorDistribution = () => {
    const chartRef = useRef();

    useEffect(() => {
        const data = [
            { label: 'SMS Phishing', value: 40, color: '#FF5252' },   // Red for high impact
            { label: 'Fake Apps', value: 35, color: '#FFA726' },      // Orange for moderate risk
            { label: 'Cloned Websites', value: 25, color: '#4CAF50' } // Green for lower frequency
        ];

        const width = 300;
        const height = 300;
        const radius = Math.min(width, height) / 2;

        const svg = d3.select(chartRef.current)
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);

        const arc = d3.arc()
            .innerRadius(radius - 50) // Donut effect
            .outerRadius(radius);

        const pie = d3.pie()
            .value(d => d.value)
            .sort(null);

        svg.selectAll('path')
            .data(pie(data))
            .enter()
            .append('path')
            .attr('d', arc)
            .attr('fill', d => d.data.color)
            .transition()
            .duration(1000)
            .attrTween('d', function (d) {
                const interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
                return function (t) {
                    return arc(interpolate(t));
                };
            });

        svg.selectAll('text')
            .data(pie(data))
            .enter()
            .append('text')
            .attr('transform', d => `translate(${arc.centroid(d)})`)
            .attr('text-anchor', 'middle')
            .text(d => `${d.data.label}: ${d.data.value}%`)
            .style('fill', '#ffffff')
            .style('font-size', '12px')
            .style('font-weight', 'bold');
    }, []);

    return (
        <div className="attack-vector-container">
            <h3>🔎 Attack Vector Distribution</h3>
            <svg ref={chartRef}></svg>
        </div>
    );
};

export default AttackVectorDistribution;

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './FeatureImportanceChart.css';

const FeatureImportanceChart = () => {
    const chartRef = useRef();



    useEffect(() => {
        const data = [
            { feature: 'SSL mismatches', value: 35 },
            { feature: 'Domain age', value: 25 },
            { feature: 'Typosquatting patterns', value: 20 },
            { feature: 'IP reputation', value: 15 },
            { feature: 'Hosting provider reputation', value: 5 }
        ];

        const width = 800;
        const height = 300;

        const svg = d3.select(chartRef.current)
            .attr('width', width)
            .attr('height', height);

        const xScale = d3.scaleLinear()
            .domain([0, 40])
            .range([150, width - 30]);

        const yScale = d3.scaleBand()
            .domain(data.map(d => d.feature))
            .range([0, height])
            .padding(0.4);

        const gradient = svg.append('defs')
            .append('linearGradient')
            .attr('id', 'bar-gradient')
            .attr('x1', '0%')
            .attr('y1', '0%')
            .attr('x2', '100%')
            .attr('y2', '0%');

        gradient.append('stop').attr('offset', '0%').attr('stop-color', '#4CAF50');
        gradient.append('stop').attr('offset', '100%').attr('stop-color', '#FFC107');

        svg.selectAll('.bar')
            .data(data)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('x', 200)
            .attr('y', d => yScale(d.feature))
            .attr('height', yScale.bandwidth())
            .attr('width', 0) // Start bars at zero for animation
            .attr('fill', 'url(#bar-gradient)')
            .transition()
            .duration(1500)
            .attr('width', d => xScale(d.value) - 150);

        svg.selectAll('.label')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'label')
            .attr('x', d => xScale(d.value) + 5)
            .attr('y', d => yScale(d.feature) + yScale.bandwidth() / 2 + 5)
            .text(d => `${d.value}%`)
            .style('fill', '#ffffff');

        svg.selectAll('.feature-label')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'feature-label')
            .attr('x', 10)
            .attr('y', d => yScale(d.feature) + yScale.bandwidth() / 2 + 5)
            .text(d => d.feature)
            .style('fill', '#ffffff');
    }, []);

    return (
        <div className="feature-container">
            <h3 className="feature-header">🧠 Feature Importance</h3>
            <svg ref={chartRef}></svg>

        </div>
    );
};

export default FeatureImportanceChart;

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

        const width = 400;
        const height = 300;

        const svg = d3.select(chartRef.current)
            .attr('width', width)
            .attr('height', height);

        const xScale = d3.scaleLinear()
            .domain([0, 35])
            .range([0, width - 100]);

        const yScale = d3.scaleBand()
            .domain(data.map(d => d.feature))
            .range([0, height])
            .padding(0.3);

        svg.selectAll('rect')
            .data(data)
            .enter()
            .append('rect')
            .attr('x', 0)
            .attr('y', d => yScale(d.feature))
            .attr('width', d => xScale(d.value))
            .attr('height', yScale.bandwidth())
            .attr('fill', '#4CAF50');

        svg.selectAll('text')
            .data(data)
            .enter()
            .append('text')
            .attr('x', d => xScale(d.value) - 30)
            .attr('y', d => yScale(d.feature) + yScale.bandwidth() / 2 + 5)
            .text(d => `${d.value}%`)
            .style('fill', '#ffffff')
            .style('font-weight', 'bold');
    }, []);

    return (
        <div className="feature-container">
            <h3>🧠 Feature Importance</h3>
            <svg ref={chartRef}></svg>
        </div>
    );
};

export default FeatureImportanceChart;

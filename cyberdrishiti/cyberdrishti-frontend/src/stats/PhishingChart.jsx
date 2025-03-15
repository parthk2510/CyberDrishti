import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './PhishingChart.css';

const PhishingChart = () => {
    const chartRef = useRef();

    useEffect(() => {
        const data = [
            { period: 'Last 24 hours', value: 1235 },
            { period: 'Last 7 days', value: 8950 },
            { period: 'Last 30 days', value: 32700 }
        ];

        const svg = d3.select(chartRef.current)
            .attr('width', 400)
            .attr('height', 300);

        const xScale = d3.scaleBand()
            .domain(data.map(d => d.period))
            .range([0, 350])
            .padding(0.4);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)])
            .range([250, 0]);

        const chartGroup = svg.append('g').attr('transform', 'translate(30, 20)');

        chartGroup.selectAll('rect')
            .data(data)
            .enter()
            .append('rect')
            .attr('x', d => xScale(d.period))
            .attr('y', d => yScale(d.value))
            .attr('width', xScale.bandwidth())
            .attr('height', d => 250 - yScale(d.value))
            .attr('fill', '#4CAF50');

        chartGroup.selectAll('text')
            .data(data)
            .enter()
            .append('text')
            .attr('x', d => xScale(d.period) + xScale.bandwidth() / 2)
            .attr('y', d => yScale(d.value) - 5)
            .attr('text-anchor', 'middle')
            .attr('fill', '#ffffff')
            .text(d => d.value);

        svg.append('g')
            .attr('transform', 'translate(30, 270)')
            .call(d3.axisBottom(xScale));

        svg.append('g')
            .attr('transform', 'translate(30, 20)')
            .call(d3.axisLeft(yScale).ticks(5));
    }, []);

    return (
        <div className="phishing-chart-container">
            <h3>No. of Phishing Websites Detected</h3>
            <svg ref={chartRef}></svg>
        </div>
    );
};

export default PhishingChart;

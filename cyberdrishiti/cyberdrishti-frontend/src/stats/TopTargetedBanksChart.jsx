import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './TopTargetedBanksChart.css';

const TopTargetedBanksChart = () => {
    const chartRef = useRef();

    useEffect(() => {
        const data = [
            { bank: 'Bank A', cases: 2500, color: '#e53935' }, // Red for highest threat
            { bank: 'Bank B', cases: 1800, color: '#f57c00' }, // Orange for medium threat
            { bank: 'Bank C', cases: 1450, color: '#43a047' }  // Green for lower threat
        ];

        const width = 400;
        const height = 300;
        const margin = { top: 30, right: 30, bottom: 40, left: 100 };

        const svg = d3.select(chartRef.current)
            .attr('width', width)
            .attr('height', height);

        const xScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.cases)])
            .range([0, width - margin.left - margin.right]);

        const yScale = d3.scaleBand()
            .domain(data.map(d => d.bank))
            .range([0, height - margin.top - margin.bottom])
            .padding(0.3);

        const chart = svg.append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);

        // Bars
        chart.selectAll('.bar')
            .data(data)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('y', d => yScale(d.bank))
            .attr('height', yScale.bandwidth())
            .attr('width', 0)
            .attr('fill', d => d.color)
            .transition()
            .duration(1000)
            .attr('width', d => xScale(d.cases));

        // Data Labels Inside Bars
        chart.selectAll('.label')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'label')
            .attr('y', d => yScale(d.bank) + yScale.bandwidth() / 2)
            .attr('x', d => xScale(d.cases) - 40)
            .attr('dy', '0.35em')
            .attr('fill', '#ffffff')
            .text(d => `${d.cases}`);

        // Bank Names (Ensuring All Data Visible)
        chart.selectAll('.bank-label')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'bank-label')
            .attr('x', -10)
            .attr('y', d => yScale(d.bank) + yScale.bandwidth() / 2)
            .attr('dy', '0.35em')
            .attr('text-anchor', 'end')
            .attr('fill', '#ffffff')
            .text(d => d.bank);
    }, []);

    return (
        <div id="chart-container">
            <h3 id="chart-title">Top Targeted Banks (Phishing Cases)</h3>
            <svg ref={chartRef}></svg>
        </div>
    );
};

export default TopTargetedBanksChart;

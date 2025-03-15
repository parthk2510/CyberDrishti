import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './PhishingTrendChart.css';

const PhishingTrendChart = () => {
    const chartRef = useRef();

    useEffect(() => {
        const data = [
            { year: '2022', attempts: 3200 },
            { year: '2023', attempts: 5400 },
            { year: '2024', attempts: 6800 }
        ];

        const width = 400;
        const height = 300;
        const margin = { top: 20, right: 20, bottom: 40, left: 60 };

        const svg = d3.select(chartRef.current)
            .attr('width', width)
            .attr('height', height);

        const xScale = d3.scalePoint()
            .domain(data.map(d => d.year))
            .range([0, width - margin.left - margin.right]);

        const yScale = d3.scaleLinear()
            .domain([3000, 7000])
            .range([height - margin.top - margin.bottom, 0]);

        const chart = svg.append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);

        const line = d3.line()
            .x(d => xScale(d.year))
            .y(d => yScale(d.attempts));

        chart.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', '#4CAF50')
            .attr('stroke-width', 3)
            .attr('d', line);

        chart.selectAll('.dot')
            .data(data)
            .enter()
            .append('circle')
            .attr('class', 'dot')
            .attr('cx', d => xScale(d.year))
            .attr('cy', d => yScale(d.attempts))
            .attr('r', 5)
            .attr('fill', '#4CAF50');
    }, []);

    return (
        <div className="trend-container">
            <h3>📈 Phishing Attempts (Last 3 Years)</h3>
            <svg ref={chartRef}></svg>
        </div>
    );
};

export default PhishingTrendChart;

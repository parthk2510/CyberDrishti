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

        const width = 450;
        const height = 350;
        const margin = { top: 20, right: 20, bottom: 60, left: 70 };

        const svg = d3.select(chartRef.current)
            .attr('id', 'phishing-trend-chart')
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
            .attr('stroke-width', 4)
            .attr('d', line);

        chart.selectAll('.phishing-trend-dot')
            .data(data)
            .enter()
            .append('circle')
            .attr('class', 'phishing-trend-dot')
            .attr('cx', d => xScale(d.year))
            .attr('cy', d => yScale(d.attempts))
            .attr('r', 8);

        chart.selectAll('.data-label')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'data-label')
            .attr('x', d => xScale(d.year))
            .attr('y', d => yScale(d.attempts) - 10)
            .attr('text-anchor', 'middle')
            .text(d => d.attempts)
            .style('fill', '#ffffff')
            .style('font-weight', 'bold');

        // X-Axis
        chart.append('g')
            .attr('transform', `translate(0, ${height - margin.top - margin.bottom})`)
            .call(d3.axisBottom(xScale));

        // X-Axis Label
        chart.append('text')
            .attr('class', 'axis-label')
            .attr('x', (width - margin.left - margin.right) / 2)
            .attr('y', height - margin.bottom + 30)
            .text('Year')
            .style('fill', '#ffffff');

        // Y-Axis
        chart.append('g')
            .call(d3.axisLeft(yScale).ticks(5).tickSize(-width + margin.left + margin.right));

        // Y-Axis Label
        chart.append('text')
            .attr('class', 'axis-label')
            .attr('transform', 'rotate(-90)')
            .attr('x', -(height / 2))
            .attr('y', -50)
            .attr('text-anchor', 'middle')
            .text('Phishing Attempts')
            .style('fill', '#ffffff');
    }, []);

    return (
        <div id="phishing-trend-container">
            <h3 id="phishing-trend-title">📈 Phishing Attempts (Last 3 Years)</h3>
            <svg ref={chartRef}></svg>
        </div>
    );
};

export default PhishingTrendChart;

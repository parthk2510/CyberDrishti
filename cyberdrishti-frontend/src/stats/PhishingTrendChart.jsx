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

        const gradient = svg.append('defs')
            .append('linearGradient')
            .attr('id', 'line-gradient')
            .attr('gradientUnits', 'userSpaceOnUse')
            .attr('x1', 0).attr('y1', 0)
            .attr('x2', width).attr('y2', 0);

        gradient.append('stop')
            .attr('offset', '0%')
            .attr('stop-color', '#4CAF50');
        gradient.append('stop')
            .attr('offset', '100%')
            .attr('stop-color', '#FF5722');

        const line = d3.line()
            .x(d => xScale(d.year))
            .y(d => yScale(d.attempts));

        chart.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', 'url(#line-gradient)')
            .attr('stroke-width', 4)
            .attr('d', line)
            .attr('stroke-dasharray', 450)
            .attr('stroke-dashoffset', 450)
            .transition()
            .duration(1500)
            .attr('stroke-dashoffset', 0);

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
            .attr('y', d => yScale(d.attempts) - 15)
            .text(d => `${d.attempts}`)
            .style('opacity', 0)
            .transition()
            .delay((d, i) => i * 500)
            .duration(1000)
            .style('opacity', 1);

        // X-Axis
        chart.append('g')
            .attr('transform', `translate(0, ${height - margin.top - margin.bottom})`)
            .call(d3.axisBottom(xScale));

        // Y-Axis
        chart.append('g')
            .call(d3.axisLeft(yScale).ticks(5));
    }, []);

    return (
        <div id="phishing-trend-container">
            <h3 id="phishing-trend-title">📈 Phishing Attempts (Last 3 Years)</h3>
            <svg ref={chartRef}></svg>
        </div>
    );
};

export default PhishingTrendChart;

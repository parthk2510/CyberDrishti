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
            .attr('id', 'phishing-chart-svg')
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

        // Tooltip Setup
        const tooltip = d3.select('#phishing-chart-container')
            .append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0);

        // Animated Bars with Dynamic Colors
        chartGroup.selectAll('.phishing-bar')
            .data(data)
            .enter()
            .append('rect')
            .attr('class', d => {
                if (d.value < 3000) return 'phishing-bar low';
                if (d.value < 10000) return 'phishing-bar medium';
                return 'phishing-bar high';
            })
            .attr('x', d => xScale(d.period))
            .attr('y', 250)
            .attr('width', xScale.bandwidth())
            .attr('height', 0)
            .on('mouseover', (event, d) => {
                tooltip.transition().duration(200).style('opacity', 1);
                tooltip.html(`${d.period}: ${d.value} sites`)
                    .style('left', `${event.pageX + 10}px`)
                    .style('top', `${event.pageY - 20}px`);
            })
            .on('mouseout', () => tooltip.transition().duration(200).style('opacity', 0))
            .transition()
            .duration(1000)
            .attr('y', d => yScale(d.value))
            .attr('height', d => 250 - yScale(d.value));

        // Value Display
        chartGroup.selectAll('.phishing-bar-value')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'phishing-bar-value')
            .attr('x', d => xScale(d.period) + xScale.bandwidth() / 2)
            .attr('y', 250)
            .attr('text-anchor', 'middle')
            .transition()
            .delay(800)
            .duration(500)
            .attr('y', d => yScale(d.value) - 5)
            .text(d => d.value);

        // Axis Animations
        svg.append('g')
            .attr('id', 'phishing-chart-axis')
            .attr('transform', 'translate(30, 270)')
            .call(d3.axisBottom(xScale));

        svg.append('g')
            .attr('id', 'phishing-chart-axis')
            .attr('transform', 'translate(30, 20)')
            .transition()
            .duration(1000)
            .call(d3.axisLeft(yScale).ticks(5));
    }, []);

    return (
        <div id="phishing-chart-container">
            <h3 className="phishing-chart-title">No. of Phishing Websites Detected</h3>
            <svg ref={chartRef}></svg>
        </div>
    );
};

export default PhishingChart;

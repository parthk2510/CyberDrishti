import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './FeatureImportanceChart.css';

const FeatureImportanceChart = () => {
    const chartRef = useRef();

    const dataDetails = [
        { feature: 'SSL mismatches', description: 'Certificates that fail SSL checks are common in phishing attempts.' },
        { feature: 'Domain age', description: 'Recently registered domains have higher phishing risk.' },
        { feature: 'Typosquatting patterns', description: 'Domain names resembling legitimate services indicate impersonation.' },
        { feature: 'IP reputation', description: 'IPs linked to malicious activities are flagged.' },
        { feature: 'Hosting provider reputation', description: 'Providers with minimal security protocols often host phishing sites.' }
    ];

    useEffect(() => {
        const data = [
            { feature: 'SSL mismatches', value: 35 },
            { feature: 'Domain age', value: 25 },
            { feature: 'Typosquatting patterns', value: 20 },
            { feature: 'IP reputation', value: 15 },
            { feature: 'Hosting provider reputation', value: 5 }
        ];

        const width = 500;
        const height = 300;

        const svg = d3.select(chartRef.current)
            .attr('width', width)
            .attr('height', height);

        const xScale = d3.scaleLinear()
            .domain([0, 40])
            .range([150, width - 30]);  // Shifted start to create label space

        const yScale = d3.scaleBand()
            .domain(data.map(d => d.feature))
            .range([0, height])
            .padding(0.4);

        const colorScale = d3.scaleOrdinal()
            .domain(data.map(d => d.feature))
            .range(['#4CAF50', '#2196F3', '#FFC107', '#FF5722', '#9C27B0']);

        svg.selectAll('.bar')
            .data(data)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('x', 150)  // Starting bars after labels
            .attr('y', d => yScale(d.feature))
            .attr('width', d => xScale(d.value) - 150)
            .attr('height', yScale.bandwidth())
            .attr('fill', d => colorScale(d.feature));

        svg.selectAll('.label')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'label')
            .attr('x', d => xScale(d.value) + 5)
            .attr('y', d => yScale(d.feature) + yScale.bandwidth() / 2 + 5)
            .text(d => `${d.value}%`)
            .style('fill', '#ffffff')
            .style('font-weight', 'bold');

        svg.selectAll('.feature-label')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'feature-label')
            .attr('x', 10)  // Position labels separately on the left
            .attr('y', d => yScale(d.feature) + yScale.bandwidth() / 2 + 5)
            .text(d => d.feature)
            .style('fill', '#ffffff')
            .style('text-anchor', 'start')
            .style('font-weight', 'bold');
    }, []);

    return (
        <div className="feature-container">
            <h3 className="feature-header">🧠 Feature Importance</h3>
            <svg ref={chartRef}></svg>

            <div className="data-details">
                <h4>📊 Data Insights</h4>
                <ul>
                    {dataDetails.map((item, index) => (
                        <li key={index}>
                            <strong>{item.feature}:</strong> {item.description}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default FeatureImportanceChart;

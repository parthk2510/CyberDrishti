import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './ResponseTimeMetrics.css';

const ResponseTimeMetrics = () => {
    const gaugeRef = useRef();
    const barChartRef = useRef();

    useEffect(() => {
        // Gauge Chart (Detection-to-Takedown Time)
        const gaugeData = [
            { label: 'Current', value: 4.2, color: '#4CAF50' },
            { label: 'Historical Avg', value: 6.5, color: '#f57c00' }
        ];

        const gaugeWidth = 300;
        const gaugeHeight = 150;

        const gaugeSvg = d3.select(gaugeRef.current)
            .attr('width', gaugeWidth)
            .attr('height', gaugeHeight);

        const arc = d3.arc()
            .innerRadius(40)
            .outerRadius(70)
            .startAngle(0)
            .cornerRadius(6);

        gaugeSvg.selectAll('path')
            .data(gaugeData)
            .enter()
            .append('path')
            .attr('d', (d) => arc({ endAngle: (d.value / 10) * Math.PI }))
            .attr('fill', (d) => d.color)
            .attr('transform', `translate(${gaugeWidth / 2}, ${gaugeHeight / 2})`);

        gaugeSvg.selectAll('text')
            .data(gaugeData)
            .enter()
            .append('text')
            .attr('class', 'gauge-label')
            .attr('x', gaugeWidth / 2)
            .attr('y', (d, i) => 80 + i * 20)
            .attr('text-anchor', 'middle')
            .text((d) => `${d.label}: ${d.value} hrs`);

        // Bar Chart (Registrar-Wise Takedown Success Rates)
        const registrarData = [
            { registrar: 'GoDaddy', successRate: 92, color: '#4CAF50' },
            { registrar: 'Namecheap', successRate: 85, color: '#f57c00' },
            { registrar: 'Google Domains', successRate: 78, color: '#e53935' }
        ];

        const barWidth = 350;
        const barHeight = 200;
        const margin = { top: 20, right: 30, bottom: 40, left: 100 };

        const xScale = d3.scaleLinear()
            .domain([0, 100])
            .range([0, barWidth - margin.left - margin.right]);

        const yScale = d3.scaleBand()
            .domain(registrarData.map((d) => d.registrar))
            .range([0, barHeight - margin.top - margin.bottom])
            .padding(0.3);

        const barSvg = d3.select(barChartRef.current)
            .attr('width', barWidth)
            .attr('height', barHeight);

        const barGroup = barSvg.append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);

        barGroup.selectAll('.bar')
            .data(registrarData)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('y', (d) => yScale(d.registrar))
            .attr('height', yScale.bandwidth())
            .attr('width', 0)
            .attr('fill', (d) => d.color)
            .transition()
            .duration(1000)
            .attr('width', (d) => xScale(d.successRate));

        barGroup.selectAll('.label')
            .data(registrarData)
            .enter()
            .append('text')
            .attr('class', 'bar-label')
            .attr('y', (d) => yScale(d.registrar) + yScale.bandwidth() / 2)
            .attr('x', (d) => xScale(d.successRate) - 30)
            .attr('dy', '0.35em')
            .attr('fill', '#ffffff')
            .text((d) => `${d.successRate}%`);
    }, []);

    return (
        <div className="metrics-container">
            <h3 className="metrics-header">Response Time Metrics</h3>

            <div className="chart-wrapper">
                <h4>Average Detection-to-Takedown Time</h4>
                <svg ref={gaugeRef}></svg>
                <p className="details-text">
                    📋 <b>Current Time:</b> 4.2 hrs<br />
                    🕒 <b>Historical Avg:</b> 6.5 hrs
                </p>
            </div>

            <div className="chart-wrapper">
                <h4>Registrar-Wise Takedown Success Rates</h4>
                <svg ref={barChartRef}></svg>
                <p className="details-text">
                    ✅ <b>GoDaddy:</b> 92%<br />
                    ⚠️ <b>Namecheap:</b> 85%<br />
                    🚫 <b>Google Domains:</b> 78%
                </p>
            </div>
        </div>
    );
};

export default ResponseTimeMetrics;

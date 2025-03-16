import React from 'react';
import { FaGlobe, FaBan } from 'react-icons/fa';
import './NonCooperativeList.css';

const NonCooperativeList = () => {
    const countries = ['Russia', 'China', 'Nigeria', 'Brazil'];

    return (
        <div className="non-cooperative-container">
            <h3>🚨 Non-Cooperative Countries/Registrars</h3>
            <ul>
                {countries.map((country, index) => (
                    <li key={index}>
                        <FaBan className="icon" /> {country}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default NonCooperativeList;

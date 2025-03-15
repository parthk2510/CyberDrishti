import React, { useState } from 'react';
import './styles/CloneDetection.css';

const CloneDetection = () => {
    const [originalURL, setOriginalURL] = useState('');
    const [copyURL, setCopyURL] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        alert('Submitted for analysis!');
    };

    return (
        <div className="clone-detection-container">
            <h2 className="clone-heading">🕵️‍♂️ Clone Detection Tool</h2>
            <p className="clone-description">
                Enter the URLs of the original and suspected copy for similarity analysis.
            </p>

            <form onSubmit={handleSubmit} className="clone-form">
                <div className="input-group">
                    <label htmlFor="original" className="input-label">Original Webpage URL:</label>
                    <input
                        type="url"
                        id="original"
                        value={originalURL}
                        onChange={(e) => setOriginalURL(e.target.value)}
                        required
                    />
                </div>

                <div className="input-group">
                    <label htmlFor="copy" className="input-label">Suspected Copy URL:</label>
                    <input
                        type="url"
                        id="copy"
                        value={copyURL}
                        onChange={(e) => setCopyURL(e.target.value)}
                        required
                    />
                </div>

                <button type="submit" className="clone-submit-btn">🔍 Detect Similarity</button>
            </form>
        </div>
    );
};

export default CloneDetection;

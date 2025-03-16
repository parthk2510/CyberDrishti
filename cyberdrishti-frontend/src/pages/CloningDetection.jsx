import React, { useState } from 'react';
import './styles/CloneDetection.css';

const CloneDetection = () => {
  const [originalURL, setOriginalURL] = useState('');
  const [copyURL, setCopyURL] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('original_url', originalURL);
      formData.append('phishing_url', copyURL);

      const response = await fetch('/api/ui-similarity/', {
        method: 'POST',
        body: formData,
      });

      let data;
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        data = await response.json();
      } else {
        const text = await response.text();
        throw new Error(text || 'Request failed with no response body');
      }

      if (!response.ok) {
        throw new Error(data.error || 'Request failed');
      }
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
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

        <button type="submit" className="clone-submit-btn" disabled={loading}>
          {loading ? 'Analyzing...' : '🔍 Detect Similarity'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}
      {result && (
        <div className="result-container">
          <h3>Results:</h3>
          <p>Original URL: {result.original_url}</p>
          <p>Suspected Copy URL: {result.phishing_url}</p>
          <p>Similarity Percentage: {result.similarity_percentage.toFixed(2)}%</p>
          <p>Message: {result.message}</p>
        </div>
      )}
    </div>
  );
};

export default CloneDetection;

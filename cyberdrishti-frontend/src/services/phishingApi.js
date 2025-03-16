const API_BASE_URL = 'http://localhost:8000/api';

export const phishingApi = {
    analyzeUrl: async (url) => {
        try {
            const response = await fetch(`${API_BASE_URL}/analyze-phishing/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });
            
            if (!response.ok) {
                throw new Error('Analysis failed');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error analyzing URL:', error);
            throw error;
        }
    },
    
    getRecentAnalyses: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/recent-analyses/`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch recent analyses');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching recent analyses:', error);
            throw error;
        }
    },
    
    getDomainDetails: async (domainId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/domain-details/${domainId}/`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch domain details');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching domain details:', error);
            throw error;
        }
    }
}; 
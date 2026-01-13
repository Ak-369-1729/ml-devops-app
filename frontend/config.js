// API Configuration - Update this with your backend URL
const API_BASE = process.env.REACT_APP_API_BASE || 
                 (window.location.hostname === 'localhost' 
                   ? 'http://localhost:5000' 
                   : 'https://your-railway-backend.up.railway.app');

// Export for use in other scripts
window.API_CONFIG = { API_BASE };

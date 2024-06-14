import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    withHeaders: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Access-Control-Allow-Methods': 'GET,POST',
        'Access-Control-Allow-Origin': '*',
        // 'Access-Control-Allow-Credentials': 'true',
        // 'Access-Control-Allow-Headers': '*',
        // 'Access-Control-Expose-Headers': '*',
    },
    
});

export default api; 
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();

app.use(cors());
app.use(express.json());

// Serve static files from current directory
app.use(express.static(path.join(__dirname)));

// Root route - serve taskpane.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'taskpane.html'));
});

// Proxy to Flask backend
app.post('/fetch_financials', async (req, res) => {
    try {
        const response = await fetch('http://localhost:5000/fetch_financials', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(req.body)
        });
        
        const data = await response.json();
        res.json(data);
    } catch (err) {
        res.status(500).json({
            success: false,
            error: `Backend error: ${err.message}`
        });
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`✅ Add-in server running on https://localhost:${PORT}`);
    console.log(`⚠️  Make sure Flask backend is running on http://localhost:5000`);
});

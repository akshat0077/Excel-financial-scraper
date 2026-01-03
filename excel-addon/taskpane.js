Office.onReady((info) => {
    if (info.host === Office.HostType.Excel) {
        console.log('Excel Add-in ready');
    }
});

async function insertData() {
    const ticker = document.getElementById('ticker').value.trim().toUpperCase();
    const years = parseInt(document.getElementById('years').value);
    
    const metrics = Array.from(document.querySelectorAll('.metric-checkboxes input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    const statusDiv = document.getElementById('status');
    statusDiv.className = 'status';
    statusDiv.textContent = 'Fetching data...';
    
    if (!ticker || !years || metrics.length === 0) {
        statusDiv.className = 'status error';
        statusDiv.textContent = '❌ Please fill all fields and select metrics';
        return;
    }
    
    try {
        // Fetch from Flask backend
        const response = await fetch('http://localhost:5000/fetch_financials', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker, metrics, years })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error);
        }
        
        // Insert into Excel
        await Excel.run(async (context) => {
            const sheet = context.application.activeWorksheet;
            
            // Clear previous data (A1:Z50)
            sheet.getRange("A1:Z50").clear();
            
            // Add title
            const titleCell = sheet.getRange("A1");
            titleCell.values = [[`${ticker} Financial Data`]];
            titleCell.format.font.bold = true;
            titleCell.format.font.size = 14;
            
            // Add headers
            const headers = ["Year", ...metrics];
            const headerRange = sheet.getRange("A3");
            headerRange.values = [headers];
            headerRange.format.font.bold = true;
            headerRange.format.fill.color = "#f5f5f5";
            
            // Add data rows
            const rows = result.data.map(row => [
                row.year,
                ...metrics.map(m => row[m] !== null ? row[m] : "N/A")
            ]);
            
            if (rows.length > 0) {
                const dataRange = sheet.getRange(`A4:${String.fromCharCode(65 + metrics.length - 1)}${rows.length + 3}`);
                dataRange.values = rows;
            }
            
            // Auto-fit columns
            sheet.getRange("A:Z").format.autofitColumn();
            
            await context.sync();
        });
        
        statusDiv.className = 'status success';
        statusDiv.textContent = `✅ Data inserted for ${ticker}!`;
        
    } catch (err) {
        statusDiv.className = 'status error';
        statusDiv.textContent = `❌ Error: ${err.message}`;
        console.error(err);
    }
}

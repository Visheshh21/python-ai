// Initialize Lucide icons
lucide.createIcons();

const runBtn = document.getElementById('runBtn');
const callLimit = document.getElementById('callLimit');
const loader = document.getElementById('loader');

    // Elements to populate
const metricTotal = document.getElementById('metricTotal');
const metricDefectRate = document.getElementById('metricDefectRate');
const metricEscalations = document.getElementById('metricEscalations');
const markdownContent = document.getElementById('markdownContent');
const callsTableBody = document.querySelector('#callsTable tbody');
const progressText = document.getElementById('progressText');

let progressInterval;

runBtn.addEventListener('click', async () => {
    const limit = parseInt(callLimit.value) || 5;
    
    // UI Loading State
    runBtn.disabled = true;
    loader.classList.remove('hidden');
    progressText.textContent = "Connecting...";
    
    // Start polling progress
    progressInterval = setInterval(async () => {
        try {
            let res = await fetch('/api/progress');
            let prog = await res.json();
            if (prog.total > 0) {
                progressText.textContent = `Analyzed call ${prog.current} / ${prog.total}`;
            }
        } catch (e) {}
    }, 500);
    metricTotal.textContent = '--';
    metricDefectRate.textContent = '--';
    metricEscalations.textContent = '--';
    markdownContent.innerHTML = `
        <div class="empty-state">
            <div class="spinner"></div>
            <p>Generating report...</p>
        </div>
    `;
    callsTableBody.innerHTML = '';

    try {
        const response = await fetch('/api/audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ limit: limit })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const data = await response.json();
        
        // 1. Populate Metrics based on the returned CSV data
        const total = data.calls.length;
        let defectCount = 0;
        let escalationsCount = 0;

        data.calls.forEach(call => {
            if (call.category && !call.category.includes('Normal')) {
                defectCount++;
            }
            if (call.sentiment === 'Frustrated' || call.sentiment === 'Angry' || call.resolution === 'Escalated') {
                escalationsCount++;
            }
        });

        metricTotal.textContent = total;
        metricDefectRate.textContent = total > 0 ? Math.round((defectCount / total) * 100) + '%' : '0%';
        metricEscalations.textContent = escalationsCount;

        // 2. Render Markdown Report
        if (data.summary) {
            // marked.js converts the markdown string to HTML
            markdownContent.innerHTML = marked.parse(data.summary);
        }

        // 3. Populate Table
        if (data.calls && data.calls.length > 0) {
            data.calls.forEach(call => {
                const tr = document.createElement('tr');
                
                const isNormal = call.category && call.category.includes('Normal');
                const badgeClass = isNormal ? 'badge normal' : 'badge defect';

                tr.innerHTML = `
                    <td><small>${call.call_id ? call.call_id.substring(0, 8) + '...' : 'N/A'}</small></td>
                    <td><span class="${badgeClass}">${call.category || 'Unknown'}</span></td>
                    <td>${call.sentiment || '-'}</td>
                    <td>${call.summary || '-'}</td>
                `;
                callsTableBody.appendChild(tr);
            });
        } else {
            callsTableBody.innerHTML = `<tr><td colspan="4" style="text-align:center;">No calls processed.</td></tr>`;
        }

    } catch (error) {
        console.error("Audit failed:", error);
        markdownContent.innerHTML = `
            <div class="empty-state" style="color: var(--accent-red)">
                <i data-lucide="alert-triangle"></i>
                <p>Failed to run audit. See console for details.</p>
                <p><small>${error.message}</small></p>
            </div>
        `;
        lucide.createIcons();
    } finally {
        clearInterval(progressInterval);
        runBtn.disabled = false;
        loader.classList.add('hidden');
    }
});

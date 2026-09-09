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
let globalCallsData = [];
let globalSummaryMarkdown = "";

async function loadDealerships() {
    try {
        const res = await fetch('/api/dealerships');
        const dships = await res.json();
        const container = document.getElementById('dealershipCheckboxes');
        dships.forEach(d => {
            const label = document.createElement('label');
            const cb = document.createElement('input');
            cb.type = 'checkbox';
            cb.value = d;
            cb.className = 'dealership-cb';
            
            label.appendChild(cb);
            label.appendChild(document.createTextNode(' ' + d));
            container.appendChild(label);
        });
    } catch(e) { console.error("Failed to load dealerships", e); }
}
document.addEventListener('DOMContentLoaded', loadDealerships);

// Close dropdown when clicking outside
document.addEventListener('click', function(e) {
    if (!e.target.closest('.custom-multiselect')) {
        const dropdown = document.getElementById('dealershipCheckboxes');
        if (dropdown) dropdown.classList.remove('show');
    }
});

runBtn.addEventListener('click', async () => {
    const limitVal = parseInt(callLimit.value);
    const limit = isNaN(limitVal) ? null : limitVal;
    
    // Gather checked dealerships
    const cbs = document.querySelectorAll('.dealership-cb:checked');
    const dealerships = Array.from(cbs).map(cb => cb.value);
    
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const customCategories = document.getElementById('customCategories').value || "Normal / No Issue";
    
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
            body: JSON.stringify({ 
                limit: limit,
                dealerships: dealerships,
                start_date: startDate ? startDate : null,
                end_date: endDate ? endDate : null,
                custom_categories: customCategories
            })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const data = await response.json();
        
        globalCallsData = data.calls || [];
        globalSummaryMarkdown = data.summary || "";
        
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
                    <td>${call.agent_name || '-'}</td>
                    <td><span class="${badgeClass}">${call.category || 'Unknown'}</span></td>
                    <td>${call.sentiment || '-'}</td>
                    <td><div style="max-height: 150px; overflow-y: auto;">${call.summary || '-'}</div></td>
                    <td><div style="max-height: 150px; overflow-y: auto; font-size: 0.85rem; background: var(--bg-dark); padding: 8px; border-radius: 4px; border: 1px solid var(--border-color); white-space: pre-wrap;">${call.transcript || '-'}</div></td>
                `;
                callsTableBody.appendChild(tr);
            });
        } else {
            callsTableBody.innerHTML = `<tr><td colspan="6" style="text-align:center;">No calls processed.</td></tr>`;
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

// Export Handlers
document.getElementById('exportCsvBtn').addEventListener('click', () => {
    if (!globalCallsData || globalCallsData.length === 0) return alert("No data to export");
    const headers = Object.keys(globalCallsData[0]);
    const csvContent = [
        headers.join(","),
        ...globalCallsData.map(row => headers.map(fieldName => JSON.stringify(row[fieldName] || "")).join(","))
    ].join("\n");
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "audit_calls.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

document.getElementById('exportPdfBtn').addEventListener('click', () => {
    if (!globalSummaryMarkdown) return alert("No summary to export");
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Strip basic markdown formatting for simple PDF text
    const cleanText = globalSummaryMarkdown.replace(/[*_]/g, '').replace(/#/g, '');
    const splitText = doc.splitTextToSize(cleanText, 180);
    
    doc.setFont("helvetica");
    doc.setFontSize(11);
    
    // Handle pagination if text is very long
    let y = 15;
    for (let i = 0; i < splitText.length; i++) {
        if (y > 280) {
            doc.addPage();
            y = 15;
        }
        doc.text(splitText[i], 15, y);
        y += 6;
    }
    
    doc.save("executive_summary.pdf");
});

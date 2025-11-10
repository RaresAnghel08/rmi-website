/* Admin dashboard JS moved out of inline HTML to avoid template literal </script> pitfalls */
/* eslint-disable no-template-curly-in-string */
// Global data storage
let resultsData = { headers: [], rows: [] };
let teamsData = { headers: [], rows: [] };

// Tab switching
function switchTab(tabName, ev) {
  if (ev && ev.target) {
    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
    ev.target.classList.add('active');
  }
  document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
  document.getElementById(tabName + '-tab').classList.add('active');
}

// CSV Parsing
function parseCSV(text) {
  const lines = text.split('\n').filter(line => line.trim());
  const headers = lines[0].split(',').map(h => h.trim());
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);
    if (values.length > 0) rows.push(values);
  }
  return { headers, rows };
}

function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    if (char === '"') inQuotes = !inQuotes;
    else if (char === ',' && !inQuotes) { result.push(current.trim()); current = ''; }
    else current += char;
  }
  result.push(current.trim());
  return result;
}

// Results CSV handling
function loadResultsCSV(event) {
  const file = event.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    const text = e.target.result;
    resultsData = parseCSV(text);
    displayResults();
    updateStatistics();
  };
  reader.readAsText(file);
}

function displayResults() {
  const container = document.getElementById('results-content');
  if (resultsData.rows.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No data to display</p></div>';
    return;
  }
  let html = '<input type="text" class="search-box" placeholder="🔍 Search by name, country, or rank..." onkeyup="filterResults(this.value)">';
  html += '<div class="btn-group">';
  html += '<button class="btn btn-success" onclick="downloadCSV(resultsData, \'results.csv\')"><span>💾</span> Download CSV</button>';
  html += '<button class="btn btn-primary" onclick="generateResultsHTML()"><span>📄</span> Generate results.html</button>';
  html += '<button class="btn btn-primary add-row-btn" onclick="addResultRow()"><span>➕</span> Add Row</button>';
  html += '</div>';
  html += '<div class="table-container"><table id="results-table"><thead><tr>';
  resultsData.headers.forEach(header => { html += `<th>${header}</th>`; });
  html += '<th>Actions</th></tr></thead><tbody>';
  resultsData.rows.forEach((row, rowIndex) => {
    html += '<tr>';
    row.forEach((cell, cellIndex) => {
      html += `<td><input type="text" class="editable" value="${cell}" onchange="updateCell(${rowIndex}, ${cellIndex}, this.value, 'results')"></td>`;
    });
    html += `<td><button class="delete-btn" onclick="deleteRow(${rowIndex}, 'results')">🗑️ Delete</button></td>`;
    html += '</tr>';
  });
  html += '</tbody></table></div>';
  container.innerHTML = html;
}

function filterResults(searchTerm) {
  const table = document.getElementById('results-table');
  const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
  const term = searchTerm.toLowerCase();
  for (let row of rows) {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(term) ? '' : 'none';
  }
}

// Teams CSV handling (similar to results)
function loadTeamsCSV(event) {
  const file = event.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) { teamsData = parseCSV(e.target.result); displayTeams(); };
  reader.readAsText(file);
}

function displayTeams() {
  const container = document.getElementById('teams-content');
  if (teamsData.rows.length === 0) { container.innerHTML = '<div class="empty-state"><p>No data to display</p></div>'; return; }
  let html = '<input type="text" class="search-box" placeholder="🔍 Search teams..." onkeyup="filterTeams(this.value)">';
  html += '<div class="btn-group">';
  html += '<button class="btn btn-success" onclick="downloadCSV(teamsData, \'teams.csv\')"><span>💾</span> Download CSV</button>';
  html += '<button class="btn btn-primary" onclick="generateParticipantsHTML()"><span>📄</span> Generate participants.html</button>';
  html += '<button class="btn btn-primary add-row-btn" onclick="addTeamRow()"><span>➕</span> Add Row</button>';
  html += '</div>';
  html += '<div class="table-container"><table id="teams-table"><thead><tr>';
  teamsData.headers.forEach(header => { html += `<th>${header}</th>`; });
  html += '<th>Actions</th></tr></thead><tbody>';
  teamsData.rows.forEach((row, rowIndex) => {
    html += '<tr>';
    row.forEach((cell, cellIndex) => { html += `<td><input type="text" class="editable" value="${cell}" onchange="updateCell(${rowIndex}, ${cellIndex}, this.value, 'teams')"></td>`; });
    html += `<td><button class="delete-btn" onclick="deleteRow(${rowIndex}, 'teams')">🗑️ Delete</button></td>`;
    html += '</tr>';
  });
  html += '</tbody></table></div>';
  container.innerHTML = html;
}

function filterTeams(searchTerm) {
  const table = document.getElementById('teams-table');
  const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
  const term = searchTerm.toLowerCase();
  for (let row of rows) { const text = row.textContent.toLowerCase(); row.style.display = text.includes(term) ? '' : 'none'; }
}

// Update cell value
function updateCell(rowIndex, cellIndex, value, dataType) {
  if (dataType === 'results') { resultsData.rows[rowIndex][cellIndex] = value; updateStatistics(); }
  else if (dataType === 'teams') teamsData.rows[rowIndex][cellIndex] = value;
}

// Add / Delete rows
function addResultRow() { const newRow = new Array(resultsData.headers.length).fill(''); resultsData.rows.push(newRow); displayResults(); }
function addTeamRow() { const newRow = new Array(teamsData.headers.length).fill(''); teamsData.rows.push(newRow); displayTeams(); }
function deleteRow(rowIndex, dataType) { if (!confirm('Are you sure you want to delete this row?')) return; if (dataType === 'results') { resultsData.rows.splice(rowIndex, 1); displayResults(); updateStatistics(); } else { teamsData.rows.splice(rowIndex, 1); displayTeams(); } }

// Download CSV helper
function downloadCSV(data, filename) {
  let csv = data.headers.join(',') + '\n';
  data.rows.forEach(row => {
    csv += row.map(cell => {
      if (cell.includes(',') || cell.includes('"') || cell.includes('\n')) return '"' + cell.replace(/"/g, '""') + '"';
      return cell;
    }).join(',') + '\n';
  });
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = filename; a.click(); window.URL.revokeObjectURL(url);
}

// Statistics / charts (kept minimal)
function updateStatistics() {
  if (resultsData.rows.length === 0) return;
  const medalIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('medal'));
  const countryIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('country'));
  let total = resultsData.rows.length, gold = 0, silver = 0, bronze = 0; const countryMedals = {};
  resultsData.rows.forEach(row => {
    const medal = row[medalIndex]?.toLowerCase() || ''; const country = row[countryIndex] || 'Unknown';
    if (medal === 'gold') gold++; else if (medal === 'silver') silver++; else if (medal === 'bronze') bronze++;
    if (medal) { if (!countryMedals[country]) countryMedals[country] = { gold: 0, silver: 0, bronze: 0, total: 0 }; if (medal === 'gold') countryMedals[country].gold++; else if (medal === 'silver') countryMedals[country].silver++; else if (medal === 'bronze') countryMedals[country].bronze++; countryMedals[country].total++; }
  });
  document.getElementById('stat-total').textContent = total; document.getElementById('stat-gold').textContent = gold; document.getElementById('stat-silver').textContent = silver; document.getElementById('stat-bronze').textContent = bronze;
  displayCountryChart(countryMedals);
}

function displayCountryChart(countryMedals) {
  const chartContainer = document.getElementById('country-chart'); const breakdownContainer = document.getElementById('country-breakdown');
  const sorted = Object.entries(countryMedals).sort((a, b) => b[1].total - a[1].total).slice(0, 10);
  if (sorted.length === 0) { chartContainer.innerHTML = '<p style="text-align:center;color:var(--text-light)">No medal data available</p>'; return; }
  const maxTotal = Math.max(...sorted.map(([_, data]) => data.total));
  let html = '';
  sorted.forEach(([country, data]) => { const height = (data.total / maxTotal) * 100; html += `<div class="bar" style="height: ${height}%"><div class="bar-value">${data.total}</div><div class="bar-label">${country}</div></div>`; });
  chartContainer.innerHTML = html;
  let breakdownHtml = '<h3>Medal Breakdown by Country</h3><div class="table-container"><table><thead><tr><th>Country</th><th>🥇 Gold</th><th>🥈 Silver</th><th>🥉 Bronze</th><th>Total</th></tr></thead><tbody>';
  sorted.forEach(([country, data]) => { breakdownHtml += `<tr><td><strong>${country}</strong></td><td>${data.gold}</td><td>${data.silver}</td><td>${data.bronze}</td><td><strong>${data.total}</strong></td></tr>`; });
  breakdownHtml += '</tbody></table></div>'; breakdownContainer.innerHTML = breakdownHtml;
}

// Auto-assign medals
function autoAssignMedals() {
  if (resultsData.rows.length === 0) { alert('Please load results CSV first!'); return; }
  const rankIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('rank'));
  let medalIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('medal'));
  if (rankIndex === -1) { alert('No rank column found!'); return; }
  if (medalIndex === -1) { resultsData.headers.push('medal'); medalIndex = resultsData.headers.length - 1; resultsData.rows.forEach(row => { if (row.length < resultsData.headers.length) row.push(''); }); }
  resultsData.rows.forEach(row => { const rank = parseInt(row[rankIndex]); if (isNaN(rank)) return; if (rank >= 1 && rank <= 16) row[medalIndex] = 'gold'; else if (rank >= 17 && rank <= 48) row[medalIndex] = 'silver'; else if (rank >= 49 && rank <= 96) row[medalIndex] = 'bronze'; else row[medalIndex] = ''; });
  displayResults(); updateStatistics(); alert('✅ Medals assigned successfully!\n\n1-16: Gold\n17-48: Silver\n49-96: Bronze');
}

// Merge CSV files
function mergeCSVFiles(event) {
  const files = Array.from(event.target.files); if (files.length < 2) { alert('Please select at least 2 files to merge!'); return; }
  let mergedData = { headers: [], rows: [] }; let filesProcessed = 0;
  files.forEach((file, index) => { const reader = new FileReader(); reader.onload = function(e) { const data = parseCSV(e.target.result); if (index === 0) mergedData.headers = data.headers; mergedData.rows.push(...data.rows); filesProcessed++; if (filesProcessed === files.length) { downloadCSV(mergedData, 'merged.csv'); alert(`✅ ${files.length} files merged successfully! Total rows: ${mergedData.rows.length}`); } }; reader.readAsText(file); });
}

// Show generator instructions
function showGeneratorInstructions() {
  alert(`📖 Generate Participants Page Instructions:

1. Open a terminal in the project root directory

2. Run the Python script:
   python scripts/generate_participants.py

3. The script will:
   - Read csv/teams.csv
   - Match country flags from assets/flags/
   - Generate pages/contest/participants.html

4. The generated page will be ready to use!

Note: Make sure you have Python installed and the CSV files are up to date.`);
}

// Generate results.html from results CSV
function generateResultsHTML() {
  if (resultsData.rows.length === 0) { alert('Please load results CSV first!'); return; }
  const rankIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('rank'));
  const nameIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('name'));
  const countryIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('country'));
  const chooseIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('choose'));
  const octagonIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('octagon'));
  const skittlezIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('skittlez'));
  const day1Index = resultsData.headers.findIndex(h => h.toLowerCase().includes('day 1'));
  const signalsIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('signals'));
  const ramenIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('ramen'));
  const jumpIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('jump'));
  const day2Index = resultsData.headers.findIndex(h => h.toLowerCase().includes('day 2'));
  const scoreIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('total score'));
  let medalIndex = resultsData.headers.findIndex(h => h.toLowerCase().includes('medal'));
  if (medalIndex === -1) medalIndex = resultsData.headers.length - 1;
  let html = `<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Results - RMI 2024</title>
      <style>
      /* Small page-specific overrides that complement rms-theme */
      .table-container { overflow-x: auto; }
      /* Make page exactly viewport height on phones and let the table-area fill the remaining space.
         This keeps the header visible and makes the table scrollable inside the viewport. */
      @media (max-width: 760px) {
        html,body{height:100vh;margin:0}
        body{display:flex;flex-direction:column}
        .results-header{flex:0 0 auto;padding:.75rem 1rem;background:var(--card);border-bottom:1px solid rgba(0,0,0,0.06)}
        .table-container{flex:1 1 auto;overflow:auto;-webkit-overflow-scrolling:touch}
        /* Ensure table header stays visible inside the scrollable table container */
        .results-table thead th{position:sticky;top:0;background:var(--card);z-index:3}
      }
      /* Keep medal name colours (uses theme variables where appropriate) */
      .name-gold { color: #bb9413; font-weight: 600; }
      .name-silver { color: #807f81; font-weight: 600; }
      .name-bronze { color: #804A00; font-weight: 600; }
      /* Ensure sticky header on results (theme provides base styles) */
      .results-table thead th { position: sticky; top: 0; z-index: 2; }
    </style>
</head>
<body>
    <h2>Competition Results</h2>
    <div class="table-container">
        <table class="results-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Name</th>
                    <th>Country</th>
                    <th>Choose Interval</th>
                    <th>Octagon</th>
                    <th>Skittlez</th>
                    <th>Day1</th>
                    <th>Signals</th>
                    <th>Ramen</th>
                    <th>Jump Civilization</th>
                    <th>Day2</th>
                    <th>Total Score</th>
                </tr>
            </thead>
            <tbody>`;
  resultsData.rows.forEach(row => {
    const rank = row[rankIndex] || ''; const name = row[nameIndex] || ''; const country = row[countryIndex] || ''; const choose = row[chooseIndex] || ''; const octagon = row[octagonIndex] || ''; const skittlez = row[skittlezIndex] || ''; const day1 = row[day1Index] || ''; const signals = row[signalsIndex] || ''; const ramen = row[ramenIndex] || ''; const jump = row[jumpIndex] || ''; const day2 = row[day2Index] || ''; const score = row[scoreIndex] || ''; const medal = row[medalIndex]?.toLowerCase() || '';
    let nameClass = '';
    if (medal === 'gold') nameClass = 'name-gold'; else if (medal === 'silver') nameClass = 'name-silver'; else if (medal === 'bronze') nameClass = 'name-bronze';
    html += `
              <tr>
                <td><strong>${rank}</strong></td>
                <td><span class="${nameClass}">${name}</span></td>
                <td>${country}</td>
                <td>${choose}</td>
                <td>${octagon}</td>
                <td>${skittlez}</td>
                <td><strong>${day1}</strong></td>
                <td>${signals}</td>
                <td>${ramen}</td>
                <td>${jump}</td>
                <td><strong>${day2}</strong></td>
                <td><strong>${score}</strong></td>
              </tr>`;
  });
  html += `</tbody></table></div></body></html>`;
  const blob = new Blob([html], { type: 'text/html' }); const url = window.URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'results.html'; a.click(); window.URL.revokeObjectURL(url);
  alert('✅ results.html generated successfully!\n\nSave it to: pages/results.html');
}

// Generate participants.html (kept escaping for </script>)
function generateParticipantsHTML() {
  if (teamsData.rows.length === 0) { alert('Please load teams CSV first!'); return; }
  
  // Find column indexes - CSV structure: Name, (empty), Team, Country, Role
  const nameIndex = 0; // First column is name
  const teamIndex = 2; // Third column is team
  const countryIndex = 3; // Fourth column is country
  const roleIndex = 4; // Fifth column is role (Lider or empty)
  
  // Group data by team
  const teams = {};
  teamsData.rows.forEach(row => {
    const name = (row[nameIndex] || '').trim();
    const team = (row[teamIndex] || '').trim();
    const country = (row[countryIndex] || '').trim();
    const role = (row[roleIndex] || '').trim().toLowerCase();
    
    if (!team || !country) return; // Skip invalid rows
    
    if (!teams[team]) {
      teams[team] = { country: country, leaders: [], students: [] };
    }
    
    if (name) {
      if (role === 'lider') {
        teams[team].leaders.push(name);
      } else {
        teams[team].students.push(name);
      }
    }
  });
  
  // Generate HTML
  let html = `<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Participants - RMI 2024</title>
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
    <button id="nav-toggle" class="nav-toggle" aria-controls="site-nav" aria-expanded="false">☰</button>
    <div class="container">
        <header class="site-header">
            <h1>Participants</h1>
        </header>
        <main class="content">
            <section class="participants-section">
                <h2>Participants</h2>
                <div class="participants-list">`;
  
  // Sort teams alphabetically and generate blocks
  Object.keys(teams).sort().forEach(teamName => {
    const team = teams[teamName];
    const flagFile = team.country.toLowerCase().replace(/\s+/g, '-') + '.svg';
    const leadersText = team.leaders.length > 0 ? team.leaders.join(', ') : '';
    const studentsText = team.students.length > 0 ? team.students.join(', ') : '';
    
    html += `
            <div class="team-block">
              <div class="team-header">
                <div class="team-flag"><img src="/assets/flags/${flagFile}" alt="${team.country}"/></div>
                <div class="team-name">${teamName}</div>
              </div>
              <div class="team-leaders"><strong>Leaders:</strong> `;
    
    if (leadersText) {
      html += `<span class="member-list">${leadersText}</span>`;
    } else {
      html += `<span class="none">—</span>`;
    }
    
    html += `</div>
              <div class="team-students"><strong>Students:</strong> `;
    
    if (studentsText) {
      html += `<span class="member-list">${studentsText}</span>`;
    } else {
      html += `<span class="none">—</span>`;
    }
    
    html += `</div>
            </div>`;
  });
  
  html += `
                </div>
            </section>
        </main>
        <footer class="site-footer">&copy; RMI 2024</footer>
    </div>
    <link rel="icon" href="/assets/organisers/vianu.png" type="image/png">
    <script src="/assets/js/main.js"><\/script>
</body>
</html>`;
  
  const blob = new Blob([html], { type: 'text/html' }); 
  const url = window.URL.createObjectURL(blob); 
  const a = document.createElement('a'); 
  a.href = url; 
  a.download = 'participants.html'; 
  a.click(); 
  window.URL.revokeObjectURL(url);
  alert('✅ participants.html generated successfully!\n\nSave it to: pages/participants.html');
}

// Drag and drop support
document.querySelectorAll('.file-input-area').forEach(area => {
  area.addEventListener('dragover', (e) => { e.preventDefault(); area.classList.add('active'); });
  area.addEventListener('dragleave', () => { area.classList.remove('active'); });
  area.addEventListener('drop', (e) => {
    e.preventDefault(); area.classList.remove('active'); const files = e.dataTransfer.files; if (files.length > 0) { const input = area.nextElementSibling; if (input && input.tagName === 'INPUT') { input.files = files; input.dispatchEvent(new Event('change')); } }
  });
});

// Initialize theme toggle element similar to previous inline behavior (keeps parity)
(function createThemeToggle(){
  const btn = document.createElement('button'); btn.className = 'theme-toggle'; btn.type = 'button'; btn.title = 'Toggle theme'; btn.innerHTML = '<span class="icon">🌙</span>';
  btn.addEventListener('click', ()=>{ const isDark = document.body.classList.toggle('theme-dark'); localStorage.setItem('site-theme-dark', isDark ? '1' : '0'); btn.innerHTML = isDark ? '<span class="icon">☀️</span>' : '<span class="icon">🌙</span>'; });
  document.body.appendChild(btn); const pref = localStorage.getItem('site-theme-dark'); if(pref === '1'){ document.body.classList.add('theme-dark'); btn.innerHTML = '<span class="icon">☀️</span>'; }
})();
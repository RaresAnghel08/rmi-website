# 📋 Admin Dashboard Guide

## Quick Start

1. Open `admin.html` in your browser (Chrome, Firefox, Edge, Safari)
2. You'll see 4 tabs: **Results**, **Teams**, **Statistics**, **Tools**

## Managing Results

### Load Results CSV
1. Go to the **Results** tab
2. Click the file input area or drag & drop `csv/results.csv`
3. The data will appear in an editable table

### Edit Results
- Click any cell to edit its value
- Use the search box to filter by name, country, or rank
- Click "➕ Add Row" to add new entries
- Click "🗑️ Delete" to remove rows
- Changes are saved automatically in memory

### Generate Results HTML
1. After loading and editing your results
2. Click **"📄 Generate results.html"**
3. The browser will download the generated HTML file
4. Save it to `pages/contest/results.html` in your repository

The generated file includes:
- Formatted table with rankings
- Country names
- Total scores
- Medal badges (🥇 Gold, 🥈 Silver, 🥉 Bronze)
- Responsive design
- Navigation integration

## Managing Teams/Participants

### Load Teams CSV
1. Go to the **Teams** tab
2. Click the file input area or drag & drop `csv/teams.csv`
3. Edit teams, leaders, and students directly in the table

### Generate Participants HTML
1. After loading and editing teams
2. Click **"📄 Generate participants.html"**
3. Save the downloaded file to `pages/contest/participants.html`

The generated file includes:
- Team blocks with country flags
- Leaders and students lists
- Grouped by team
- Matches the existing site design

## Statistics Dashboard

The **Statistics** tab automatically shows:
- Total participants count
- Medal counts (Gold, Silver, Bronze)
- Interactive bar chart of medals by country
- Detailed breakdown table

Statistics update automatically when you edit results data.

## Utility Tools

### Auto-assign Medals
1. Load `csv/results.csv` in the Results tab
2. Go to the **Tools** tab
3. Click **"✨ Auto-assign Medals"**
4. Medals will be assigned based on rank:
   - Ranks 1-16: 🥇 Gold
   - Ranks 17-48: 🥈 Silver
   - Ranks 49-96: 🥉 Bronze

### Merge CSV Files
1. Go to the **Tools** tab
2. Click "Select multiple CSV files to merge"
3. Choose 2 or more CSV files
4. Download the merged result

## Workflow Example

### Updating Competition Results

1. **Open Admin Dashboard**
   ```
   Open admin.html in your browser
   ```

2. **Load Current Data**
   - Load `csv/results.csv` in Results tab

3. **Make Changes**
   - Update scores, add new participants, fix typos
   - Use auto-assign medals if needed

4. **Generate HTML**
   - Click "Generate results.html"
   - Save to `pages/contest/results.html`

5. **Update Repository**
   ```powershell
   git add csv/results.csv pages/contest/results.html
   git commit -m "Update competition results"
   git push
   ```

6. **Deploy**
   - Your changes are live after the git push (if using Netlify/GitHub Pages)

## Tips & Tricks

### Search & Filter
- Use the search box to quickly find specific participants
- Type country names to see all participants from that country
- Search by rank numbers

### Keyboard Shortcuts
- **Tab**: Move to next cell
- **Enter**: Save cell and move down
- **Escape**: Cancel editing

### Data Validation
- The dashboard validates rank numbers for medal assignment
- Empty cells are preserved
- CSV special characters (commas, quotes) are properly escaped

### Backup
Always download CSV files before major changes:
1. Click "💾 Download CSV" before editing
2. Keep a backup copy
3. You can reload the backup if needed

## Troubleshooting

### "No file loaded" message
- Make sure you clicked the file input area and selected a CSV file
- Check that the file is a valid CSV format

### Medal badges not showing
- Ensure the CSV has a "medal" column with values: gold, silver, or bronze
- Use the "Auto-assign Medals" tool to populate automatically

### Generated HTML looks wrong
- Make sure you loaded the correct CSV file
- Check that CSV columns are properly formatted
- Verify headers match expected names (Total Rank, Name, Country, etc.)

### Browser compatibility
- Use a modern browser (Chrome 90+, Firefox 88+, Edge 90+, Safari 14+)
- JavaScript must be enabled
- No browser extensions should block file operations

## Security Note

⚠️ **All data processing happens in your browser**
- No data is sent to any server
- Files are processed locally on your computer
- Changes are only saved when you download files
- Safe to use with sensitive competition data

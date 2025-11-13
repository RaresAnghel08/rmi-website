import re

# Read the original file to extract team data
with open('d:/GITHUB/update_rmi_2024/rmi-website/rmi_2025/pages/participants.html', 'r', encoding='utf-8') as f:
    original_content = f.read()

# Extract teams data using regex
teams = []
team_pattern = r'<div class="team-card">.*?<img src="([^"]+)" alt="([^"]+)".*?<div class="team-name">([^<]+)</div>.*?<span class="label">Leaders:</span>\s*<span class="member-list">([^<]+)</span>.*?<span class="label">Students:</span>\s*<span class="member-list">([^<]+)</span>'
matches = re.findall(team_pattern, original_content, re.DOTALL)

for match in matches:
    teams.append({
        'flag': match[0],
        'country': match[1],
        'name': match[2].strip(),
        'leaders': match[3].strip(),
        'students': match[4].strip()
    })

# Create new HTML with proper structure
html_head = '''<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>Participants</title>
        <link rel="stylesheet" href="assets/css/style.css">
    </head>
    <body>
        <div class="container">
            <header class="site-header"><h1>Participants</h1></header>
            <main class="content">
                <section class="participants-section">
                    <h2>Participants</h2>
                    <div class="participants-grid">
'''

html_foot = '''                    </div>
                </section>
            </main>
            <footer class="site-footer">&copy; 2025 Tudor Vianu National High School of Computer Science - Built by <a href="https://linkedin.com/in/raresanghel" target="_blank" rel="noopener" title="Visit Rares Anghel's LinkedIn profile">Rares Anghel</a></footer>
        </div>
        <link rel="icon" href="assets/organisers/vianu.png" type="image/png">
        <script src="assets/js/main.js"></script>
    </body>
</html>
'''

# Generate team cards
team_cards = []
for team in teams:
    card = f'''            <div class="team-card">
              <div class="team-flag-header"><img src="{team['flag']}" alt="{team['country']}" class="flag-img"/></div>
              <div class="team-name">{team['name']}</div>
              <div class="team-info">
                <div class="team-leaders"><span class="label">Leaders:</span> <span class="member-list">{team['leaders']}</span></div>
                <div class="team-students"><span class="label">Students:</span> <span class="member-list">{team['students']}</span></div>
              </div>
            </div>'''
    team_cards.append(card)

# Combine everything
new_html = html_head + '\n'.join(team_cards) + '\n' + html_foot

# Write the new file
with open('d:/GITHUB/update_rmi_2024/rmi-website/rmi_2025/pages/participants.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Successfully created {len(teams)} team cards!")

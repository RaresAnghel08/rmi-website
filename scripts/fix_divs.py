import re

# Read the file
with open('d:/GITHUB/update_rmi_2024/rmi-website/rmi_2025/pages/participants.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove extra closing divs between cards
pattern = r'</div>\s*</div>\s*</div>\s*<div class="team-card">'
replacement = r'</div>\n            </div>\n            <div class="team-card">'
content = re.sub(pattern, replacement, content)

# Fix any remaining double closing divs
content = re.sub(r'</div>\s*</div>\s*<div class="team-card">', r'</div>\n            <div class="team-card">', content)

# Write back
with open('d:/GITHUB/update_rmi_2024/rmi-website/rmi_2025/pages/participants.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed extra divs!")

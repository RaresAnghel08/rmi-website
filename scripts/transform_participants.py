import re

# Read the file
with open('d:/GITHUB/update_rmi_2024/rmi-website/rmi_2025/pages/participants.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace team-block with team-card
content = content.replace('class="team-block"', 'class="team-card"')

# Replace team-header structure with team-flag-header
pattern = r'<div class="team-header">\s*<div class="team-flag"><img src="([^"]+)" alt="([^"]+)"/></div>\s*<div class="team-name">([^<]+)</div>\s*</div>'
replacement = r'<div class="team-flag-header"><img src="\1" alt="\2" class="flag-img"/></div>\n              <div class="team-name">\3</div>\n              <div class="team-info">'
content = re.sub(pattern, replacement, content)

# Replace <strong>Leaders:</strong> with <span class="label">Leaders:</span>
content = content.replace('<strong>Leaders:</strong>', '<span class="label">Leaders:</span>')

# Replace <strong>Students:</strong> with <span class="label">Students:</span>
content = content.replace('<strong>Students:</strong>', '<span class="label">Students:</span>')

# Add closing </div> for team-info before each new team-card (except the first one)
# Find pattern where team-students ends and next team-card begins
pattern = r'(</div>\s*</div>\s*)<div class="team-card">'
replacement = r'\1</div>\n            <div class="team-card">'
content = re.sub(pattern, replacement, content)

# Fix the last team card - add closing div for team-info
content = content.replace('</div>\n            </div>\n                    </div>', '</div>\n              </div>\n            </div>\n                    </div>')

# Replace participants-list with participants-grid
content = content.replace('participants-list', 'participants-grid')

# Write back
with open('d:/GITHUB/update_rmi_2024/rmi-website/rmi_2025/pages/participants.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Transformation complete!")

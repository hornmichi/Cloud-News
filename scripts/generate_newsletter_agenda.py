#!/usr/bin/env python3
"""
Generate a clickable agenda for the newsletter.
This script creates a table of contents with links to each section.
"""

import os
import json
import re
from datetime import datetime
from urllib.parse import quote

def load_monthly_content():
    """Load content for the current month."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m")
    
    # Look for monthly content file
    content_file = f"content/monthly_content_{timestamp}.json"
    
    if not os.path.exists(content_file):
        print(f"Error: No content file found for {now.strftime('%B %Y')}")
        return []
    
    with open(content_file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    return content

def create_section_id(title):
    """Create a URL-friendly section ID from title."""
    # Remove special characters and convert to lowercase
    id_text = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    id_text = re.sub(r'\s+', '-', id_text.lower())
    return id_text

def generate_teams_agenda(content, newsletter_url):
    """Generate a Teams-friendly agenda with clickable links."""
    now = datetime.now()
    month_year = now.strftime('%B %Y')
    
    # Start with header
    agenda = f"""📰 **Cloud News - {month_year}**

Welcome to this month's newsletter! Here's what's inside:

📊 **Monthly Highlights**
• {len(content)} articles from our community
• {len(set(article.get('category', '') for article in content))} different categories
• {len(set(article.get('author', '') for article in content))} contributors

---

**📋 Table of Contents**

"""
    
    # Sort content by priority and category
    sorted_content = sorted(content, key=lambda x: (
        {'Urgent': 0, 'High': 1, 'Normal': 2}.get(x.get('priority', 'Normal'), 2),
        x.get('category', '')
    ))
    
    # Group by category
    categories = {}
    for article in sorted_content:
        category = article.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(article)
    
    # Generate agenda items
    for category, articles in categories.items():
        agenda += f"\n**{category}**\n"
        
        for i, article in enumerate(articles):
            title = article.get('title', 'Untitled')
            author = article.get('author', 'Unknown')
            priority = article.get('priority', 'Normal')
            
            # Create section ID
            section_id = create_section_id(title)
            
            # Priority emoji
            priority_emoji = {
                'Urgent': '🔴',
                'High': '🟡', 
                'Normal': '⚪'
            }.get(priority, '⚪')
            
            # Create link
            link = f"{newsletter_url}#{section_id}"
            
            agenda += f"{priority_emoji} [{title}]({link}) - by {author}\n"
    
    # Add footer
    agenda += f"""

---

**📝 Want to contribute?**
Submit content for next month's newsletter: [Submit Here](https://github.com/hornmichi/Cloud-News/issues)

**📧 Questions?**
Contact us: newsletter@hornmichi.com

---
*This newsletter is automatically generated from community contributions.*
"""
    
    return agenda

def generate_html_agenda(content, newsletter_url):
    """Generate an HTML agenda with anchor links."""
    now = datetime.now()
    month_year = now.strftime('%B %Y')
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter Agenda - {month_year}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 30px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .category {{
            margin-bottom: 25px;
        }}
        .category h3 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
            margin-bottom: 15px;
        }}
        .agenda-item {{
            margin-bottom: 12px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }}
        .agenda-item a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}
        .agenda-item a:hover {{
            text-decoration: underline;
        }}
        .priority-urgent {{ border-left-color: #e74c3c; }}
        .priority-high {{ border-left-color: #f39c12; }}
        .priority-normal {{ border-left-color: #95a5a6; }}
        .author {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .stats {{
            background: #e8f4fd;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 Cloud News - {month_year}</h1>
            <p>Newsletter Agenda</p>
        </div>
        
        <div class="stats">
            <h3>📊 This Month's Highlights</h3>
            <p><strong>{len(content)} articles</strong> from our community</p>
            <p><strong>{len(set(article.get('category', '') for article in content))} categories</strong> covered</p>
            <p><strong>{len(set(article.get('author', '') for article in content))} contributors</strong> participated</p>
        </div>
"""
    
    # Group by category
    categories = {}
    for article in content:
        category = article.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(article)
    
    # Sort content by priority
    sorted_content = sorted(content, key=lambda x: (
        {'Urgent': 0, 'High': 1, 'Normal': 2}.get(x.get('priority', 'Normal'), 2),
        x.get('category', '')
    ))
    
    for category, articles in categories.items():
        html += f"""
        <div class="category">
            <h3>{category}</h3>
"""
        
        for article in articles:
            title = article.get('title', 'Untitled')
            author = article.get('author', 'Unknown')
            priority = article.get('priority', 'Normal')
            section_id = create_section_id(title)
            
            priority_class = f"priority-{priority.lower()}"
            
            html += f"""
            <div class="agenda-item {priority_class}">
                <a href="{newsletter_url}#{section_id}">{title}</a>
                <div class="author">by {author}</div>
            </div>
"""
        
        html += "        </div>"
    
    html += """
        <div class="footer">
            <p>Want to contribute? <a href="https://github.com/hornmichi/Cloud-News/issues">Submit content here</a></p>
            <p>📧 newsletter@hornmichi.com</p>
        </div>
    </div>
</body>
</html>"""
    
    return html

def save_agenda_files(teams_agenda, html_agenda):
    """Save the agenda files."""
    timestamp = datetime.now().strftime("%Y%m")
    
    # Save Teams agenda (Markdown format)
    teams_filename = f"newsletters/teams-agenda-{timestamp}.md"
    os.makedirs(os.path.dirname(teams_filename), exist_ok=True)
    with open(teams_filename, 'w', encoding='utf-8') as f:
        f.write(teams_agenda)
    
    # Save HTML agenda
    html_filename = f"newsletters/html-agenda-{timestamp}.html"
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_agenda)
    
    # Save copy-paste version for Teams
    copy_paste_filename = f"newsletters/teams-copy-paste-{timestamp}.txt"
    with open(copy_paste_filename, 'w', encoding='utf-8') as f:
        f.write("=== COPY AND PASTE INTO MICROSOFT TEAMS ===\n\n")
        f.write(teams_agenda)
        f.write("\n\n=== END OF COPY-PASTE CONTENT ===")
    
    print(f"Agenda files saved:")
    print(f"  - Teams Markdown: {teams_filename}")
    print(f"  - HTML Agenda: {html_filename}")
    print(f"  - Copy-Paste: {copy_paste_filename}")
    
    return copy_paste_filename

def main():
    """Main function to generate the newsletter agenda."""
    print("📋 Generating Newsletter Agenda")
    print("=" * 40)
    
    # Load monthly content
    content = load_monthly_content()
    
    if not content:
        print("No content found for this month. Please collect content first.")
        return
    
    print(f"Found {len(content)} articles for {datetime.now().strftime('%B %Y')}")
    
    # Newsletter URL (this would be the published newsletter URL)
    newsletter_url = "https://github.com/hornmichi/Cloud-News/releases/latest"
    
    # Generate agendas
    teams_agenda = generate_teams_agenda(content, newsletter_url)
    html_agenda = generate_html_agenda(content, newsletter_url)
    
    # Save files
    copy_paste_file = save_agenda_files(teams_agenda, html_agenda)
    
    print("\n✅ Newsletter agenda generated successfully!")
    print(f"\n📋 Copy-paste file ready: {copy_paste_file}")
    print("\n💡 How to use:")
    print("1. Open the copy-paste file")
    print("2. Copy the content between the markers")
    print("3. Paste directly into Microsoft Teams")
    print("4. The links will be clickable in Teams!")
    
    # Display the agenda for immediate use
    print("\n" + "="*50)
    print("📋 AGENDA FOR IMMEDIATE USE:")
    print("="*50)
    print(teams_agenda)

if __name__ == "__main__":
    main()

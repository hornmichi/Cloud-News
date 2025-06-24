#!/usr/bin/env python3
"""
Test script to generate agenda with example content.
"""

import json
import re
from datetime import datetime

def create_section_id(title):
    """Create a URL-friendly section ID from title."""
    id_text = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    id_text = re.sub(r'\s+', '-', id_text.lower())
    return id_text

def generate_teams_agenda(content, newsletter_url):
    """Generate a Teams-friendly agenda with clickable links."""
    month_year = "January 2024"
    
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

def main():
    """Main function to test agenda generation."""
    print("📋 Testing Newsletter Agenda Generation")
    print("=" * 45)
    
    # Load example content
    with open('content/example_monthly_content.json', 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    print(f"Loaded {len(content)} example articles")
    
    # Newsletter URL (example)
    newsletter_url = "https://github.com/hornmichi/Cloud-News/releases/latest"
    
    # Generate agenda
    teams_agenda = generate_teams_agenda(content, newsletter_url)
    
    # Save copy-paste version
    copy_paste_filename = "example-teams-agenda.txt"
    with open(copy_paste_filename, 'w', encoding='utf-8') as f:
        f.write("=== COPY AND PASTE INTO MICROSOFT TEAMS ===\n\n")
        f.write(teams_agenda)
        f.write("\n\n=== END OF COPY-PASTE CONTENT ===")
    
    print(f"\n✅ Example agenda saved to: {copy_paste_filename}")
    
    # Display the agenda
    print("\n" + "="*50)
    print("📋 EXAMPLE AGENDA FOR MICROSOFT TEAMS:")
    print("="*50)
    print(teams_agenda)

if __name__ == "__main__":
    main()

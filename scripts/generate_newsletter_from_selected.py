#!/usr/bin/env python3
"""
Generate newsletter from selected GitHub issue numbers.
Usage: python generate_newsletter_from_selected.py "1,2,3" "January 2024"
"""

import sys
import json
import re
import os
from datetime import datetime
from jinja2 import Template
import requests

def create_section_id(title):
    """Create a URL-friendly section ID from title."""
    id_text = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    id_text = re.sub(r'\s+', '-', id_text.lower())
    return id_text

def fetch_issue_content(issue_number, repo_owner, repo_name, token=None):
    """Fetch issue content from GitHub API."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}"
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching issue {issue_number}: {response.status_code}")
        return None
    
    issue = response.json()
    
    # Parse the issue body to extract structured content
    body = issue.get('body', '')
    lines = body.split('\n')
    
    # Extract content from issue body
    content = {
        'title': issue.get('title', 'Untitled'),
        'author': issue.get('user', {}).get('login', 'Unknown'),
        'url': issue.get('html_url', ''),
        'number': issue_number,
        'body': body
    }
    
    # Try to extract structured fields from the issue body
    for line in lines:
        if line.startswith('**Title:**'):
            content['title'] = line.replace('**Title:**', '').strip()
        elif line.startswith('**Summary:**'):
            content['summary'] = line.replace('**Summary:**', '').strip()
        elif line.startswith('**Category:**'):
            content['category'] = line.replace('**Category:**', '').strip()
        elif line.startswith('**Priority:**'):
            content['priority'] = line.replace('**Priority:**', '').strip()
        elif line.startswith('**Author:**'):
            content['author'] = line.replace('**Author:**', '').strip()
        elif line.startswith('**Image:**'):
            content['image'] = line.replace('**Image:**', '').strip()
    
    # Set defaults if not found
    if 'summary' not in content:
        content['summary'] = body[:200] + '...' if len(body) > 200 else body
    if 'category' not in content:
        content['category'] = 'Article'
    if 'priority' not in content:
        content['priority'] = 'Normal'
    if 'image' not in content:
        content['image'] = ''
    
    # Extract the main content (everything after the metadata)
    content_lines = []
    in_content = False
    for line in lines:
        if line.startswith('**Content:**'):
            in_content = True
            continue
        if in_content:
            content_lines.append(line)
    
    content['content'] = '\n'.join(content_lines).strip()
    if not content['content']:
        content['content'] = body
    
    return content

def generate_newsletter_html(articles, newsletter_date):
    """Generate the newsletter HTML."""
    template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud News - {{ newsletter_date }}</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            background-color: #f8f9fa;
        }
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 40px; 
            text-align: center; 
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .monthly-info {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .content-area {
            padding: 40px;
        }
        .article { 
            margin-bottom: 40px; 
            padding: 25px; 
            border-left: 4px solid #667eea; 
            background: #f8f9fa; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            scroll-margin-top: 20px;
        }
        .article h2 { 
            color: #667eea; 
            margin-bottom: 15px; 
            font-size: 1.5rem;
        }
        .article .meta { 
            color: #666; 
            font-size: 0.9em; 
            margin-bottom: 15px; 
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        .article .summary { 
            font-style: italic; 
            color: #555; 
            margin-bottom: 20px; 
            padding: 15px;
            background: white;
            border-radius: 6px;
            border-left: 3px solid #667eea;
        }
        .category-badge { 
            display: inline-block; 
            background: #667eea; 
            color: white; 
            padding: 6px 12px; 
            border-radius: 20px; 
            font-size: 0.8em; 
            font-weight: 600;
        }
        .priority-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: 600;
        }
        .priority-urgent { background: #e74c3c; color: white; }
        .priority-high { background: #f39c12; color: white; }
        .priority-normal { background: #95a5a6; color: white; }
        .footer { 
            text-align: center; 
            margin-top: 40px; 
            padding: 30px; 
            background: #f8f9fa; 
            border-top: 1px solid #e9ecef;
        }
        .footer a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        .image {
            margin-top: 20px;
            text-align: center;
        }
        .image img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .monthly-stats {
            background: #e8f4fd;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }
        .stat-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 5px;
        }
        @media (max-width: 768px) {
            body { padding: 10px; }
            .header { padding: 30px 20px; }
            .header h1 { font-size: 2rem; }
            .content-area { padding: 30px 20px; }
            .article { padding: 20px; }
            .stats-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 Cloud News</h1>
            <p>{{ newsletter_date }}</p>
            <div class="monthly-info">
                <strong>Monthly Newsletter</strong><br>
                {{ total_articles }} articles • {{ categories_count }} categories
            </div>
        </div>

        <div class="content-area">
            <div class="monthly-stats">
                <h3>📊 This Month's Highlights</h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number">{{ total_articles }}</div>
                        <div class="stat-label">Articles</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{{ categories_count }}</div>
                        <div class="stat-label">Categories</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{{ authors_count }}</div>
                        <div class="stat-label">Contributors</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{{ urgent_count }}</div>
                        <div class="stat-label">Urgent Items</div>
                    </div>
                </div>
            </div>

            {% for article in articles %}
            <div class="article" id="{{ article.section_id }}">
                <h2>{{ article.title }}</h2>
                <div class="meta">
                    <span class="category-badge">{{ article.category }}</span>
                    <span class="priority-badge priority-{{ article.priority.lower() }}">{{ article.priority }}</span>
                    <span>By {{ article.author }}</span>
                </div>
                <div class="summary">{{ article.summary }}</div>
                <div class="content">{{ article.content | safe }}</div>
                {% if article.image %}
                <div class="image">
                    <img src="{{ article.image }}" alt="Article image">
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>

        <div class="footer">
            <p>Want to contribute? <a href="https://github.com/hornmichi/Cloud-News/issues">Submit content here</a></p>
            <p>📧 <a href="mailto:newsletter@hornmichi.com">newsletter@hornmichi.com</a></p>
            <p style="margin-top: 20px; font-size: 0.9em; color: #666;">© 2024 Cloud News. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
    
    template = Template(template_content)
    
    # Sort content by priority and category
    sorted_articles = sorted(articles, key=lambda x: (
        {'Urgent': 0, 'High': 1, 'Normal': 2}.get(x.get('priority', 'Normal'), 2),
        x.get('category', '')
    ))
    
    # Add section IDs to each article
    for article in sorted_articles:
        article['section_id'] = create_section_id(article.get('title', 'Untitled'))
    
    # Calculate statistics
    categories = set(article.get('category', '') for article in articles)
    authors = set(article.get('author', '') for article in articles)
    urgent_count = sum(1 for article in articles if article.get('priority') == 'Urgent')
    
    html_content = template.render(
        articles=sorted_articles,
        newsletter_date=newsletter_date,
        total_articles=len(articles),
        categories_count=len(categories),
        authors_count=len(authors),
        urgent_count=urgent_count
    )
    
    return html_content

def generate_teams_agenda(articles, newsletter_date, newsletter_url):
    """Generate a Teams-friendly agenda with clickable links."""
    
    # Start with header
    agenda = f"""📰 **Cloud News - {newsletter_date}**

Welcome to this month's newsletter! Here's what's inside:

📊 **Monthly Highlights**
• {len(articles)} articles from our community
• {len(set(article.get('category', '') for article in articles))} different categories
• {len(set(article.get('author', '') for article in articles))} contributors

---

**📋 Table of Contents**

"""
    
    # Sort content by priority and category
    sorted_articles = sorted(articles, key=lambda x: (
        {'Urgent': 0, 'High': 1, 'Normal': 2}.get(x.get('priority', 'Normal'), 2),
        x.get('category', '')
    ))
    
    # Group by category
    categories = {}
    for article in sorted_articles:
        category = article.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(article)
    
    # Generate agenda items
    for category, category_articles in categories.items():
        agenda += f"\n**{category}**\n"
        
        for article in category_articles:
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
    """Main function."""
    if len(sys.argv) != 3:
        print("Usage: python generate_newsletter_from_selected.py \"1,2,3\" \"January 2024\"")
        sys.exit(1)
    
    selected_articles_str = sys.argv[1]
    newsletter_date = sys.argv[2]
    
    # Parse selected article numbers
    try:
        article_numbers = [int(x.strip()) for x in selected_articles_str.split(',')]
    except ValueError:
        print("Error: Article numbers must be comma-separated integers")
        sys.exit(1)
    
    # Configuration
    repo_owner = "hornmichi"
    repo_name = "Cloud-News"
    github_token = os.getenv('GITHUB_TOKEN')
    
    print(f"Fetching {len(article_numbers)} articles...")
    
    # Fetch articles from GitHub Issues
    articles = []
    for issue_number in article_numbers:
        print(f"Fetching issue #{issue_number}...")
        article = fetch_issue_content(issue_number, repo_owner, repo_name, github_token)
        if article:
            articles.append(article)
        else:
            print(f"Warning: Could not fetch issue #{issue_number}")
    
    if not articles:
        print("No articles found. Exiting.")
        sys.exit(1)
    
    print(f"Successfully fetched {len(articles)} articles")
    
    # Generate newsletter HTML
    print("Generating newsletter HTML...")
    html_content = generate_newsletter_html(articles, newsletter_date)
    
    # Save newsletter
    with open('newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Generate Teams agenda
    print("Generating Teams agenda...")
    newsletter_url = f"https://github.com/{repo_owner}/{repo_name}/releases/latest"
    teams_agenda = generate_teams_agenda(articles, newsletter_date, newsletter_url)
    
    # Save agenda
    with open('teams-agenda.txt', 'w', encoding='utf-8') as f:
        f.write("=== COPY AND PASTE INTO MICROSOFT TEAMS ===\n\n")
        f.write(teams_agenda)
        f.write("\n\n=== END OF COPY-PASTE CONTENT ===")
    
    print("✅ Newsletter files generated:")
    print("  - newsletter.html")
    print("  - teams-agenda.txt")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate monthly newsletter with section IDs for agenda links.
This script creates the final monthly newsletter with anchor links.
"""

import os
import json
import re
from datetime import datetime
from jinja2 import Template

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

def load_newsletter_template():
    """Load the newsletter template with section IDs."""
    template_path = "templates/monthly_newsletter_with_agenda.html"
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # Return a template with section IDs
        return """
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
            {% if monthly_stats %}
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
            {% endif %}

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

def generate_monthly_newsletter_html(content, template_content):
    """Generate the monthly newsletter HTML using the template."""
    template = Template(template_content)
    
    # Prepare data for template
    newsletter_date = datetime.now().strftime("%B %Y")
    
    # Sort content by priority and category
    sorted_content = sorted(content, key=lambda x: (
        {'Urgent': 0, 'High': 1, 'Normal': 2}.get(x.get('priority', 'Normal'), 2),
        x.get('category', '')
    ))
    
    # Add section IDs to each article
    for article in sorted_content:
        article['section_id'] = create_section_id(article.get('title', 'Untitled'))
    
    # Calculate statistics
    categories = set(article.get('category', '') for article in content)
    authors = set(article.get('author', '') for article in content)
    urgent_count = sum(1 for article in content if article.get('priority') == 'Urgent')
    
    monthly_stats = {
        'total_articles': len(content),
        'categories_count': len(categories),
        'authors_count': len(authors),
        'urgent_count': urgent_count
    }
    
    html_content = template.render(
        articles=sorted_content,
        newsletter_date=newsletter_date,
        total_articles=len(content),
        monthly_stats=monthly_stats,
        **monthly_stats
    )
    
    return html_content

def generate_monthly_newsletter_markdown(content):
    """Generate a markdown version of the monthly newsletter with section IDs."""
    newsletter_date = datetime.now().strftime("%B %Y")
    
    markdown_content = f"""# 📰 Cloud News - {newsletter_date}

Welcome to this month's Cloud News! Here's what's happening in our community.

## 📊 Monthly Highlights

- **Total Articles**: {len(content)}
- **Categories**: {len(set(article.get('category', '') for article in content))}
- **Contributors**: {len(set(article.get('author', '') for article in content))}
- **Urgent Items**: {sum(1 for article in content if article.get('priority') == 'Urgent')}

---

"""
    
    # Sort content by priority and category
    sorted_content = sorted(content, key=lambda x: (
        {'Urgent': 0, 'High': 1, 'Normal': 2}.get(x.get('priority', 'Normal'), 2),
        x.get('category', '')
    ))
    
    for article in sorted_content:
        title = article.get('title', 'Untitled')
        section_id = create_section_id(title)
        
        markdown_content += f"""## <a name="{section_id}"></a>{title}

**Category:** {article['category']} | **Author:** {article['author']} | **Priority:** {article['priority']}

{article['summary']}

{article['content']}

"""
        
        if article.get('image'):
            markdown_content += f"![{title}]({article['image']})\n\n"
        
        markdown_content += "---\n\n"
    
    markdown_content += """---

**Want to contribute?** [Submit content here](https://github.com/hornmichi/Cloud-News/issues)

© 2024 Cloud News. All rights reserved.
"""
    
    return markdown_content

def save_newsletter_files(html_content, markdown_content):
    """Save the newsletter files."""
    timestamp = datetime.now().strftime("%Y%m")
    
    # Save HTML version
    html_filename = f"newsletters/monthly-newsletter-{timestamp}.html"
    os.makedirs(os.path.dirname(html_filename), exist_ok=True)
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Save Markdown version
    markdown_filename = f"newsletters/monthly-newsletter-{timestamp}.md"
    with open(markdown_filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    # Save draft for review
    with open("monthly-newsletter-draft.md", 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Newsletter files saved:")
    print(f"  - HTML: {html_filename}")
    print(f"  - Markdown: {markdown_filename}")
    print(f"  - Draft: monthly-newsletter-draft.md")
    
    return html_filename

def main():
    """Main function to generate the monthly newsletter."""
    print("📰 Generating Monthly Newsletter with Agenda Links")
    print("=" * 50)
    
    # Load monthly content
    content = load_monthly_content()
    
    if not content:
        print("No content found for this month. Please collect content first.")
        return
    
    print(f"Found {len(content)} articles for {datetime.now().strftime('%B %Y')}")
    
    # Load template
    template_content = load_newsletter_template()
    
    # Generate newsletter
    html_content = generate_monthly_newsletter_html(content, template_content)
    markdown_content = generate_monthly_newsletter_markdown(content)
    
    # Save files
    html_filename = save_newsletter_files(html_content, markdown_content)
    
    print("✅ Monthly newsletter generation complete!")
    print(f"\n🔗 Newsletter URL: {html_filename}")
    print("💡 Use generate_newsletter_agenda.py to create the Teams agenda!")

if __name__ == "__main__":
    main()

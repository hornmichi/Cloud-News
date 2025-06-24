#!/usr/bin/env python3
"""
Collect monthly newsletter content from GitHub issues.
This script collects all approved content for the current month.
"""

import os
import json
import re
from datetime import datetime, timedelta
from github import Github
from dateutil import parser

def get_monthly_content():
    """Collect all approved content for the current month."""
    # Initialize GitHub client
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set")
        return []
    
    g = Github(github_token)
    
    # Get repository information
    repo_name = os.getenv('GITHUB_REPOSITORY', 'hornmichi/Cloud-News')
    repo = g.get_repo(repo_name)
    
    # Get current month boundaries
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.month == 12:
        end_of_month = now.replace(year=now.year + 1, month=1, day=1) - timedelta(seconds=1)
    else:
        end_of_month = now.replace(month=now.month + 1, day=1) - timedelta(seconds=1)
    
    print(f"Collecting content from {start_of_month.strftime('%B %Y')}")
    print(f"Period: {start_of_month.date()} to {end_of_month.date()}")
    
    # Get all approved issues for the current month
    issues = repo.get_issues(
        state='open',
        labels=['newsletter', 'approved'],
        since=start_of_month
    )
    
    monthly_content = []
    
    for issue in issues:
        # Check if issue was created or updated in current month
        if (start_of_month <= issue.created_at <= end_of_month or 
            start_of_month <= issue.updated_at <= end_of_month):
            
            content_data = extract_issue_data(issue)
            if content_data:
                monthly_content.append(content_data)
                print(f"✓ Collected: {content_data['title']}")
    
    # Save monthly content
    timestamp = now.strftime("%Y%m")
    filename = f"content/monthly_content_{timestamp}.json"
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(monthly_content, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Monthly Content Summary:")
    print(f"  - Total articles: {len(monthly_content)}")
    print(f"  - Saved to: {filename}")
    
    # Create content summary
    create_content_summary(monthly_content, start_of_month)
    
    return monthly_content

def extract_issue_data(issue):
    """Extract structured data from a GitHub issue."""
    body = issue.body or ""
    
    data = {
        'issue_number': issue.number,
        'title': extract_field(body, 'Article Title'),
        'summary': extract_field(body, 'Summary'),
        'category': extract_field(body, 'Content Category'),
        'content': extract_field(body, 'Full Content'),
        'author': extract_field(body, 'Author Name'),
        'image': extract_field(body, 'Image'),
        'priority': extract_field(body, 'Priority'),
        'additional_notes': extract_field(body, 'Additional Notes'),
        'created_at': issue.created_at.isoformat(),
        'updated_at': issue.updated_at.isoformat(),
        'labels': [label.name for label in issue.labels],
        'state': issue.state,
        'url': issue.html_url
    }
    
    return data

def extract_field(body, field_name):
    """Extract a specific field from the issue body."""
    patterns = [
        rf'{field_name}:\s*(.+?)(?=\n[A-Z][a-z]+:|$)',
        rf'{field_name}\s*\n(.+?)(?=\n[A-Z][a-z]+:|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return ""

def create_content_summary(content, month_date):
    """Create a summary of the monthly content."""
    summary = {
        'month': month_date.strftime('%B %Y'),
        'total_articles': len(content),
        'categories': {},
        'authors': {},
        'priorities': {}
    }
    
    for article in content:
        # Count categories
        category = article.get('category', 'Unknown')
        summary['categories'][category] = summary['categories'].get(category, 0) + 1
        
        # Count authors
        author = article.get('author', 'Unknown')
        summary['authors'][author] = summary['authors'].get(author, 0) + 1
        
        # Count priorities
        priority = article.get('priority', 'Normal')
        summary['priorities'][priority] = summary['priorities'].get(priority, 0) + 1
    
    # Save summary
    timestamp = month_date.strftime("%Y%m")
    filename = f"content/monthly_summary_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"  - Summary saved to: {filename}")
    
    return summary

def main():
    """Main function to collect monthly content."""
    print("📰 Collecting Monthly Newsletter Content")
    print("=" * 50)
    
    content = get_monthly_content()
    
    if not content:
        print("\n⚠️  No approved content found for this month.")
        print("   Consider extending the deadline or encouraging more submissions.")
    else:
        print(f"\n✅ Successfully collected {len(content)} articles for the monthly newsletter!")

if __name__ == "__main__":
    main()

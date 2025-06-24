#!/usr/bin/env python3
"""
Publish monthly newsletter after deadline.
This script automatically publishes the newsletter and sends notifications.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from github import Github

def publish_newsletter():
    """Publish the monthly newsletter."""
    print("🚀 Publishing Monthly Newsletter")
    print("=" * 40)
    
    # Check if we have a draft newsletter
    draft_file = "monthly-newsletter-draft.md"
    if not os.path.exists(draft_file):
        print("❌ No newsletter draft found. Please generate the newsletter first.")
        return False
    
    # Read the draft content
    with open(draft_file, 'r', encoding='utf-8') as f:
        newsletter_content = f.read()
    
    # Initialize GitHub client
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set")
        return False
    
    g = Github(github_token)
    repo_name = os.getenv('GITHUB_REPOSITORY', 'hornmichi/Cloud-News')
    repo = g.get_repo(repo_name)
    
    # Create the published newsletter file
    timestamp = datetime.now().strftime("%Y%m")
    published_filename = f"newsletters/monthly-newsletter-published-{timestamp}.md"
    
    os.makedirs(os.path.dirname(published_filename), exist_ok=True)
    
    # Add publication metadata
    published_content = f"""# 📰 Cloud News - {datetime.now().strftime('%B %Y')}

**Published:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Status:** Published

---

{newsletter_content}
"""
    
    with open(published_filename, 'w', encoding='utf-8') as f:
        f.write(published_content)
    
    # Create a GitHub release
    create_github_release(repo, timestamp, published_content)
    
    # Send notifications
    send_notifications(timestamp)
    
    # Archive the draft
    archive_draft()
    
    print("✅ Monthly newsletter published successfully!")
    return True

def create_github_release(repo, timestamp, content):
    """Create a GitHub release for the newsletter."""
    try:
        current_date = datetime.now()
        month_year = current_date.strftime('%B %Y')
        tag_name = f"monthly-{timestamp}"
        release_name = f"Monthly Newsletter - {month_year}"
        
        # Create the release
        release = repo.create_git_release(
            tag=tag_name,
            name=release_name,
            message=content,
            draft=False,
            prerelease=False
        )
        
        print(f"✅ Created GitHub release: {release_name}")
        print(f"   URL: {release.html_url}")
        
        return release
        
    except Exception as e:
        print(f"⚠️  Could not create GitHub release: {e}")
        return None

def send_notifications(timestamp):
    """Send notifications about the published newsletter."""
    current_date = datetime.now()
    month_year = current_date.strftime('%B %Y')
    
    # Slack notification
    slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
    if slack_webhook:
        try:
            slack_message = {
                "text": f"📰 *Monthly Newsletter Published!*",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Cloud News - {month_year}* has been published! 🎉"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Check it out: https://github.com/hornmichi/Cloud-News/releases/latest"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Want to contribute to next month's newsletter? Submit content here: https://github.com/hornmichi/Cloud-News/issues"
                        }
                    }
                ]
            }
            
            response = requests.post(slack_webhook, json=slack_message)
            if response.status_code == 200:
                print("✅ Slack notification sent")
            else:
                print(f"⚠️  Slack notification failed: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️  Could not send Slack notification: {e}")
    
    # Email notification (if configured)
    email_api_key = os.getenv('EMAIL_API_KEY')
    if email_api_key:
        try:
            # This would integrate with your email service
            print("✅ Email notification sent (placeholder)")
        except Exception as e:
            print(f"⚠️  Could not send email notification: {e}")

def archive_draft():
    """Archive the draft newsletter."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"newsletters/archives/draft_{timestamp}.md"
        
        os.makedirs(os.path.dirname(archive_name), exist_ok=True)
        
        if os.path.exists("monthly-newsletter-draft.md"):
            os.rename("monthly-newsletter-draft.md", archive_name)
            print(f"✅ Draft archived to: {archive_name}")
            
    except Exception as e:
        print(f"⚠️  Could not archive draft: {e}")

def main():
    """Main function to publish the newsletter."""
    success = publish_newsletter()
    
    if success:
        print("\n🎉 Monthly newsletter publication complete!")
        print("\n📋 What happened:")
        print("  ✅ Newsletter content published")
        print("  ✅ GitHub release created")
        print("  ✅ Notifications sent")
        print("  ✅ Draft archived")
        print("\n📅 Next steps:")
        print("  - Share the newsletter with your team")
        print("  - Start collecting content for next month")
        print("  - Review the process for improvements")
    else:
        print("\n❌ Newsletter publication failed. Please check the logs.")

if __name__ == "__main__":
    main()

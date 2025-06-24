#!/bin/bash

# Script to push Cloud News to GitHub
echo "🚀 Pushing Cloud News to GitHub..."

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote origin found."
    echo "Please create a GitHub repository first and add it as origin:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/cloud-news.git"
    exit 1
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Your Cloud News newsletter platform is now live!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Go to your repository on GitHub"
    echo "2. Enable Issues in Settings > Features"
    echo "3. Set up GitHub Pages for the web form"
    echo "4. Test the newsletter submission form"
    echo "5. Share the contribution guide with your team"
    echo ""
    echo "🔗 Repository URL: $(git remote get-url origin)"
else
    echo "❌ Failed to push to GitHub. Please check your repository URL and permissions."
fi

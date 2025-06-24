# Cloud News - Newsletter Platform

A self-service newsletter platform that allows both technical and non-technical team members to contribute content easily through GitHub.

## 🚀 Quick Start for Contributors

### For Non-Technical Users

1. **Submit Content via GitHub Issues** (Recommended)
   - Go to the [Issues tab](https://github.com/hornmichi/cloud-news/issues)
   - Click "New Issue"
   - Select "Newsletter Content Submission" template
   - Fill out the form and submit

2. **Submit Content via Web Form**
   - Visit our [Newsletter Submission Form](https://hornmichi.github.io/cloud-news/)
   - Fill out the form
   - Submit - it automatically creates a GitHub issue

### For Technical Users

- Create pull requests with content in the `content/` directory
- Follow the content structure guidelines
- Use the provided templates

## 📋 Content Guidelines

### What You Can Submit

- **Articles**: Insights, updates, or stories
- **Announcements**: Company news, events, updates
- **Spotlights**: Team members, projects, achievements
- **Tips & Tricks**: Helpful advice or best practices
- **Industry News**: Relevant external news or trends

### Content Requirements

- **Title**: Clear, engaging headline (max 60 characters)
- **Summary**: Brief 2-3 sentence description
- **Content**: Full article text (300-500 words recommended)
- **Author**: Your name and role
- **Category**: Choose from available categories
- **Image**: Optional - URL or description

## 📅 Newsletter Schedule

- **Publication**: Every month
- **Submission Deadline**: Last day of the month
- **Review Period**: 2-3 business days

## 🛠️ For Newsletter Editors

### Automated Workflows

- **Content Collection**: GitHub Issues are automatically processed
- **Content Review**: Automated notifications for new submissions
- **Newsletter Generation**: Automated newsletter creation from approved content
- **Distribution**: Automated email distribution

### Manual Processes

- Content review and approval
- Newsletter formatting and final edits
- Quality assurance

## 📁 Repository Structure

```
cloud-news/
├── .github/
│   ├── ISSUE_TEMPLATE/          # GitHub issue templates
│   └── workflows/               # GitHub Actions workflows
├── content/                     # Newsletter content files
├── templates/                   # Newsletter templates
├── scripts/                     # Automation scripts
├── web-form/                    # Web submission form
└── docs/                        # Documentation
```

## 🔧 Setup Instructions

### Prerequisites

- Node.js 18+ (for web form)
- Python 3.8+ (for automation scripts)
- GitHub repository with Issues enabled

### Installation

1. Clone the repository
2. Install dependencies: `npm install` and `pip install -r requirements.txt`
3. Configure GitHub secrets for automation
4. Set up web form hosting (GitHub Pages recommended)

## 📖 Documentation

- [Contribution Guide](docs/CONTRIBUTION_GUIDE.md)
- [Editor Guide](docs/EDITOR_GUIDE.md)
- [Technical Setup](docs/TECHNICAL_SETUP.md)
- [Content Guidelines](docs/CONTENT_GUIDELINES.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contribution Guide](docs/CONTRIBUTION_GUIDE.md) for details.

## 📞 Support

- **Questions**: Create an issue with the "Question" label
- **Technical Issues**: Create an issue with the "Bug" label
- **Content Ideas**: Check our content calendar or brainstorm with the team

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for easy newsletter collaboration**

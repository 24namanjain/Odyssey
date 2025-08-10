# Odyssey Documentation

A comprehensive knowledge base covering cloud infrastructure, system design, and development practices. Built with MkDocs Material for optimal learning and retention.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd Odyssey

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the documentation server
mkdocs serve
```

### Access Documentation
- **Local**: http://127.0.0.1:8000
- **Build static site**: `mkdocs build`
- **Deploy to GitHub Pages**: `mkdocs gh-deploy`

## 🏷️ Content Organization

### Guides vs Commands vs References
- **Guides** (`*/guides/`): Step-by-step tutorials and conceptual explanations
- **Commands** (`*/commands/`): Copy-paste command references and cheat sheets
- **References** (`*/references/`): Quick lookups, diagrams, and formulas
- **Manifests** (`*/manifests/`): YAML configurations and deployment files

### Personal Workspace
- **Links** (`_personal/links.md`): Important bookmarks and resources
- **TODO** (`_personal/todo.md`): Actionable tasks and learning goals

## 🏷️ Tagging System

Add tags to any page using YAML front matter:

```yaml
---
title: Page Title
tags: [tag1, tag2, tag3]
---
```

### Common Tags
- **Technology**: `kubernetes`, `docker`, `system-design`
- **Type**: `guides`, `commands`, `setup`, `troubleshooting`
- **Level**: `beginner`, `intermediate`, `advanced`
- **Domain**: `networking`, `storage`, `security`, `monitoring`

## 🤖 AI Assistant Instructions

When adding new documentation content, the AI assistant should automatically handle these tasks:

### 📋 **Required Actions for New Content**

#### **For New Markdown Files:**
1. **Add YAML Front Matter** with title and tags:
   ```yaml
   ---
   title: Page Title
   tags: [relevant, tags, here]
   ---
   ```

2. **Update Navigation** in `mkdocs.yml`:
   - Add entry to appropriate section
   - Maintain logical ordering
   - Use descriptive titles

3. **Update Index** in `docs/index.md`:
   - Add link to new content
   - Update directory structure diagram
   - Maintain alphabetical/chronological order

4. **Add Tags** for discoverability:
   - Technology tags: `kubernetes`, `docker`, `system-design`
   - Type tags: `guides`, `commands`, `setup`, `troubleshooting`
   - Level tags: `beginner`, `intermediate`, `advanced`
   - Domain tags: `networking`, `storage`, `security`, `monitoring`

#### **For New YAML/Config Files:**
1. **Create Markdown Wrapper** (`.md`) with:
   - Syntax-highlighted YAML content in code blocks
   - Usage instructions and examples
   - Download link to original file: `[📥 Download YAML file](filename.yaml)`
   - Proper tags: `[technology, yaml, manifests, config]`

2. **Update Navigation** to point to `.md` wrapper, not `.yaml` file

3. **Preserve Original File** for direct use with tools

#### **For New Technology Areas:**
1. **Create Directory Structure**:
   ```
   Technology/
   ├── guides/
   │   └── README.md
   ├── commands/
   │   └── README.md
   └── manifests/
       └── README.md
   ```

2. **Add to Navigation** in `mkdocs.yml`:
   ```yaml
   - Technology Name:
     - Guides:
       - Overview: Technology/guides/README.md
     - Commands:
       - Overview: Technology/commands/README.md
     - Manifests:
       - Overview: Technology/manifests/README.md
   ```

3. **Update Index** in `docs/index.md`

#### **For Personal Workspace Updates:**
1. **Links** (`_personal/links.md`):
   - Use proper nested list format
   - Add descriptive text for each link
   - Organize by category with bold headers

2. **TODO** (`_personal/todo.md`):
   - Use checkbox format: `- [ ] Task description`
   - Add context and priority if needed

### 🔍 **Quality Checks**

#### **Before Committing:**
1. **Test Build**: `mkdocs build --strict`
2. **Check Navigation**: Verify all links work
3. **Validate Tags**: Ensure tags are consistent and searchable
4. **Review Structure**: Confirm proper organization
5. **Test Links**: Verify download links work for YAML files

#### **Common Issues to Fix:**
- Missing YAML front matter
- Broken navigation links
- Inconsistent tag naming
- YAML files not wrapped in Markdown
- Missing download buttons for config files
- Improper nested list formatting

### 📝 **Template for New Content**

#### **Guide Template:**
```markdown
---
title: Guide Title
tags: [technology, type, level, domain]
---

# Guide Title

## Overview
Brief description of what this guide covers.

## Prerequisites
What users need before starting.

## Steps
1. Step one
2. Step two
3. Step three

## Summary
Key takeaways and next steps.
```

#### **Commands Template:**
```markdown
---
title: Commands Reference
tags: [technology, commands, cli, type]
---

# Commands Reference

## Basic Commands
```bash
command --option value
```

## Examples
```bash
# Example usage
command --option value
```

## Common Options
- `--option`: Description
- `--flag`: Description
```

#### **Manifest Template:**
```markdown
---
title: Configuration Name
tags: [technology, yaml, manifests, config]
---

# Configuration Name

## Configuration
```yaml
# YAML content here
```

## Usage
```bash
# How to use this config
```

## Download
[📥 Download YAML file](filename.yaml)
```

### 🚀 **Automation Checklist**

When adding content, automatically:
- [ ] Add YAML front matter with title and tags
- [ ] Update `mkdocs.yml` navigation
- [ ] Update `docs/index.md` structure
- [ ] Create Markdown wrappers for YAML files
- [ ] Add download links for config files
- [ ] Test build with `mkdocs build --strict`
- [ ] Commit with descriptive message
- [ ] Verify tags appear in search and tag index

## 🔧 Development

### Local Development
```bash
# Start development server with live reload
mkdocs serve

# Build static site
mkdocs build

# Validate configuration
mkdocs build --strict
```

## 🚀 Deployment

### GitHub Pages
```bash
# Deploy to GitHub Pages
mkdocs gh-deploy
```

---

**Happy Learning! 🎓**
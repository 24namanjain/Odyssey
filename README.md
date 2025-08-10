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

## 📚 Documentation Structure

```
docs/
├── index.md                    # Homepage
├── tags.md                     # Tag index
├── _personal/                  # Personal workspace
│   ├── links.md               # Important links
│   └── todo.md                # TODO items
├── Docker/                     # Docker documentation
│   ├── guides/                # Conceptual guides
│   │   ├── 1-docker-introduction.md
│   │   └── 3-debugging-a-container.md
│   └── commands/              # Command references
│       └── 2-docker-basic-commands.md
├── Kubernetes/                 # Kubernetes documentation
│   ├── guides/                # Conceptual guides
│   │   ├── 1-kubernetes-introduction.md
│   │   ├── 2-main-kube-components.md
│   │   ├── 3-k8s-architecture.md
│   │   ├── 4-local-k8s-setup.md
│   │   ├── 6-control-plane-components.md
│   │   ├── 8-mutli-node-cluster-with-kind.md
│   │   └── 9-running-your-containers-in-kube.md
│   ├── commands/              # Command references
│   │   ├── 5-basic-kubectl-commands.md
│   │   └── 7-minikube-cluster-cmds.md
│   └── manifests/             # YAML configurations
│       ├── kind-multi-node-cluster.yaml
│       ├── nginx-deployment.yaml
│       └── nginx-pod.yaml
└── SystemDesign/              # System design documentation
    ├── guides/                # Design guides
    │   └── README.md
    └── references/            # Quick references
        └── README.md
```

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

### Viewing Tags
- **Tags page**: Browse all tagged content
- **Search**: Tags are included in search results
- **Visual**: Tag chips appear above page titles

## 📝 Adding Content

### New Guide
1. Create file in appropriate `*/guides/` directory
2. Add YAML front matter with title and tags
3. Update navigation in `mkdocs.yml`
4. Add link to `docs/index.md`

### New Commands Reference
1. Create file in appropriate `*/commands/` directory
2. Focus on copy-paste commands with examples
3. Add tags for easy discovery

### New Technology Area
1. Create directory structure: `Technology/{guides,commands,manifests}`
2. Add to navigation in `mkdocs.yml`
3. Update `docs/index.md`

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

### Adding Dependencies
```bash
# Add new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

## 🎯 Best Practices

### Content Guidelines
- **Guides**: Narrative, step-by-step, with context
- **Commands**: Terse, copy-paste ready, with examples
- **References**: Concise, scannable, high-signal
- **Tags**: 3-6 per page, consistent naming

### File Naming
- Use descriptive names: `1-kubernetes-introduction.md`
- Prefix with numbers for ordering
- Use kebab-case for URLs

### Navigation
- Keep navigation shallow (max 3 levels)
- Group related content logically
- Use clear, descriptive titles

## 🚀 Deployment

### GitHub Pages
```bash
# Deploy to GitHub Pages
mkdocs gh-deploy

# Deploy with custom branch
mkdocs gh-deploy --remote-branch custom-branch
```

### Custom Domain
1. Add `CNAME` file to `docs/` directory
2. Configure in `mkdocs.yml`:
   ```yaml
   site_url: https://yourdomain.com
   ```

## 🤝 Contributing

1. Create feature branch
2. Add content following structure guidelines
3. Update navigation and tags
4. Test locally with `mkdocs serve`
5. Submit pull request

## 📄 License

This documentation is for personal learning and reference.

---

**Happy Learning! 🎓**
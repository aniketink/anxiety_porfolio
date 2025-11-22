# Portfolio CMS

A custom offline content management system for your portfolio with LaTeX support and Obsidian-like features.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd cms
   pip install -r requirements.txt
   ```

2. **Start the CMS:**
   ```bash
   python main.py
   ```

3. **Open in browser:**
   Navigate to http://localhost:8000

## Features

- ✅ Full CRUD for projects, garden notes, and research papers
- ✅ Auto-commit to git on every save
- ✅ LaTeX rendering ($inline$ and $$block$$)
- ✅ [[Wiki-style]] backlinks
- ✅ Real-time search
- ✅ Markdown preview
- ✅ Dark theme
- ✅ Auto-save drafts

## Usage

1. **Select content type** from the sidebar (Projects/Garden/Research)
2. **Click existing content** to edit or click "+ New Content" to create
3. **Edit in the left pane**, preview in the right (toggle with "👁 Preview")
4. **Save** to commit changes automatically to git
5. **Deploy** by running `npm run deploy` from the main directory

## Keyboard Shortcuts

- `Ctrl/Cmd + S`: Save
- `Ctrl/Cmd + P`: Toggle preview

## File Structure

- `main.py` - FastAPI server
- `git_manager.py` - Git integration
- `content_parser.py` - Markdown/LaTeX parser
- `models.py` - Data models
- `config.json` - Configuration
- `frontend/dist/` - UI assets

## Note

Content is stored in your existing Astro project structure:
- `src/content/projects/`
- `src/content/garden/`
- `src/content/research/`

All changes are automatically committed to git with descriptive messages.

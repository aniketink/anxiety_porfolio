from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import json
from typing import List
from models import ContentMetadata
from git_manager import GitManager
from content_parser import ContentParser
from datetime import datetime
import os

app = FastAPI(title="Portfolio CMS")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Initialize managers
git_manager = GitManager(str(SCRIPT_DIR.parent))
parser = ContentParser()

# Get content directories
CONTENT_DIRS = config["content_dirs"]
BASE_PATH = SCRIPT_DIR.parent  # Parent of cms directory


def get_content_path(content_type: str) -> Path:
    """Get full path for content type"""
    return BASE_PATH / CONTENT_DIRS[content_type]


def read_content_file(path: Path) -> dict:
    """Read and parse a content file"""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata, body = parser.parse_markdown(content)
    backlinks = parser.extract_backlinks(body)
    
    return {
        "filename": path.stem,
        "path": str(path.relative_to(BASE_PATH)),
        "metadata": metadata,
        "body": body,
        "backlinks": backlinks,
        "word_count": parser.word_count(body),
        "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat()
    }


@app.get("/api")
async def root():
    return {"message": "Portfolio CMS API", "version": "1.0.0"}


@app.get("/api/content/{content_type}")
async def list_content(content_type: str):
    """List all content of a specific type"""
    if content_type not in CONTENT_DIRS:
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    content_path = get_content_path(content_type)
    
    if not content_path.exists():
        return []
    
    content_list = []
    for file_path in content_path.glob("*.md*"):
        try:
            data = read_content_file(file_path)
            content_list.append(data)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Sort by modified date
    content_list.sort(key=lambda x: x["modified"], reverse=True)
    return content_list


@app.get("/api/content/{content_type}/{filename}")
async def get_content(content_type: str, filename: str):
    """Get specific content file"""
    if content_type not in CONTENT_DIRS:
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    content_path = get_content_path(content_type)
    file_path = content_path / f"{filename}.md"
    
    if not file_path.exists():
        file_path = content_path / f"{filename}.mdx"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Content not found")
    
    return read_content_file(file_path)


@app.post("/api/content/{content_type}")
async def create_content(content_type: str, title: str, body: str, metadata: dict):
    """Create new content"""
    if content_type not in CONTENT_DIRS:
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    content_path = get_content_path(content_type)
    content_path.mkdir(parents=True, exist_ok=True)
    
    # Generate filename from title
    filename = title.lower().replace(" ", "-").replace("/", "-")
    filename = "".join(c for c in filename if c.isalnum() or c == "-")
    file_path = content_path / f"{filename}.md"
    
    # Create frontmatter + body
    full_content = parser.create_frontmatter(metadata)
    full_content += f"\n{body}"
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    # Git commit if enabled
    if config["git"]["auto_commit"]:
        git_manager.commit_file(
            str(file_path.relative_to(BASE_PATH)),
            content_type,
            title
        )
    
    return {"success": True, "filename": filename}


@app.put("/api/content/{content_type}/{filename}")
async def update_content(content_type: str, filename: str, body: str, metadata: dict):
    """Update existing content"""
    if content_type not in CONTENT_DIRS:
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    content_path = get_content_path(content_type)
    file_path = content_path / f"{filename}.md"
    
    if not file_path.exists():
        file_path = content_path / f"{filename}.mdx"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Create frontmatter + body
    full_content = parser.create_frontmatter(metadata)
    full_content += f"\n{body}"
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    # Git commit if enabled
    if config["git"]["auto_commit"]:
        git_manager.commit_file(
            str(file_path.relative_to(BASE_PATH)),
            content_type,
            metadata.get("title", filename)
        )
    
    return {"success": True}


@app.delete("/api/content/{content_type}/{filename}")
async def delete_content(content_type: str, filename: str):
    """Delete content"""
    if content_type not in CONTENT_DIRS:
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    content_path = get_content_path(content_type)
    file_path = content_path / f"{filename}.md"
    
    if not file_path.exists():
        file_path = content_path / f"{filename}.mdx"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Content not found")
    
    file_path.unlink()
    
    # Git commit deletion
    if config["git"]["auto_commit"]:
        git_manager.repo.index.remove([str(file_path.relative_to(BASE_PATH))])
        git_manager.repo.index.commit(f"Delete {content_type}: {filename}")
    
    return {"success": True}


@app.get("/api/git/status")
async def git_status():
    """Get git status"""
    return git_manager.get_status()


@app.get("/api/git/history/{content_type}/{filename}")
async def git_history(content_type: str, filename: str):
    """Get file commit history"""
    file_path = f"{CONTENT_DIRS[content_type]}/{filename}.md"
    return git_manager.get_file_history(file_path)


@app.get("/api/search")
async def search(query: str):
    """Search across all content"""
    results = []
    query_lower = query.lower()
    
    for content_type in CONTENT_DIRS:
        content_path = get_content_path(content_type)
        if not content_path.exists():
            continue
            
        for file_path in content_path.glob("*.md*"):
            try:
                data = read_content_file(file_path)
                # Search in title, body, and tags
                if (query_lower in data["metadata"].get("title", "").lower() or
                    query_lower in data["body"].lower() or
                    any(query_lower in tag.lower() for tag in data["metadata"].get("tags", []))):
                    data["type"] = content_type
                    results.append(data)
            except Exception as e:
                continue
    
    return results


# Serve frontend
FRONTEND_PATH = SCRIPT_DIR / "frontend" / "dist"
app.mount("/", StaticFiles(directory=str(FRONTEND_PATH), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config["server"]["host"],
        port=config["server"]["port"],
        reload=True
    )

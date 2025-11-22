import git
import json
from pathlib import Path
from datetime import datetime


class GitManager:
    def __init__(self, repo_path: str = ".."):
        self.repo_path = Path(repo_path)
        self.repo = git.Repo(self.repo_path)
        
    def commit_file(self, file_path: str, content_type: str, title: str, custom_message: str = None):
        """Commit a single file with auto-generated or custom message"""
        try:
            # Add the file
            self.repo.index.add([file_path])
            
            # Generate commit message
            if custom_message:
                message = custom_message
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                message = f"Update {content_type}: {title} ({timestamp})"
            
            # Commit
            self.repo.index.commit(message)
            return {"success": True, "message": message}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_file_history(self, file_path: str, limit: int = 10):
        """Get commit history for a specific file"""
        try:
            commits = list(self.repo.iter_commits(paths=file_path, max_count=limit))
            history = []
            for commit in commits:
                history.append({
                    "hash": commit.hexsha[:7],
                    "message": commit.message.strip(),
                    "author": str(commit.author),
                    "date": datetime.fromtimestamp(commit.committed_date).isoformat()
                })
            return history
        except Exception as e:
            return []
    
    def get_status(self):
        """Get current git status"""
        return {
            "branch": self.repo.active_branch.name,
            "modified": [item.a_path for item in self.repo.index.diff(None)],
            "untracked": self.repo.untracked_files
        }

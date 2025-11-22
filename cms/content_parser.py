import frontmatter
import re
from pathlib import Path
from typing import List, Dict, Tuple
from markdown_it import MarkdownIt


class ContentParser:
    def __init__(self):
        self.md = MarkdownIt()
        
    def parse_markdown(self, content: str) -> Tuple[Dict, str]:
        """Parse frontmatter and body from markdown content"""
        post = frontmatter.loads(content)
        return dict(post.metadata), post.content
    
    def extract_backlinks(self, content: str) -> List[str]:
        """Extract [[wiki-style]] backlinks from content"""
        pattern = r'\[\[([^\]]+)\]\]'
        matches = re.findall(pattern, content)
        return list(set(matches))  # Remove duplicates
    
    def extract_tags(self, content: str, frontmatter_tags: List[str] = None) -> List[str]:
        """Extract tags from frontmatter and #hashtags from content"""
        tags = set(frontmatter_tags or [])
        
        # Extract #hashtags
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, content)
        tags.update(hashtags)
        
        return list(tags)
    
    def render_latex(self, content: str) -> str:
        """Prepare content for LaTeX rendering (mark LaTeX blocks)"""
        # Inline math: $...$
        content = re.sub(
            r'\$([^\$]+)\$',
            r'<span class="latex-inline">\1</span>',
            content
        )
        
        # Block math: $$...$$
        content = re.sub(
            r'\$\$([^\$]+)\$\$',
            r'<div class="latex-block">\1</div>',
            content,
            flags=re.DOTALL
        )
        
        return content
    
    def word_count(self, content: str) -> int:
        """Count words in content"""
        # Remove code blocks
        content = re.sub(r'```[\s\S]*?```', '', content)
        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)
        # Count words
        words = re.findall(r'\b\w+\b', content)
        return len(words)
    
    def create_frontmatter(self, data: Dict) -> str:
        """Create frontmatter string from data"""
        post = frontmatter.Post('', **data)
        return frontmatter.dumps(post)

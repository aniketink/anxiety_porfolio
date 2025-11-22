from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


# Simple data structures
@dataclass
class ContentMetadata:
    filename: str
    path: str
    type: str  # project, garden, research
    modified: datetime
    word_count: int
    backlinks: List[str] = field(default_factory=list)


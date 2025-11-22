from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ContentBase(BaseModel):
    title: str
    body: str
    tags: List[str] = []
    

class Project(ContentBase):
    description: str
    date: str
    status: str  # Active, Completed, Archived
    

class GardenNote(ContentBase):
    date: str
    

class ResearchPaper(ContentBase):
    description: str
    date: str
    pdf: Optional[str] = None


class ContentMetadata(BaseModel):
    filename: str
    path: str
    type: str  # project, garden, research
    modified: datetime
    word_count: int
    backlinks: List[str] = []

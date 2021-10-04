from typing import Optional
from pydantic import BaseModel

class Authors(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str

class Books(BaseModel):
    title: str
    author_id: int
    description: Optional[str] = None

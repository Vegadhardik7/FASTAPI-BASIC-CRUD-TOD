from uuid import uuid4
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator

# Create Book
class BookModel(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = "English"
    published_date: Optional[str] = None

    # validation for the published data parameter
    @field_validator("published_date")
    def validate_pusblised_date(cls, value):
        try:
            # Ensure the format is YYYY-MM-DD and it's a valid calendar date
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("published_date must be a valid date in the format YYYY-MM-DD")
        return value

class BOOKS:
    def __init__(self, title: Optional[str], author: Optional[str], publisher: Optional[str], 
                 published_date: Optional[str], page_count: Optional[int], language: Optional[str]):
        
        self.id = str(uuid4())
        self.title = title 
        self.author = author
        self.publisher = publisher
        self.published_date = published_date
        self.page_count = page_count
        self.language= language
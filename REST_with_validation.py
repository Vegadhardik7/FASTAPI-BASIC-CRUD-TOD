from uuid import uuid4
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

books = [
    {
      "id": "1",
      "title": "To Kill a Mockingbird",
      "author": "Harper Lee",
      "publisher": "J.B. Lippincott & Co.",
      "published_date": "1960-07-11",
      "page_count": 281,
      "language": "English"
    },
    {
      "id": "2",
      "title": "1984",
      "author": "George Orwell",
      "publisher": "Secker & Warburg",
      "published_date": "1949-06-08",
      "page_count": 328,
      "language": "English"
    },
    {
      "id": "3",
      "title": "Pride and Prejudice",
      "author": "Jane Austen",
      "publisher": "T. Egerton, Whitehall",
      "published_date": "1813-01-28",
      "page_count": 279,
      "language": "English"
    },
    {
      "id": "4",
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "publisher": "Charles Scribner's Sons",
      "published_date": "1925-04-10",
      "page_count": 180,
      "language": "English"
    },
    {
      "id": "5",
      "title": "Moby-Dick",
      "author": "Herman Melville",
      "publisher": "Harper & Brothers",
      "published_date": "1851-10-18",
      "page_count": 635,
      "language": "English"
    }
]

app = FastAPI()

# List all the books
@app.get("/", response_class=JSONResponse)
async def getAllBooks():
    return books

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
        
@app.post("/createBook", response_class=JSONResponse)
async def createBook(newbook: BookModel):
    newbook_data = BOOKS(title=newbook.title, author=newbook.author, publisher=newbook.publisher, 
                         published_date=newbook.published_date, page_count=newbook.page_count, 
                         language=newbook.language or "English")
    
    books.append(newbook_data.__dict__) # Convert the BOOKS object to a dictionary before appending

    return {"message": "Book created successfully", "data": newbook_data}

# Update Books based on User ID
@app.put("/updatebook/{book_id}", response_class=JSONResponse)
async def updateBook(book_id: str, book: BookModel):
    for bk in books:
        if bk["id"] == book_id:
            if book.title is not None:
                bk["title"] = book.title
            if book.author is not None:
                bk["author"] = book.author
            if book.publisher is not None:
                bk["publisher"] = book.publisher
            if book.published_date is not None:
                bk["published_date"] = book.published_date
            if book.page_count is not None:
                bk["page_count"] = book.page_count
            if book.language is not None:
                    bk["language"] = book.language
            return {"message": "User updated successfully", "data": bk}
        
     # If user is not found, raise a 404 error
    raise HTTPException(status_code=404, detail=f"User with ID '{book_id}' not found") 

# delete a user based on id
@app.delete("/delete/{book_id}",response_class=JSONResponse)
async def deleteBook(book_id: str):
    for bk in books:
        if str(bk["id"]) == book_id:
            books.remove(bk)
            return {"message": "User deleted successfully"}
    
    # If no user is found with the given ID, raise a 404 error
    raise HTTPException(status_code=404, detail=f"User with ID '{book_id}' not found")

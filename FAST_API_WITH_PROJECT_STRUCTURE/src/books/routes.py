from src.books.book_data import books
from src.books.schemas import BookModel, BOOKS
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

book_router = APIRouter()

# List all the books
@book_router.get("/", response_class=JSONResponse)
async def getAllBooks():
    return books

# List the book data by id
@book_router.get("/{book_id}", response_class=JSONResponse)
async def getBook(book_id: str):
    for bk in books:
        if bk["id"] == book_id:
            return bk
        
    raise HTTPException(status_code=500, detail=f"User with ID '{book_id}' not found")

# Insert Book data
@book_router.post("/createBook", response_class=JSONResponse)
async def createBook(newbook: BookModel):
    newbook_data = BOOKS(title=newbook.title, author=newbook.author, publisher=newbook.publisher, 
                         published_date=newbook.published_date, page_count=newbook.page_count, 
                         language=newbook.language or "English")
    
    books.append(newbook_data.__dict__) # Convert the BOOKS object to a dictionary before appending

    return {"message": "Book created successfully", "data": newbook_data}

# Update Books based on User ID
@book_router.put("/updatebook/{book_id}", response_class=JSONResponse)
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
@book_router.delete("/delete/{book_id}",response_class=JSONResponse)
async def deleteBook(book_id: str):
    for bk in books:
        if str(bk["id"]) == book_id:
            books.remove(bk)
            return {"message": "User deleted successfully"}
    
    # If no user is found with the given ID, raise a 404 error
    raise HTTPException(status_code=404, detail=f"User with ID '{book_id}' not found")
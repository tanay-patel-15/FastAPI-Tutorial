from fastapi import FastAPI, HTTPException, Path, Query, status 
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
  id: int
  book_name: str
  author: str
  publisher: Optional[str] = None

class UpdateBook(BaseModel):
  id: Optional[int] = None
  book_name: Optional[str]  = None
  author: Optional[str] = None
  publisher: Optional[str] = None

books = {}

# CREATE
@app.post("/books/create/{book_id}")
def create_book(*, book_id: int=Path(description="The ID of the new book", ge=0), book: Book):
    if book_id in books:
        raise HTTPException(status_code=409, detail="Book with this ID already exists.")
    else:
      books[book_id] = book
      return books[book_id]

# READ
@app.get("/books/read/{book_id}")
def get_book(book_id: int):
  if book_id not in books:
    raise HTTPException(status_code=404, detail="Book with this ID does not exist.")
  else:
    return books[book_id]
  

# UPDATE
@app.put("/books/update/{book_id}")
def update_book(book_id: int, book: UpdateBook):
  if book_id not in books:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book with this ID does not exist.")
  
  if  book.id != None:
    books[book_id].id = book.id

  if  book.book_name != None:
    books[book_id].book_name = book.book_name

  if  book.author != None:
    books[book_id].author = book.author

  if  book.publisher != None:
    books[book_id].publisher = book.publisher

  return books[book_id]


# DELETE
@app.delete("/books/remove/{book_id}")
def remove_book(book_id: int):
  if book_id not in books:
    raise HTTPException(status_code=404, detail="Book not found")
  del books[book_id]
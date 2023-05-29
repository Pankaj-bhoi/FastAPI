from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

# v-64
class BOOK:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

# v-67
class BookRequest(BaseModel):
    id: Optional[int] = Field(title='Id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=5)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0,lt=6)
    published_date: int = Field(gt=1996, lt=2030)

    # v-69 (Pydantic configuration)
    class Config:
        schema_extra = {
            'example':{
                'title':'A new Book',
                'author':'codingwithmac',
                'description':'A new description of a book',
                'rating': 5,
                'published_date':2025
            }
        }


# v-64
books = [
    BOOK(1,'title one','author 1','description one',4,2015),
    BOOK(2,'title two','author 1','description two',2,1997),
    BOOK(3,'title three','author 3','description three',5,2010),
    BOOK(4,'title four','author 4','description four',1,2017),
    BOOK(5,'title five','author 5','description five',2,2018),
    BOOK(6,'title six','author 6','description six',3,2018)
]

# v-64 (get request)
@app.get('/books', status_code=status.HTTP_200_OK) #v-80 Explicit Status Code Responses
async def read_all_books():
    return books

# v-65 (post request with out validation)
@app.post('/create_book',status_code=status.HTTP_201_CREATED) #v-80 Explicit Status Code Responses
async def create_book(book_request=Body()):
    books.append(book_request)

# v-67 (post request with validation)
@app.post('/create_book_validation/',status_code=status.HTTP_201_CREATED) #v-80 Explicit Status Code Responses
async def create_book(book_request: BookRequest):
    new_book = find_book_id(BOOK(**book_request.dict()))
    books.append(new_book)

def find_book_id(book: BOOK):

    if len(books)>0:
        book.id = books[-1].id + 1
    else:
        book.id = 1

    # ternary operator
    # book.id = 1 if len(books)==0 else books[-1].id + 1
    return book

# v-70 (fetch book)
@app.get('/get_book/{book_id}',status_code=status.HTTP_200_OK) #v-80 Explicit Status Code Responses
async def get_book_by_id(book_id : int = Path(gt=0)):
    for book in books:
        if book.id == book_id:
            return book
    # v-79 (HTTP Exception handling)
    raise HTTPException(status_code=404, detail='Item not found')

# v-71 (fetch book by rating)
@app.get('/get_book/',status_code=status.HTTP_200_OK) #v-80 Explicit Status Code Responses
async def get_book_by_rating(rating:int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in books:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return

# v-72 (put method)
@app.put('/books/update_book/',status_code=status.HTTP_204_NO_CONTENT) #v-80 Explicit Status Code Responses
async def book_update(book:BookRequest):
    book_changed = False
    for i in range(len(books)):
        if books[i].id == book.id:
            books[i] = book
            book_changed=True
    # v-79 (HTTP Exception handling)
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')

# v-73 (delete method)
@app.delete('/books/{books_id}',status_code=status.HTTP_204_NO_CONTENT) #v-80 Explicit Status Code Responses
async def delete_book(books_id: int=Path(gt=0)):
    books_changed = False
    for i in range(len(books)):
        if books[i].id == books_id:
            books.pop(i)
            books_changed=True
            break
    # v-79 (HTTP Exception handling)
    if not books_changed:
        raise HTTPException(status_code=404, detail='Item not found')

# v-75 (add published date)
@app.get('/books/publish',status_code=status.HTTP_200_OK) #v-80 Explicit Status Code Responses
async def read_books_by_published(published_date:int = Query(gt=1996, lt=2030)):
    books_to_return = []
    for book in books:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return




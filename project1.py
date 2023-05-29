from fastapi import FastAPI,Body

app = FastAPI()

# v-50
BOOKS =[
    {'title':'Title One','author':'Author One','category':'Science'},
    {'title':'Title Two','author':'Author Two','category':'Science'},
    {'title':'Title Three','author':'Author Three','category':'History'},
    {'title':'Title Four','author':'Author Four','category':'Math'},
    {'title':'Title Five','author':'Author Four','category':'Math'},
    {'title':'Title Six','author':'Author Six','category':'Math'},

]

# v-49
@app.get("/")
def first_api():
    return {"messsage":"hello world"}


# v-50
@app.get('/books/')
async def get_books():
    return BOOKS

# v-52 (path parameter)
@app.get("/books/{book_title}")
async def get_book(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        
# v-54 query parameter
@app.get('/books/category/')
async def get_books_by_category(category:str):
    books_to_returns = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_returns.append(book)
    print(books_to_returns)
    return books_to_returns

# v-54 (path and query parameter)
@app.get('/books/category/{author}')
async def get_books_by_author_category(author:str,category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and \
        book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Note
# Get cannot have a body
# command to run fast api server : uvicorn books:app --reload

# v-56 (post request)
@app.post('/books/create_book')
async def create_books(new_book=Body()):
    BOOKS.append(new_book)

# v-58 (put request)
@app.put('/books/update_book')
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book
            break

# v-60 (delete request)
@app.delete('/books/{books_title}')
async def delete_book(books_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == books_title.casefold():
            BOOKS.pop(i)
            break

'''
Assignment Solution
Get all books from a specific author using path or query parameters
'''
# 1 - Answer
# path parameter
@app.get('/assign_books/byauthor/{author}')
async def get_books_by_author(author:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    
    return books_to_return

# query parameter
@app.get('/assign_books/')
async def get_books_by_author(author:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return


    
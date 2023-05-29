from fastapi import FastAPI, Depends, Path, HTTPException
from typing_extensions import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Todos
from starlette import status
from pydantic import BaseModel, Field
app = FastAPI()

# v-90
models.Base.metadata.create_all(bind=engine)

# v-90
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# v-90
# dependency Injection
db_dependency = Annotated[Session, Depends(get_db)]

# v-92
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: bool

# v-90
@app.get('/', status_code=status.HTTP_200_OK)
async def read_all(db : db_dependency):
    return db.query(Todos).all()

# v-91
@app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def get_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')

# v-92
@app.post('/todo',status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())
    
    db.add(todo_model)
    db.commit()

# v-93
@app.put('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, 
                      todo_request: TodoRequest, 
                      todo_id: int = Path(gt=0)):
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

# v-94
@app.delete('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    
    db.commit()
    
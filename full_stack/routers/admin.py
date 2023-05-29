from fastapi import APIRouter, Depends, HTTPException, Path
from database import SessionLocal
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from models import Todos

# v-96
router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

# v-103
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# dependency Injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency  = Annotated[dict, Depends(get_current_user)]

# v-114
@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user : user_dependency, db : db_dependency):
    print(user)
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Todos).all()

# v-114
@router.delete('/delete/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user : user_dependency, db: db_dependency, todo_id : int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

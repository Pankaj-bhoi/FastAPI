from fastapi import Depends, Path, HTTPException, APIRouter
from typing_extensions import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Todos, Users
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/users',
    tags=['users']
)

# v-116
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# v-116
class UserVerification(BaseModel):
    password : str
    new_password : str = Field(min_length=6)



# v-116
# dependency Injection
db_dependency = Annotated[Session, Depends(get_db)]
# v-116
user_dependency  = Annotated[dict, Depends(get_current_user)]
# v-116
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get('/',status_code=status.HTTP_200_OK)
async def get_users( user: user_dependency, db: db_dependency ):

    if user is None:
        raise HTTPException(status_code=401, detail='Could not validate user')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Could not validate user')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()


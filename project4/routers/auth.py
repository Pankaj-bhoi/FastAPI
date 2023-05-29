from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime

# v-96
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# v-103
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# v-103
# dependency Injection
db_dependency = Annotated[Session, Depends(get_db)]


# v-102
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# v-107
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# v-104 
form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]

# v-106
SECRET_KEY = '5783371EFF31D4E423681CCCEC98F'
ALGORITHM = 'HS256'

# v-104
def authenticate_user(username: str, password: str, db):

    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user

# v-106
def create_access_token(username: str, user_id: int,role: str, expires_delta: timedelta):

    encode = {'sub': username, 'id': user_id, 'user_role':role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# v-107
async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role : str = payload.get('user_role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'username':username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')


# v-106
class Token(BaseModel):
    access_token: str
    token_type: str

# v-101
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

# v-96
# v-101
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):

    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True
    )
    db.add(create_user_model)
    db.commit()

# v-104
@router.post('/token', response_model=Token)
async def log_for_access_token(form_data: form_dependency, db: db_dependency):
    
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        return 'Failed to Authenticate'
    
    token = create_access_token(user.username, user.id, user.role,timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'Bearer'}
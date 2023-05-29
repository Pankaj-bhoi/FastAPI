from fastapi import FastAPI
from routers import auth, todos, admin, users
from database import engine
import models

app = FastAPI()

# v-90
models.Base.metadata.create_all(bind=engine)
# v-96
app.include_router(auth.router)
# v-97
app.include_router(todos.router)
# v-114
app.include_router(admin.router)
# v-116
app.include_router(users.router)
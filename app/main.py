from fastapi import FastAPI
import os
from . import models
from .database import engine
from .routers import user, post, auth, vote



# This will create all our models in the database
models.Base.metadata.create_all(bind=engine)


db_password = os.environ.get('DATABASE_PASSWORD')
db_username = os.environ.get('DATABASE_USERNAME')
db_name = os.environ.get('DATABASE_NAME')
db_hostname = os.environ.get('DATABASE_HOSTNAME')
db_port = os.environ.get('DATABASE_PORT')


app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router) 
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello Multiverse"}


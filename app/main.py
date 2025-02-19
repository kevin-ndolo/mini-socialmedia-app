import time
from fastapi import Depends, FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import user, post




# This will create all our models in the database
models.Base.metadata.create_all(bind=engine)


db_password = os.environ.get('DATABASE_PASSWORD')
db_username = os.environ.get('DATABASE_USERNAME')
db_name = os.environ.get('DATABASE_NAME')
db_hostname = os.environ.get('DATABASE_HOSTNAME')
db_port = os.environ.get('DATABASE_PORT')



# Connect to an existing database using raw SQL
while True:
    try:
        
        conn = psycopg2.connect(host=db_hostname, dbname=db_name, user=db_username, password=db_password, cursor_factory=RealDictCursor)
        cursor = conn.cursor() 
        print('db connection successful')
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error", error)
        time.sleep(5)




app = FastAPI()


app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
async def root():
    return {"message": "Hello Universe"}


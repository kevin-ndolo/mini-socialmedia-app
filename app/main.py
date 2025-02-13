import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os


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

class Post(BaseModel):
    title:str
    content: str



@app.get("/")
async def root():
    return {"message": "Hello Universe"}



@app.get("/posts/")
async def get_posts():
    
    # Execute a query via vanilla SQL 
    cursor.execute("""SELECT * FROM posts""")
    
    # Retrieve query results via vanilla SQL using psycopg2
    posts =  cursor.fetchall()

    # print(posts)
    if posts:
        return {"posts": posts}
    return {"message": "No posts found"}




@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    

    # Execute a query via vanilla SQL 
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    
    # Retrieve query results via vanilla SQL using psycopg2
    post =  cursor.fetchone()
    # print(post)
    if post:
        return post
    return {"message": f"Post with id {post_id} was not found"}

@app.post("/")
async def create_post(post:Post):
          
    cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (post.title, post.content))

    new_post = cursor.fetchone()
    print(new_post)
    conn.commit()
    return new_post


@app.put("/posts/{post_id}")
async def update_post(post_id: int, updated_post: Post):
     
    # check if post with post_id exists
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    post = cursor.fetchone()
    print(f"Post with id {post_id} is:", post)
    
    if post:
        cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (updated_post.title, updated_post.content, post_id))
        returned_updated_post = cursor.fetchone()
        print(returned_updated_post)
        conn.commit()
       
        return returned_updated_post


    return {"message": f"Post with id {post_id} was not found"}


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    # check if post with post_id exists
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,)) 
    post = cursor.fetchone()
    
    if post:
        cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (post_id,))
        deleted_post = cursor.fetchone()
        conn.commit()
        return {"message": f"Post with id {post_id} was deleted successfully"}

    return {"message": f"Post with id {post_id} was not found"}





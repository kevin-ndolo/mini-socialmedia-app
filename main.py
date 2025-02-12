import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os


# Connect to an existing database using raw SQL
while True:
    try:
        
        conn = psycopg2.connect(host='localhost', dbname='mini-socialmedia-app', user='postgres', password='mbuguz', cursor_factory=RealDictCursor)
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



# posts = [
#     {"id": 1, "title": "First Post", "content": "This is the first post"},
#     {"id": 2, "title": "Second Post", "content": "This is the second post"},
#     {"id": 3, "title": "Third Post", "content": "This is the third post"},
#     {"id": 4, "title": "Fourth Post", "content": "This is the fourth post"},
#     {"id": 5, "title": "Fifth Post", "content": "This is the fifth post"},
#     {"id": 6, "title": "Sixth Post", "content": "This is the sixth post"},
#     {"id": 7, "title": "Seventh Post", "content": "This is the seventh post"},
#     {"id": 8, "title": "Eighth Post", "content": "This is the eighth post"},
#     {"id": 9, "title": "Ninth Post", "content": "This is the ninth post"},
#     {"id": 10, "title": "Tenth Post", "content": "This is the tenth post"}
# ]




@app.get("/")
async def root():
    return {"message": "Hello Universe"}



@app.get("/posts/")
async def get_posts():
    # return {"posts": posts}
    # Execute a query via vanilla SQL 
    cursor.execute("""SELECT * FROM posts""")
    
    # Retrieve query results via vanilla SQL using psycopg2
    posts =  cursor.fetchall()

    print(posts)
    if posts:
        return {"posts": posts}
    return {"message": "No posts found"}




@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    
    # for post in posts:
    #     if post["id"] == post_id:
    #         return {"post": post}

    # print(post_id)

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
   
    # new_post_id =posts[-1]["id"] + 1 if len(posts) > 0 else 1
    # new_post = post.model_dump()
    # new_post["id"] = new_post_id
    
    # posts.append(new_post)
    
    # return posts[-1]

    print(post)
    
    cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (post.title, post.content))

    new_post = cursor.fetchone()
    print(new_post)
    conn.commit()
    return new_post


@app.put("/posts/{post_id}")
async def update_post(post_id: int, updated_post: Post):
      
    # found = False

    # for post in posts:
        
    #     if post["id"] == post_id:
    #         found = True
    #         updated_post_id = post["id"]
    #         updated_post = updated_post.model_dump()
    #         updated_post["id"] = updated_post_id

    #         post.update(updated_post)
    #         return {"message": "Post updated successfully"}
            

    # return {"message": f"Post with id {post_id} was not found"}

    # print(post_id)
    # print(updated_post)

    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (updated_post.title, updated_post.content, post_id))

    # post = cursor.fetchone()
    # print(post)
    # conn.commit()
    # return updated_post

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
    # print(post_id)
    # found = False
    # for post in posts:
    #     if post["id"] == post_id:
    #         found = True
    #         posts.remove(post)
    #         print(f"found = {found}")
    #         print(posts)
    #         return {"message": "Post deleted successfully"}
            
    # print(f"found = {found}")
    # print(posts)
    # return {"message": f"Post with id {post_id} was not found"}        


    # check if post with post_id exists
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,)) 
    post = cursor.fetchone()
    
    if post:
        cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (post_id,))
        deleted_post = cursor.fetchone()
        conn.commit()
        return {"message": f"Post with id {post_id} was deleted successfully"}

    return {"message": f"Post with id {post_id} was not found"}





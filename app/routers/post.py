
from fastapi import Depends, FastAPI, HTTPException, Response, status, APIRouter
from .. import models, schemas, utils
from ..database import get_db 
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/", response_model=list[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    
    # # Execute a query via vanilla SQL 
    # cursor.execute("""SELECT * FROM posts""")
    
    # # Retrieve query results via vanilla SQL using psycopg2
    # posts =  cursor.fetchall()

    posts = db.query(models.Post).all()
    # print(posts)

    if posts:
        return posts
    return {"message": "No posts found"}

  
@router.get("/{post_id}/", response_model=schemas.Post) 
async def get_post(post_id: int, db: Session = Depends(get_db)):
    # print(schemas.Postout)
    # print(type(schemas.Postout))

    # # Execute a query via vanilla SQL 
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    
    # # Retrieve query results via vanilla SQL using psycopg2
    # post =  cursor.fetchone()
    # print(post)

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    # print(post)

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} was not found")
    
    return post


@router.post("/", response_model=schemas.Post)
async def create_post(post:schemas.PostCreate, db: Session = Depends(get_db)):
          
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (post.title, post.content))

    # new_post = cursor.fetchone()
    # print(new_post)
    # conn.commit()

    # print(post)
    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    # print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.put("/{post_id}/", response_model=schemas.Post)
async def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
     
    # # check if post with post_id exists
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    # post = cursor.fetchone()
    # print(f"Post with id {post_id} is:", post)
    
    # if post:
    #     cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (updated_post.title, updated_post.content, post_id))
    #     returned_updated_post = cursor.fetchone()
    #     print(returned_updated_post)
    #     conn.commit()
       
    #     return returned_updated_post


    # return {"message": f"Post with id {post_id} was not found"}

    # print(post_id)
    # print(updated_post)

    # check if post with post_id exists
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} was not found")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    db.refresh(post)

    return post


@router.delete("/posts/{post_id}/")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    # check if post with post_id exists
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,)) 
    # post = cursor.fetchone()
    
    # if post:
    #     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (post_id,))
    #     deleted_post = cursor.fetchone()
    #     conn.commit()
    #     return {"message": f"Post with id {post_id} was deleted successfully"}

    # return {"message": f"Post with id {post_id} was not found"}


    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    # print(post_query)

    if post_query.first() == None:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} was not found")
    
    post_query.delete(synchronize_session=False)
    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


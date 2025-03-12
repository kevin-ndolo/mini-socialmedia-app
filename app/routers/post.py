
from typing import Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db 
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/", response_model=list[schemas.PostOut])
#@router.get("/")
async def get_posts(db: Session = Depends(get_db),  user_id: int = Depends(oauth2.get_current_user),
                    limit: int = 50, skip: int = 0, search: Optional[str] = ""):
   
    #posts = db.query(models.Post).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()

    #results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    posts = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Post, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()

    #We need to convert the posts to a list of dictionaries to be able to return it as a response to the client 
    posts = list ( map (lambda x : x._mapping, posts) )

    return posts
    

  
@router.get("/{post_id}/", response_model=schemas.PostOut) 
async def get_post(post_id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
     
    #post = db.query(models.Post).filter(models.Post.id == post_id).first()
    post = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Post, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} was not found")
    
    return post


@router.post("/", response_model=schemas.Post)
async def create_post(post:schemas.PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):

    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # print(new_post)
    return new_post


@router.put("/{post_id}/", response_model=schemas.Post)
async def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
  
    # check if post with post_id exists
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    db.refresh(post)

    return post


@router.delete("/{post_id}/")
async def delete_post(post_id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    # check if post with post_id exists
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
   

    if post_query.first() == None:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} was not found")
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


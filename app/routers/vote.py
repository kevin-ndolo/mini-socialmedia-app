
from typing import Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db 
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote:schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #Check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} was not found")
    
    # check if vote already exists
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
  
    if (vote.dir == 1):
      if found_vote:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user{current_user.id} has already voted on post{vote.post_id}")
      
      #add new vote ton the database
      new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
      db.add(new_vote)
      db.commit() 
      return {"message": "Vote added successfully"}

    else:   
      #check if vote exists and delete it. Raise exception if vote not found as we cannot delete a vote that doesn't exist. Nb* a vote with a dir of 1 is a vote that has been cast. A vote with a dir of anything but 1 is a vote that has been deleted.
      if not found_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
      
      #delete vote from the database
      vote_query.delete(synchronize_session=False)
      db.commit()
      return {"message": "Vote deleted successfully"}

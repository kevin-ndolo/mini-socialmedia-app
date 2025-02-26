from fastapi import Depends, HTTPException, status, APIRouter
from .. import models, schemas, utils
from ..database import get_db 
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=['Users']
    
)

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
   
    # check if user with email exists
    check_user = db.query(models.User).filter(models.User.email == user.email).first()
   

    if check_user :
        raise HTTPException(status_code=400, detail="User with that email already exists")
    
    # hash password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{user_id}/", response_model=  schemas.UserOut) 
async def get_user( user_id:int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} was not found")

    return user
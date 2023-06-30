from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
import schemas, database, models
from hashing import Hash

router = APIRouter(
  prefix = '/user',
  tags = ['Users']
  )
get_db = database.get_db

# create a user in database
@router.post('/', response_model = schemas.ShowUser, status_code = status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
  new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

# get a user by id from database
@router.get('/{id}', response_model = schemas.ShowUser)
def get_user_by_id(id, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND, 
      detail = f'User with id {id} not found'
    )
  return user
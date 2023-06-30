from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
import schemas, database, models
from hashing import Hash
from repository import user

router = APIRouter(
  prefix = '/user',
  tags = ['Users']
  )
get_db = database.get_db

# create a user in database
@router.post('/', response_model = schemas.ShowUser, status_code = status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
  return user.create(request, db)

# get a user by id from database
@router.get('/{id}', response_model = schemas.ShowUser)
def get_user_by_id(id, db: Session = Depends(get_db)):
  return user.show(id, db)
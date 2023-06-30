from fastapi import APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.orm import Session
from repository import blog
import schemas, database, models

router = APIRouter(
   prefix = '/blog',
   tags = ['Blogs'] 
   )
get_db = database.get_db

@router.get('/', response_model = List[schemas.ShowBlog], status_code = 200)
def get_all_blogs(db: Session = Depends(get_db)):
  return blog.get_all(db)

# get a blog by id from database
@router.get('/{id}', response_model = schemas.ShowBlog, status_code = 200)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
  return blog.show(id, db)

# post a blog in database
@router.post('/', status_code = status.HTTP_201_CREATED)
def create_a_blog( request: schemas.Blog, db: Session = Depends(get_db)):
  return blog.create(request, db)

# delete a blog from database
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_a_blog(id: int, db: Session = Depends(get_db)):
  return blog.delete(id, db)

# update a blog in database
@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update_a_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
  return blog.update(id, request, db)

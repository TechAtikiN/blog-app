from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session
import schemas, database, models

router = APIRouter(
   prefix = '/blog',
   tags = ['Blogs'] 
   )
get_db = database.get_db

@router.get('/', response_model = List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs

# get a blog by id from database
@router.get('/{id}', status_code = 200, response_model = schemas.ShowBlog)
def get_blog_by_id(id, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND, 
      detail = f'Blog with id {id} not found'
    )
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f'Blog with id {id} not found'}
  return blog

# post a blog in database
@router.post('/', status_code = status.HTTP_201_CREATED)
def create_a_blog( request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1, )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# delete a blog from database
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_a_blog(id, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
  if not blog.first():
      raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND, 
        detail = f'Blog with id {id} not found'
      )
  blog.delete(request.dict())
  db.commit()
  return 'Blog deleted successfully'

# update a blog in database
@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update_a_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND, 
      detail = f'Blog with id {id} not found'
    )
  blog.update(request.dict())
  db.commit()
  return 'Blog updated successfully'

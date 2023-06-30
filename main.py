from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from schemas import Blog
from schemas import ShowBlog, User
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get all blogs from database
@app.get('/blog', response_model = List[ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs

# get a blog by id from database
@app.get('/blog/{id}', status_code = 200, response_model = ShowBlog)
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
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
@app.post('/blog', status_code = status.HTTP_201_CREATED)
def create_a_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# delete a blog from database
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
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
@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED)
def update_a_blog(id, request: Blog, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND, 
      detail = f'Blog with id {id} not found'
    )
  blog.update(request.dict())
  db.commit()
  return 'Blog updated successfully'

@app.post('/user')
def create_user(request: User, db: Session = Depends(get_db)):
  new_user = models.User(name=request.name, email=request.email, password=request.password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user
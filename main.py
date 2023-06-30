from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from schemas import Blog
from schemas import ShowBlog, User, ShowUser
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from hashing import Hash
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
@app.get('/blog', response_model = List[ShowBlog], tags = ['blogs'])
def get_all_blogs(db: Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs

# get a blog by id from database
@app.get('/blog/{id}', status_code = 200, response_model = ShowBlog, tags = ['blogs'])
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
@app.post('/blog', status_code = status.HTTP_201_CREATED, tags = ['blogs'])
def create_a_blog( request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1, )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# delete a blog from database
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags = ['blogs'])
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
@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED, tags = ['blogs'])
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

# create a user in database
@app.post('/user', response_model = ShowUser, status_code = status.HTTP_201_CREATED, tags = ['users'])
def create_user(request: User, db: Session = Depends(get_db)):
  new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

# get a user by id from database
@app.get('/user/{id}', response_model = ShowUser, tags = ['users'])
def get_user_by_id(id, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND, 
      detail = f'User with id {id} not found'
    )
  return user
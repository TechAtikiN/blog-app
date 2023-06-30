from fastapi import FastAPI
from  schemas import Blog

app = FastAPI()

@app.get('/blog')
def get():
    return {'data': 'blog list'}

@app.post('/blog')
def create(request: Blog):
    return request
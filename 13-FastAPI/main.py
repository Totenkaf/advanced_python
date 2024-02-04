# Copyright 2024 Artem Ustsov

from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn


app = FastAPI()


@app.get('/index')
def index():
    return FileResponse('./index.html')


@app.get('/blog')
def index(limit: int = 10, published: bool = False, sort: Optional[str] = None):
    return {'data': f'{limit} published blogs from the db'} if published else {'data': f'{limit} blogs from the db'}


@app.get('/blog/{blog_id}')
def show(blog_id: int):
    return {'data': blog_id}


@app.get('/blog/{blog_id}/comments')
def comments(blog_id: str, limit: int = 10):
    return {'data': {'1', '2'}}


class Blog(BaseModel):
    id: str
    title: str
    published: Optional[bool] = True


@app.post('/blog')
def create_blog(request: Blog):
    return {'date': f'blog has been created with values: {request.dict()}'}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=9000)

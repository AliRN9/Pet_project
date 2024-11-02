from typing import Optional, List, Dict
from xml.dom.xmlbuilder import Options

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


users = [
    {"id": 1, "name": "Alex", "age": 35},
    {"id": 2, "name": "Nike", "age": 12},
    {"id": 3, "name": "Kris", "age": 26},
]

posts = [
    {"id": 1, "title": "New1", "body": "Text 1", 'author': users[1]},
    {"id": 2, "title": "New2", "body": "Text 2", 'author': users[0]},
    {"id": 3, "title": "New3", "body": "Text 3", 'author': users[2]},
]


@app.get("/items")
async def items() -> List[Post]:
    print([Post(**post) for post in posts])
    return [Post(**post) for post in posts]


@app.get("/items/{post_id}")
async def items(post_id: int) -> Post:
    for post in posts:
        if post["id"] == post_id:
            return Post(**post)
    raise HTTPException(status_code=404, detail="Post not found")


@app.get("/search")
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if post_id is None:
        return {"data": None}
    for post in posts:
        if post["id"] == post_id:
            return {'data': Post(**post)}
    raise HTTPException(status_code=404, detail="Post not found")

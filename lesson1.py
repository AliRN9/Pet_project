from typing import Optional

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def test():
    return {"message": "Hello World"}


@app.get("/contacts")
async def contacts() -> int:
    return 5


posts = [
    {"id": 1, "title": "New1", "body": "Text 1"},
    {"id": 2, "title": "New2", "body": "Text 2"},
    {"id": 3, "title": "New3", "body": "Text 3"}
]


@app.get("/items/{id}")
async def items(id: int) -> dict:
    for post in posts:
        if post["id"] == id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")


@app.get("/search")
async def search(post_id: Optional[int] = None) -> dict:
    if post_id is None:
        return {"message": "Please provide post id"}
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

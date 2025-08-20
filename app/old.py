from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi import FastAPI, Response, status, HTTPException


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    Rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='20Haneef05#',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Failed to connect to database")
        print("Error: ", error)
        time.sleep()


app = FastAPI()


my_posts = [{"title": "Foods", "content":"Pizza, Amala", "id": 1}, {"title": "Cars", "content": "Ferrari, Bugatti", "id": 2}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i



@app.get("/posts/")
def get_all_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return{"post": posts}

@app.get("/posts/latest")
def get_latest():
    post = my_posts[len(my_posts) - 1]
    return{"details": post}


@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id of {id} was not found")
    return{"message": post}


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """ ,
                   (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()
    return{"message": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
    cursor.execute("""DELETE FROM posts WHERE  id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id of {id} does not exist")
        
    return{"message": "Post deleted successfully"}

@app.put("/posts/{id}")
def update_posts(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id of {id} was not found")
    conn.commit()
    return{"message ": updated_post}
from fastapi import FastAPI


app = FastAPI()

posts = [
    {"id": 1, "title": "First Post", "content": "This is the first post"},
    {"id": 2, "title": "Second Post", "content": "This is the second post"},
    {"id": 3, "title": "Third Post", "content": "This is the third post"},
    {"id": 4, "title": "Fourth Post", "content": "This is the fourth post"},
    {"id": 5, "title": "Fifth Post", "content": "This is the fifth post"},
    {"id": 6, "title": "Sixth Post", "content": "This is the sixth post"},
    {"id": 7, "title": "Seventh Post", "content": "This is the seventh post"},
    {"id": 8, "title": "Eighth Post", "content": "This is the eighth post"},
    {"id": 9, "title": "Ninth Post", "content": "This is the ninth post"},
    {"id": 10, "title": "Tenth Post", "content": "This is the tenth post"}
]

@app.get("/")
async def root():
    return {"message": "Hello Universe"}



@app.get("/posts/")
async def get_posts():
    return {"posts": posts}


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    
    for post in posts:
        if post["id"] == post_id:
            # print(post)

            return {"post": post}

@app.post("/")
async def create_post(post:dict):
    # print(post)
    # print(type(post))
    posts.append(post)
    # print(posts[-1])
    return posts[-1]


@app.put("/posts/{post_id}")
async def update_post(post_id: int, updated_post: dict):
    # print(post_id)
    # print(updated_post)
    
    found = False

    for post in posts:
        # print(post)
        # print(post["id"])
        # print(type(post["id"]))
        # print(type(post_id))
        if post["id"] == post_id:
            found = True
            post.update(updated_post)
            # print(f"found = {found}")    
            # print(posts) 
            return {"message": "Post updated successfully"}
            

    # print(f"found = {found}") 
    # print(posts)  
    return {"message": f"Post with id {post_id} was not found"}




@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    print(post_id)
    found = False
    for post in posts:
        if post["id"] == post_id:
            found = True
            posts.remove(post)
            print(f"found = {found}")
            print(posts)
            return {"message": "Post deleted successfully"}
            
    print(f"found = {found}")
    print(posts)
    return {"message": f"Post with id {post_id} was not found"}        
from fastapi import FastAPI
from mangum import Mangum

from api.routers import posts, users, follows, comments

app = FastAPI()
handler = Mangum(app)

app.include_router(users.router)
app.include_router(follows.router)
app.include_router(posts.router)
app.include_router(comments.router)
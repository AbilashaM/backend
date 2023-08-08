# api router
from fastapi import FastAPI
from server.apirequest import user
app = FastAPI()
app.include_router(user)

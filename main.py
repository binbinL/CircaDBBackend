from fastapi import FastAPI, Request
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from config import TORTOISE_ORM
from api.index import api
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.include_router(api, tags=['APIs of indexs'])
# app.include_router(gene_api, tags=['APIs of genes'])

register_tortoise(
    app=app,
    config=TORTOISE_ORM
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)

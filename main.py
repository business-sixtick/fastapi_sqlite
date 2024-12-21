from fastapi import FastAPI
# from crawling import *  # 네임 스페이스 없이 접근함
import crawling # 네임스페이스로 접근해야함

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


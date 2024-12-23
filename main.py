from fastapi import FastAPI
# from crawling import *  # 네임 스페이스 없이 접근함
import crawling # 네임스페이스로 접근해야함
# from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/lotto")
async def root():
    lottos = crawling.getLottos(100)
    # return {"lottos": f"{lottos.count}"}
    res = []
    for i in lottos:
        res.append(crawling.toJsonLotto(i))
    return res
    # return 



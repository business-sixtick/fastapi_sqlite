from fastapi import FastAPI, Query
# from crawling import *  # 네임 스페이스 없이 접근함
import crawling # 네임스페이스로 접근해야함
# from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


@app.get("/")
async def root():
    
    return {"message": f"Hello World {datetime.now()}"}


@app.get("/lotto")
async def root(length: int = Query(100, description="로또 번호 개수")):
    lottos = crawling.getLottos(length)
    # return {"lottos": f"{lottos.count}"}
    res = []
    for i in lottos:
        res.append(crawling.toJsonLotto(i))
    return res
    # return 



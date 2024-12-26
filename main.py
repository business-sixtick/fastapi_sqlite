import uvicorn
from fastapi import FastAPI, Query
# from crawling import *  # 네임 스페이스 없이 접근함
import crawling # 네임스페이스로 접근해야함
# from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 요청 허용 (개발 환경에서는 "*"을 사용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

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


# 직접 기동시 nginx 없이 https 가 가능하다다
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=443, ssl_keyfile="/etc/letsencrypt/live/lottoapi.duckdns.org/privkey.pem", ssl_certfile="/etc/letsencrypt/live/lottoapi.duckdns.org/fullchain.pem")

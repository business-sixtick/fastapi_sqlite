# fastapi_sqlite
파이썬 fastapi 서버에 sqlite를 구동한다.

## 오라클 클라우드 (sqlite 데이터베이스)
- https://cloud.oracle.com/
- 가용성 도메인: AD-1 항상 무료 적격
- Ubuntu 24.04
- VM.Standard.E2.1.Micro 가상 머신, 1 core OCPU, 1 GB memory, 0.48 Gbps network bandwidth, Processor: 2.0 GHz AMD EPYC™ 7551 (Naples)
- ㅋㅋ 거의뭐 쓰레기급이네 
- ssh ubuntu@144.24.78.242
- ssh -i C:\Users\sixtick3\.ssh\ssh-key-2024-12-21.key ubuntu@144.24.78.242
- ssh -i C:\Users\hungh\.ssh\ssh-key-2024-12-21.key ubuntu@144.24.78.242
- sudo apt update

## 우분투 파이썬 가상환경
- sudo apt install python3-venv python3-pip
- cd ~
- python3 -m venv venv
- source ~/venv/bin/activate

## remote ssh config 구성 (유저폴더에 .ssh\config 파일)
```
Host sqlite
  HostName 144.24.78.242
  User ubuntu
  IdentityFile ~/.ssh/ssh-key-2024-12-21.key
  IdentitiesOnly yes
```

## fastapi sqlite 구성 https://fastapi.tiangolo.com/ko/
- pip install fastapi[all]
- main.py 작성
```
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

- uvicorn main:app --reload
- uvicorn main:app --host 0.0.0.0 --port 80 --reload


## 루트 계정
- sudo passwd root
- su -
- sudo iptables -I INPUT 1 -p tcp --dport 80 -j ACCEPT
- sudo iptables-save | sudo tee /etc/iptables/rules.v4
- sudo ip6tables-save | sudo tee /etc/iptables/rules.v6
- 저장이 안되면 sudo apt install iptables-persistent 설치
- cd /home/ubuntu/fastapi_sqlite/
- source /home/ubuntu/venv/bin/activate
- uvicorn main:app --host 0.0.0.0 --port 80 --reload
- 80 포트로 쓰려면 루트 권한으로 실행해야함
- nohup uvicorn main:app --host 0.0.0.0 --port 80 --reload > /home/ubuntu/uvicorn.log 2>&1 &


## 깃허브 
- git config --global user.name "sixtick_sqlite"
- git config --global user.name "sixtick_lenovno"
- git config --global user.email "business4dyd@gmail.com"
- git config --list
- pip install -r requirements.txt




## 윈도우즈 가상환경
- python -m venv venv
- .\venv\Scripts\activate   // 보안오류시 ttps://blog.naver.com/hungh4/223701757449  참조
- python.exe -m pip install --upgrade pip
- pip install fastapi[all]
- pip install pandas
- pip install beautifulsoup4
- pip install sqlalchemy
- pip install requests
- uvicorn main:app --reload
- http://127.0.0.1:8000/lotto?length=10



## 우분투 로그파일 관리

/home/ubuntu/uvicorn.log {
    daily            
    rotate 7         
    missingok
    create 666 root adm
}
sudo nano /etc/logrotate.d/uvicorn
sudo logrotate -f /etc/logrotate.d/uvicorn  # 강제 실행

/var/log/syslog {
    daily            # 로그 회전 주기 (매일)
    rotate 7         # 7일치 로그 보관
    compress         # 압축 (gzip 사용)
    delaycompress    # 바로 압축하지 않고 하루 뒤에 압축
    missingok        # 로그 파일 없어도 에러 무시
    notifempty       # 비어 있으면 회전 생략
    create 640 root adm  # 새 로그 파일 권한 설정
}



## SSL/TLS 인증서 발급  http://lottoapi.duckdns.org  http://144.24.78.242/

- sudo apt update
- sudo apt install certbot python3-certbot-nginx nginx
- sudo nano /etc/nginx/sites-available/fastapi   (nginx 설정정)
```
server {
    listen 80;
    server_name 144.24.78.242 lottoapi.duckdns.org; # 도메인 설정 (IP 주소도 가능)

    location / {
        proxy_pass http://127.0.0.1:8000; # FastAPI 서버 주소
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 정적 파일 제공 (옵션)
    location /static/ {
        alias /var/www/fastapi/static/;
    }
}
```
- nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /home/ubuntu/uvicorn.log 2>&1 &
- nohup uvicorn main:app --host 0.0.0.0 --port 80 --reload > /home/ubuntu/uvicorn.log 2>&1 &

- sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
- sudo nginx -t  # 설정 파일 테스트
- sudo systemctl reload nginx  (또는 start)

- sudo iptables -I INPUT 1 -p tcp --dport 443 -j ACCEPT
- sudo iptables-save | sudo tee /etc/iptables/rules.v4
- sudo ip6tables-save | sudo tee /etc/iptables/rules.v6

- sudo certbot   (duckdns.org lottoapi.duckdns.org) business4dyd@gmail.com

- 자동갱신 설정 (나중에 다시 확인 해보자자)
- sudo certbot renew --dry-run
- sudo crontab -e
- 0 2 * * * certbot renew --quiet


- 인증서 확인 sudo certbot certificates
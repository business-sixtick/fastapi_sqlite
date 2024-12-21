from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime, timedelta, timezone
from typing import List

import requests
from bs4 import BeautifulSoup
import re


# SQLite 데이터베이스 URL
DATABASE_URL = "sqlite:///lotto.db"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, echo=True) # echo 로그 출력

# 기본 클래스 생성
Base = declarative_base()

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# 모델 정의
class Lotto(Base):
    __tablename__ = 'lotto'
    turn = Column(Integer, primary_key=True) # 회차
    date = Column(Integer) # 추첨일
    grade1count = Column(Integer) # 1등 당첨자수
    grade1money = Column(Integer) # 1등 당첨금액
    grade2count = Column(Integer)
    grade2money = Column(Integer)
    grade3count = Column(Integer)
    grade3money = Column(Integer)
    grade4count = Column(Integer)
    grade4money = Column(Integer)
    grade5count = Column(Integer) # 5등 당첨자수
    grade5money = Column(Integer) # 5등 당첨금액
    win1 = Column(Integer) # 당첨번호 첫번째
    win2 = Column(Integer) # 당첨번호 두번째
    win3 = Column(Integer) # 당첨번호 세번째
    win4 = Column(Integer) # 당첨번호 네번째
    win5 = Column(Integer) # 당첨번호 다섯번째
    win6 = Column(Integer) # 당첨번호 여섯번째
    win7 = Column(Integer) # 당첨번호 보너스
    note = Column(String)   # 비고

def insertLotto(lotto : Lotto):
    # 세션에 추가
    session.add(lotto)
    # 변경 사항 커밋
    session.commit()
    print(f'ok {lotto.turn}')



def deleteLotto(num : int):
    # 특정 id로 객체 찾기
    lotto_to_delete = session.query(Lotto).filter(Lotto.turn == num).first()

    # 객체가 존재하면 삭제
    if lotto_to_delete:
        session.delete(lotto_to_delete)
        session.commit()
        print(f'ok {num}')

def getLotto(num : int = None) -> Lotto: 
    # 데이터 조회
    res : Lotto = session.query(Lotto).order_by(Lotto.turn.desc()).first() if num == None else session.query(Lotto).filter_by(turn = num).first()    
    session.close()
    return res

def getLottos(count : int = None) -> List[Lotto]:
    # 세션 생성
    # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # session = SessionLocal()
    # 데이터 조회
    res : List[Lotto] = session.query(Lotto).all() if count == None else session.query(Lotto).order_by(Lotto.turn.desc()).limit(count).all()
    session.close()
    return res

def crawlingLotto(num : int) -> Lotto:
    url = f'https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo={num}'

    # HTTP 요청 보내기
    response = requests.get(url)
    
    # 응답 상태 확인
    if response.status_code == 200:
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 회차 번호 추출
        draw_no = soup.select_one('h4 strong').text
        draw_no = re.sub(r'[^\d]', '', draw_no)

        # 날짜 추출
        date = soup.select_one('p.desc').text.strip()
        print(date)
        # 문자열에서 숫자 추출
        year, month, day = map(int, [date[1:5], date[7:9], date[11:13]])
        print(year, month, day)
        # datetime 객체로 변환
        date_obj = datetime(year, month, day, 0, 0, 0, 0)
        # 밀리세컨드(Unix 타임스탬프) 변환
        timestamp_ms = int(date_obj.timestamp() * 1000)
        print("밀리세컨드:", timestamp_ms)
         
        # 당첨 번호 추출
        balls = soup.select('span.ball_645')  # 당첨번호 클래스 선택
        winning_numbers = [ball.text for ball in balls]

        # 결과 출력
        print(f'회차: {draw_no}')
        print(f'추첨일: {date}')
        print(f'당첨번호: {winning_numbers[:6]} + 보너스번호: {winning_numbers[6]}')
        print(f'{winning_numbers[0]} {winning_numbers[1]} {winning_numbers[2]} {winning_numbers[3]} {winning_numbers[4]} {winning_numbers[5]} {winning_numbers[6]}')

        rows = soup.select('tbody tr')

        # 결과 저장용 리스트
        results = []

        # 데이터 추출
        for row in rows:
            cols = row.find_all('td')
            rank = cols[0].text.strip()  # 순위

            # 문자열 금액과 당첨자 수에서 ',' 제거 후 정수로 변환
            total_prize = int(re.sub(r'[^\d]', '', cols[1].text))  # 등위별 총 당첨금액
            winners = int(re.sub(r'[^\d]', '', cols[2].text))  # 당첨게임 수

            # 비고 처리 (rowspan이 적용된 1등 행에서만 값 추출)
            remarks = cols[5].get_text(separator=" ", strip=True) if len(cols) > 5 else ""

            # 결과 저장
            results.append((rank, total_prize, winners, remarks))

        # 결과 출력
        for rank, total_prize, winners, remarks in results:
            print(f"{rank}: 총당첨금액 = {total_prize:,}원, 당첨자 수 = {winners:,}명, 비고 = {remarks}")
        print(f'{results[0]}')
        print(f'{results[0][1]}')

        return Lotto(
            turn = draw_no,
            date = timestamp_ms,
            grade1count = results[0][2],
            grade1money = results[0][1],
            grade2count = results[1][2],
            grade2money = results[1][1],
            grade3count = results[2][2],
            grade3money = results[2][1],
            grade4count = results[3][2],
            grade4money = results[3][1],
            grade5count = results[4][2],
            grade5money = results[4][1],
            win1 = winning_numbers[0],
            win2 = winning_numbers[1],
            win3 = winning_numbers[2],
            win4 = winning_numbers[3],
            win5 = winning_numbers[4],
            win6 = winning_numbers[5],
            win7 = winning_numbers[6],
            note = results[0][3]
        )
    else:
        return None

def refreshLotto():
    lotto = getLotto()
    # 밀리세컨드 타임스탬프 (예시)
    timestamp = lotto.date

    # 타임스탬프를 datetime으로 변환 (밀리세컨드 -> 초로 변환) 
    timestamp_datetime = datetime.fromtimestamp(timestamp / 1000, tz=None)
    # timestamp_datetime = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)

    # 현재 날짜와 시간 (UTC)
    now = datetime.now(tz=None)
    print(now)
    print(timestamp_datetime)
    # 7일을 timedelta로 설정
    seven_days = timedelta(days=7, hours=21)

    # 날짜 차이 계산
    time_difference = now - timestamp_datetime
    print(time_difference)
    # 7일 이상인지 확인
    if time_difference > seven_days:
        print("7일 이상 지났습니다.")
        insertLotto(crawlingLotto(lotto.turn + 1)) # 크롤링해서 인서트 한다다
    else:
        print("7일 이내입니다.")
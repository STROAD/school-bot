from discord import Embed
from datetime import datetime
from requests import get
from xml.etree.ElementTree import fromstring
from config import NIES_KEY


# 학사일정 API URL
schedule_url = "https://open.neis.go.kr/hub/SchoolSchedule"


# 학사일정 정보 가져오기
async def schedule_parser():
    # 현재 날짜 구하기
    aa_ymd = datetime.now().strftime("%Y%m%d")

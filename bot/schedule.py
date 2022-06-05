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

    # 학사일정 파라미터
    schedule_params = {
        "key": NIES_KEY,
        "Type": "xml",
        "ATPT_OFCDC_SC_CODE": "#수정하기#",
        "SD_SCHUL_CODE": "#수정하기#",
        "AA_FROM_YMD": aa_ymd,
        "AA_TO_YMD": aa_ymd,
    }

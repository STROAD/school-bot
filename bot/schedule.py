from discord import Embed
from datetime import datetime
from dateutil.relativedelta import relativedelta
from requests import get
from xml.etree.ElementTree import fromstring
from pandas import DataFrame
from re import sub
from config import NIES_KEY


# 학사일정 API URL
schedule_url = "https://open.neis.go.kr/hub/SchoolSchedule"


# 학사일정 정보 가져오기
async def schedule_parser():
    # 현재, 한달 뒤 날짜 구하기
    aa_from_ymd = datetime.now()
    aa_to_ymd = aa_from_ymd + relativedelta(months=1)
    aa_from_ymd = sub("-", "", str(aa_from_ymd)[:10])
    aa_to_ymd = sub("-", "", str(aa_to_ymd)[:10])

    # 학사일정 파라미터
    schedule_params = {
        "key": NIES_KEY,
        "Type": "xml",
        "ATPT_OFCDC_SC_CODE": "#수정하기#",
        "SD_SCHUL_CODE": "#수정하기#",
        "AA_FROM_YMD": aa_ymd,
        "AA_TO_YMD": aa_ymd,
    }

    # 학사일정 XML로 받아오기
    response = get(schedule_url, schedule_params)
    schedule_xml = fromstring(response.content)

    # 호출결과 코드 찾기
    result_code = schedule_xml.findtext(".//CODE")

    # 학사일정 정보가 존재하는지 확인
    # 학사일정이 있을경우
    if result_code == "INFO-000":
        pass

    # 학사일정이 없을경우
    elif result_code == "INFO-200":
        pass


# 학사일정
async def schedule(ctx):
    pass

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
        "AA_FROM_YMD": aa_from_ymd,
        "AA_TO_YMD": aa_to_ymd,
    }

    # 학사일정 XML로 받아오기
    response = get(schedule_url, schedule_params)
    schedule_xml = fromstring(response.content)

    # 호출결과 코드 찾기
    result_code = schedule_xml.findtext(".//CODE")

    # 학사일정 정보가 존재하는지 확인
    # 학사일정이 있을경우
    if result_code == "INFO-000":
        # 학교 이름 찾기
        schul_nm = schedule_xml.findtext(".//SCHUL_NM")
        # 데이터 프레임 생성
        df = DataFrame([], columns=["aa_ymd", "evn_nm"])

        # 행사명, 행사일자 찾기
        for value in schedule_xml.iter("row"):
            evn_nm = value.findtext("EVENT_NM")
            aa_ymd = value.findtext("AA_YMD")

            # 데이터 프레임에 행사명, 행사일자 넣기
            data = {"evn_nm": f"{evn_nm}", "aa_ymd": f"{aa_ymd}"}
            df = df.append(data, ignore_index=True)

        # 행사명이 토요휴업일인 행은 삭제
        df = df[df["evn_nm"] != "토요휴업일"]
        df = df.reset_index(drop=True)

        embed = Embed(
            title=f"🗓️ **{schul_nm} 학사일정** 🗓️",
            description=f"**행사명\n행사일**",
            colour=0xB0BEC5,
        )

    # 학사일정이 없을경우
    if result_code == "INFO-200":
        pass


# 학사일정
async def schedule(ctx):
    pass

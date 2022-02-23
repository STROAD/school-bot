from nextcord import Embed
from datetime import datetime
from requests import get
from xml.etree.ElementTree import fromstring
from re import sub
from config import meal_KEY


# 급식 API URL
meal_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"


# 급식정보 가져오기
async def meal_parser(meal_params):
    global meal, msm

    # 급식정보 XML로 받아오기
    response = get(meal_url, meal_params)
    meal_xml = fromstring(response.content)

    # 호출결과 코드 찾기
    result_code = meal_xml.findtext(".//CODE")

    # 급식메뉴가 존재하는지 확인
    # 급식이있을경우
    if result_code == "INFO-000":
        # 급식메뉴만 추출
        meal = str(meal_xml.findtext(".//DDISH_NM"))
        meal = sub("(<([^>]+)>)", "\n", meal)
        meal = sub("[0-9.]", "", meal)

        # 식사명 찾기
        msm = meal_xml.findtext(".//MMEAL_SC_NM")

    # 급식이 없을경우
    elif result_code == "INFO-200":
        meal = "급식이 없습니다."
        msm = " "


# 오늘급식 or 사용자가 입력한 날짜의 급식
async def today_meal(ctx, msg):
    # 현재 날짜 구하기
    # `!급식` 뒤에 날짜를 입력하지 않았을 경우
    if msg == None:
        today_time = datetime.now().strftime("%Y%m%d")
        y = datetime.now().strftime("%Y")
        m = datetime.now().strftime("%m")
        d = datetime.now().strftime("%d")

    # 급식 파라미터
    meal_params = {
        "key": meal_KEY,
        "Type": "xml",
        "ATPT_OFCDC_SC_CODE": "#수정하기#",
        "SD_SCHUL_CODE": "#수정하기#",
        "MMEAL_SC_CODE": "#수정하기#",
        "MLSV_YMD": today_time,
    }

    # meal_parser함수 실행
    await meal_parser(meal_params)

    embed = Embed(
        title=f"***{y}년 {m}월 {d}일 급식***", description="\u200B", colour=0xB0BEC5
    )
    embed.add_field(name=f"**{meal}**", value=f"**{msm}**", inline=False)

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 내일급식
async def tomorrow_meal(ctx):
    # 내일 날짜 구하기
    tomorrow_time = int(datetime.now().strftime("%Y%m%d")) + 1
    tomorrow_y = int(datetime.now().strftime("%Y"))
    tomorrow_m = int(datetime.now().strftime("%m"))
    tomorrow_d = int(datetime.now().strftime("%d")) + 1

    # 급식 파라미터
    meal_params = {
        "key": meal_KEY,
        "Type": "xml",
        "ATPT_OFCDC_SC_CODE": "#수정하기#",
        "SD_SCHUL_CODE": "#수정하기#",
        "MMEAL_SC_CODE": "#수정하기#",
        "MLSV_YMD": tomorrow_time,
    }

    # meal_parser함수 실행
    await meal_parser(meal_params)

    embed = Embed(
        title=f"***{tomorrow_y}년 {tomorrow_m}월 {tomorrow_d}일 급식***",
        description="\u200B",
        colour=0xB0BEC5,
    )
    embed.add_field(name=f"**{meal}**", value=f"**{msm}**", inline=False)

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)

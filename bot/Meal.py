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
        msm = f'({meal_xml.findtext(".//MMEAL_SC_NM")})'

    # 급식이 없을경우
    elif result_code == "INFO-200":
        meal = "급식정보가 존재하지 않습니다."
        msm = " "


# 오늘급식 or 사용자가 입력한 날짜의 급식
async def today_meal(ctx, msg):
    # 기본적으로 중식정보를 받아오도록 함
    m_s_code = "2"

    # 현재 날짜 구하기
    today_time = datetime.now().strftime("%Y%m%d")
    y = datetime.now().strftime("%Y")
    m = datetime.now().strftime("%m")
    d = datetime.now().strftime("%d")

    # `!급식` 뒤에 날짜를 입력하지 않았을 경우
    if msg == None:
        pass

    # `!급식` 뒤에 석식을 입력했을 경우
    elif msg == "석식":
        m_s_code = "3"

    # `!급식` 뒤에 날짜를 입력했고 그 길이가 6자 혹은 8자 일 경우
    elif (
        msg != None
        and (0 < int(msg[-4:-2]) < 13)
        and (0 < int(msg[-2:]) < 32)
        and (len(msg) == 6 or len(msg) == 8)
    ):
        # 사용자가 입력한 날짜로 설정
        today_time = msg
        y = msg[:-4]
        m = msg[-4:-2]
        d = msg[-2:]

        # 년도를 2글자만 썼을경우 앞에 20을 붙여줌
        if len(y) == 2:
            y = "20" + y
        # 4글자 모두 입력했으면 pass
        elif len(y) == 4:
            pass

    # 잘못된 날짜를 입력하면 오류 메시지를 출력
    else:
        embed = Embed(title=f"***오류!***", description="\u200B", colour=0xB0BEC5)
        embed.add_field(name="**잘못된 값을 입력하였습니다.**", value=f"입력값 : {msg}", inline=False)

        await ctx.send(embed=embed, reference=ctx.message, mention_author=False)

    # 급식 파라미터
    meal_params = {
        "key": meal_KEY,
        "Type": "xml",
        "ATPT_OFCDC_SC_CODE": "#수정하기#",
        "SD_SCHUL_CODE": "#수정하기#",
        "MMEAL_SC_CODE": m_s_code,
        "MLSV_YMD": today_time,
    }

    # meal_parser함수 실행
    await meal_parser(meal_params)

    embed = Embed(
        title=f"***{y}년 {m}월 {d}일 급식***", description="\u200B", colour=0xB0BEC5
    )
    embed.add_field(name=f"**{meal}**", value="\u200B", inline=False)
    embed.set_footer(text=f"{msm}")

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 내일급식
async def tomorrow_meal(ctx, msg):
    # 기본적으로 중식정보를 받아오도록 함
    m_s_code = "2"

    # 내일 날짜 구하기
    tomorrow_time = int(datetime.now().strftime("%Y%m%d")) + 1
    tomorrow_y = int(datetime.now().strftime("%Y"))
    tomorrow_m = int(datetime.now().strftime("%m"))
    tomorrow_d = int(datetime.now().strftime("%d")) + 1

    # `!내일급식` 뒤에 아무것도 입력하지 않았을 경우
    if msg == None:
        pass

    # `!내일급식` 뒤에 석식을 입력했을 경우
    elif msg == "석식":
        m_s_code = "3"

    else:
        embed = Embed(title=f"***오류!***", description="\u200B", colour=0xB0BEC5)
        embed.add_field(name="**잘못된 값을 입력하였습니다.**", value=f"입력값 : {msg}", inline=False)

        await ctx.send(embed=embed, reference=ctx.message, mention_author=False)

    # 급식 파라미터
    meal_params = {
        "key": meal_KEY,
        "Type": "xml",
        "ATPT_OFCDC_SC_CODE": "#수정하기#",
        "SD_SCHUL_CODE": "#수정하기#",
        "MMEAL_SC_CODE": m_s_code,
        "MLSV_YMD": tomorrow_time,
    }

    # meal_parser함수 실행
    await meal_parser(meal_params)

    embed = Embed(
        title=f"***{tomorrow_y}년 {tomorrow_m}월 {tomorrow_d}일 급식***",
        description="\u200B",
        colour=0xB0BEC5,
    )
    embed.add_field(name=f"**{meal}**", value="\u200B", inline=False)
    embed.set_footer(text=f"{msm}")

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 특정 채널로 급식(중식)정보 보내기
async def meal_noti(bot):
    # 현재 날짜 구하기
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
        "MMEAL_SC_CODE": "2",
        "MLSV_YMD": today_time,
    }

    # meal_parser함수 실행
    await meal_parser(meal_params)

    embed = Embed(
        title=f"***{y}년 {m}월 {d}일 급식***", description="\u200B", colour=0xB0BEC5
    )
    embed.add_field(name=f"**{meal}**", value="\u200B", inline=False)
    embed.set_footer(text=f"{msm}")

    await bot.get_channel("#수정하기#").send(embed=embed)

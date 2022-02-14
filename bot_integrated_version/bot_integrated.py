import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET
import re


"""API 정보

##############################################################################

[나이스교육정보개방포털](급식식단정보)
(https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&
rows=10&sortColumn=&sortDirection=&infId=OPEN17320190722180924242823&infSeq=1)


[기본인자]

{변수설명}{변수명}
인증키 = KEY
호출 문서(xml, json) = Type
페이지 위치 = pIndex
페이지 당 요청 숫자 = pSize


[요청인자]

{변수설명}{변수명}{예시}
시도교육청코드 = ATPT_OFCDC_SC_CODE = A01
표준학교코드 = SD_SCHUL_CODE = 0123456
식사코드 = MMEAL_SC_CODE = 0
급식일자 = MLSV_YMD = yyyymmdd
급식시작일자 = MLSV_FROM_YMD = yyyymmdd
급식종료일자 = MLSV_TO_YMD = yyyymmdd

##############################################################################

[공공데이터포털](국토교통부_버스도착정보)
(https://www.data.go.kr/data/15000757/openapi.do)


-정류소별특정노선버스도착예정정보목록조회-


[요청변수(Request Parameter)]

{항목명(국문)}{항목명(영문)}{예시}
도시코드 = cityCode = 12345
정류소ID = nodeId = ABC12345678
노선ID = routeId = ABC123456789


[출력결과(Response Element)]

{항목명(국문)}{항목명(영문)}{예시}
정류소ID = nodeid = ABC12345678
정류소명 = nodenm = OO정류소
노선ID = routeid = ABC123456789
노선번호 = routeno = 1
노선유형 = routetp = 일반버스
도착예정버스 남은 정류장 수 = arrprevstationcnt = 12
도착예정버스 차량유형 = vehicletp = 일반차량
도착예정버스 도착예상시간[초] = arrtime = 123

##############################################################################

"""


# config #####################################################################

Token = "#수정하기#"  # 이곳에 자신의 디스코드 봇 토큰 넣기
meal_KEY = "#수정하기#"  # 이곳에 자신의 급식식단정보 Open API 인증키 입력
open_API_KEY = "#수정하기#"  # 이곳에 자신의 국토교통부 버스도착정보 Open API 인증키 입력

GitHub = "https://github.com/STROAD/school-bot"

##############################################################################


# 명령어 접두어
bot = commands.Bot(command_prefix="!")


# 봇 시작
@bot.event
async def on_ready():
    await bot.change_presence(
        status=nextcord.Status.online,
        activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="!도움말"),
    )
    print(f"{bot.user.name}({bot.user.id}) 연결 완료")


# 도움말
@bot.command()
async def 도움말(ctx):
    embed = nextcord.Embed(title="***도움말***", description="명령어 리스트", colour=0xFFFF8D)
    embed.add_field(name="1. **정보**", value="`!정보\n!info`", inline=False)
    embed.add_field(name="2. **인사**", value="`!안녕\n!hi`", inline=False)
    embed.add_field(name="3. **현재 시간 확인**", value="`!현재시간\n!time`", inline=False)
    embed.add_field(name="4. **지연시간 확인**", value="`!핑\n!ping`", inline=False)
    embed.add_field(name="5. **시간표**", value="`!시간표`", inline=False)
    embed.add_field(name="6. **급식정보 확인**", value="`!급식\n!오늘급식\n!내일급식`", inline=False)
    embed.add_field(name="7. **버스 도착 정보 확인**", value="`!집버스\n!학교버스`", inline=False)

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 정보
@bot.command(aliases=["정보"])
async def info(ctx):
    embed = nextcord.Embed(title="***정보***", description="\u200B", colour=0xFFFF8D)
    embed.add_field(name="디스코드 봇", value="급식, 버스정보 확인가능", inline=False)
    embed.add_field(name="자세한 정보는", value=f"[여기서]({GitHub}) 확인 가능", inline=False)
    embed.add_field(name="\u200B", value="\u200B", inline=False)
    embed.add_field(name="*버전* : 2.1.0", value=f"[GitHub]({GitHub})", inline=False)

    await ctx.send(embed=embed)


# 인사
@bot.command(aliases=["안녕", "반가워", "Hi"])
async def hi(ctx):
    await ctx.send(f"**{ctx.message.author.nick}님 안녕하세요!**", reference=ctx.message)


# 시간
@bot.command(aliases=["시간", "현재시간"])
async def time(ctx):
    # 오전 오후 변수
    apm = datetime.now().strftime("%p")

    # 오전 오후 구하기
    if apm == "AM":
        ampm = "오전"
    else:
        ampm = "오후"

    # 요일 구하기
    days = ["월", "화", "수", "목", "금", "토", "일"]
    d = datetime.now().weekday()

    await ctx.send(
        datetime.now().strftime(
            f"> **%Y년 %m월 %d일 \
{days[d]}요일**\n> **{ampm} %I시 %M분 %S초**"
        )
    )


# 핑
@bot.command(aliases=["핑"])
async def ping(ctx):
    await ctx.send(f"> **Ping : {round(bot.latency * 1000)}ms**")


# 시간표
@bot.command()
async def 시간표(ctx):
    await ctx.send(
        """
```
ㅤ| 월요일 | 화요일 | 수요일 | 목요일 | 금요일 |
1 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
2 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
3 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
4 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
5 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
6 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
7 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
```
"""
    )


# 급식 API URL
meal_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"


# 급식정보 가져오기
async def meal_parser(meal_params):
    global meal, msm

    # 급식정보 XML로 받아오기
    response = requests.get(meal_url, meal_params)
    meal_xml = ET.fromstring(response.content)

    # 호출결과 코드 찾기
    result_code = meal_xml.findtext(".//CODE")

    # 급식메뉴가 존재하는지 확인
    # 급식이있을경우
    if result_code == "INFO-000":
        # 급식메뉴만 추출
        meal = str(meal_xml.findtext(".//DDISH_NM"))
        meal = re.sub("(<([^>]+)>)", "\n", meal)
        meal = re.sub("[0-9.]", "", meal)

        # 식사명 찾기
        msm = meal_xml.findtext(".//MMEAL_SC_NM")

    # 급식이 없을경우
    elif result_code == "INFO-200":
        meal = "급식이 없습니다."
        msm = " "


# 오늘급식
@bot.command(aliases=["오늘급식"])
async def 급식(ctx):
    # 현재 날짜 구하기
    today_time = datetime.now().strftime("%Y%m%d")
    y = datetime.now().strftime("%Y")
    m = datetime.now().strftime("%m")
    d = datetime.now().strftime("%d")

    # 급식 파라미터
    meal_params = {
        "key": meal_KEY,
        "Type": "xml",
        "ATPT_OFCDC_SC_CODE": "N10",
        "SD_SCHUL_CODE": "#수정하기#",
        "MMEAL_SC_CODE": "#수정하기#",
        "MLSV_YMD": today_time,
    }

    # meal_parser함수 실행
    await meal_parser(meal_params)

    embed = nextcord.Embed(
        title=f"***{y}년 {m}월 {d}일 급식***", description="\u200B", colour=0xB0BEC5
    )
    embed.add_field(name=f"**{meal}**", value=f"**{msm}**", inline=False)

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 내일급식
@bot.command(aliases=["ㄴㅇㄱㅅ", "ㄴㅇ"])
async def 내일급식(ctx):
    # 내일 날짜 구하기
    tomorrow_time = int(datetime.now().strftime("%Y%m%d")) + 1
    tomorrow_y = int(datetime.now().strftime("%Y"))
    tomorrow_m = int(datetime.now().strftime("%m"))
    tomorrow_d = int(datetime.now().strftime("%d")) + 1

    # 급식 파라미터
    meal_params = {
        "key": meal_KEY,
        "Type": "xml",
        "ATPT_OFCDC_SC_CODE": "N10",
        "SD_SCHUL_CODE": "#수정하기#",
        "MMEAL_SC_CODE": "#수정하기#",
        "MLSV_YMD": tomorrow_time,
    }

    # meal_parser함수 실행
    await meal_parser(meal_params)

    embed = nextcord.Embed(
        title=f"***{tomorrow_y}년 {tomorrow_m}월 {tomorrow_d}일 급식***",
        description="\u200B",
        colour=0xB0BEC5,
    )
    embed.add_field(name=f"**{meal}**", value=f"**{msm}**", inline=False)

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 버스 API URL
Bus_URL = "http://openapi.tago.go.kr/openapi/service/\
ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"


# 버스정보 가져오기
async def bus_parser(Bus_params):
    global minute, second, cnt, nodenm

    # 버스 정보 XML로 받아오기
    response = requests.get(Bus_URL, params=Bus_params)
    bus_xml = ET.fromstring(response.content)

    # 도착 예정 시간
    arrtime = int(bus_xml.findtext(".//arrtime"))
    # 남은 정거장 수
    cnt = f"(남은 정거장 수 : {bus_xml.findtext('.//arrprevstationcnt')})"
    # 정거장 이름
    nodenm = bus_xml.findtext(".//nodenm")

    # 도착 예정 시간 초를 분,초로 변환
    second = arrtime % 60
    minute = int(arrtime / 60 % 60)


# 집버스
@bot.command(aliases=["집", "ㅈ"])
async def 집버스(ctx):
    # 버스 파라미터
    Bus_params = {
        "serviceKey": open_API_KEY,
        "cityCode": "#수정하기#",
        "nodeId": "#수정하기#",
        "routeId": "#수정하기#",
    }

    await bus_parser(Bus_params)

    embed = nextcord.Embed(
        title="***버스 도착 정보***", description="\u200B", colour=0x2196F3
    )
    embed.add_field(name="**버스 정보**", value="#수정하기#", inline=False)
    embed.add_field(name="**정거장 정보**", value=nodenm, inline=False)
    embed.add_field(
        name="**버스 도착 예정 시간**", value=(f"{minute}분 {second}초 {cnt}"), inline=False
    )

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 학교 버스
@bot.command(aliases=["학교", "ㅎㄱ"])
async def 학교버스(ctx):
    # 버스 파라미터
    Bus_params = {
        "serviceKey": open_API_KEY,
        "cityCode": "#수정하기#",
        "nodeId": "#수정하기#",
        "routeId": "#수정하기#",
    }

    await bus_parser(Bus_params)

    embed = nextcord.Embed(
        title="***버스 도착 정보***", description="\u200B", colour=0x2196F3
    )
    embed.add_field(name="**버스 정보**", value="#수정하기#", inline=False)
    embed.add_field(name="**정거장 정보**", value=nodenm, inline=False)
    embed.add_field(
        name="**버스 도착 예정 시간**", value=(f"{minute}분 {second}초 {cnt}"), inline=False
    )

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 날씨 API URL
weather_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"


@bot.command(aliases=["ㄴㅆ"])
async def 날씨(ctx):
    # 날짜, 시간 구하기
    now_date = int(datetime.now().strftime("%Y%m%d"))
    yes_date = datetime.now() - timedelta(1)
    now_hour = int(datetime.now().strftime("%H"))
    now_min = int(datetime.now().strftime("%M"))

    # API 제공 시간에 맞춰 가장 최신의 정보를 받을 수 있는 시간을 설정
    if now_hour < 2 or (now_hour == 2 and now_min <= 10):
        base_date = yes_date
        base_time = "2300"
    elif now_hour < 5 or (now_hour == 5 and now_min <= 10):
        base_date = now_date
        base_time = "0200"
    elif now_hour < 8 or (now_hour == 8 and now_min <= 10):
        base_date = now_date
        base_time = "0500"
    elif now_hour < 11 or now_min <= 10:
        base_date = now_date
        base_time = "0800"
    elif now_hour < 14 or (now_hour == 14 and now_min <= 10):
        base_date = now_date
        base_time = "1100"
    elif now_hour < 17 or (now_hour == 17 and now_min <= 10):
        base_date = now_date
        base_time = "1400"
    elif now_hour < 20 or (now_hour == 20 and now_min <= 10):
        base_date = now_date
        base_time = "1700"
    elif now_hour < 23 or (now_hour == 23 and now_min <= 10):
        base_date = now_date
        base_time = "2000"
    else:
        base_time = now_date
        base_time = "2300"

    # 날씨 파라미터
    weather_params = {
        "ServiceKey": open_API_KEY,
        "pageNo": "1",
        "numOfRows": "12",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": "62",
        "ny": "110",
    }

    # 날씨정보 JSON으로 받아오기
    response = requests.get(weather_URL, params=weather_params).json()


bot.run(Token)

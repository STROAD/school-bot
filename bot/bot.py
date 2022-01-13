import nextcord
from nextcord.ext import commands
from datetime import datetime
import requests
import xml.etree.ElementTree as ET
import re
from config import Token
from config import meal_KEY
from config import bus_KEY
from config import bot_status
from config import bot_activity
from config import schedule
from config import GitHub


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


# 명령어 접두어
bot = commands.Bot(command_prefix="!")


# 봇 시작
@bot.event
async def on_ready():
    await bot.change_presence(status=bot_status, activity=bot_activity)
    print(f"{bot.user.name}({bot.user.id}) 연결 완료")


# 도움말
@bot.command()
async def 도움말(ctx):
    embed = nextcord.Embed(title="***도움말***", description="명령어 리스트", colour=0xFFFF8D)
    embed.add_field(name="1. **정보**", value="`!정보\n!info`", inline=False)
    embed.add_field(name="2. **현재 시간 확인**", value="`!현재시간\n!time`", inline=False)
    embed.add_field(name="3. **지연시간 확인**", value="`!핑\n!ping`", inline=False)
    embed.add_field(name="4. **시간표**", value="`!시간표`", inline=False)
    embed.add_field(name="5. **급식정보 확인**", value="`!급식\n!오늘급식\n!내일급식`", inline=False)
    embed.add_field(name="5. **버스 도착 정보 확인**", value="`!집버스\n!학교버스`", inline=False)

    await ctx.send(embed=embed)


# 정보
@bot.command(aliases=["정보"])
async def info(ctx):
    embed = nextcord.Embed(title="***정보***", description="\u200B", colour=0xFFFF8D)
    embed.add_field(name="디스코드 봇", value="급식, 버스정보 확인가능", inline=False)
    embed.add_field(name="자세한 정보는", value=f"[여기서]({GitHub}) 확인 가능", inline=False)
    embed.add_field(name="\u200B", value="\u200B", inline=False)
    embed.add_field(name="*버전* : 2.0.1", value=f"[GitHub]({GitHub})", inline=False)

    await ctx.send(embed=embed)


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
    await ctx.send(schedule)


# 오늘급식
@bot.command(aliases=["오늘급식"])
async def 급식(ctx):
    # 현재 날짜 구하기
    today_time = datetime.now().strftime("%Y%m%d")
    y = datetime.now().strftime("%Y")
    m = datetime.now().strftime("%m")
    d = datetime.now().strftime("%d")

    # 급식 API URL
    meal_url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?key={meal_KEY}\
&Type=json&pIndex=1&pSize=100\
&ATPT_OFCDC_SC_CODE=#수정하기#&SD_SCHUL_CODE=#수정하기#\
&MMEAL_SC_CODE=2&MLSV_YMD={today_time}"

    # 급식정보 json으로 받아오기
    response = requests.get(meal_url).json()

    # 급식메뉴만 추출
    meal = str(response["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"])
    meal = re.sub("(<([^>]+)>)", "\n", meal)
    meal = re.sub("[0-9.]", "", meal)

    embed = nextcord.Embed(
        title=f"***{y}년 {m}월 {d}일 급식***", description="\u200B", colour=0xB0BEC5
    )
    embed.add_field(name=f"**{meal}**", value="(중식)", inline=False)

    await ctx.send(embed=embed)


# 내일급식
@bot.command(aliases=["ㄴㅇㄱㅅ", "ㄴㅇ"])
async def 내일급식(ctx):
    # 내일 날짜 구하기
    tomorrow_time = int(datetime.now().strftime("%Y%m%d")) + 1
    tomorrow_y = int(datetime.now().strftime("%Y"))
    tomorrow_m = int(datetime.now().strftime("%m"))
    tomorrow_d = int(datetime.now().strftime("%d")) + 1

    # 급식 API URL
    meal_url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?key={meal_KEY}\
&Type=json&pIndex=1&pSize=100\
&ATPT_OFCDC_SC_CODE=#수정하기#&SD_SCHUL_CODE=#수정하기#\
&MMEAL_SC_CODE=2&MLSV_YMD={tomorrow_time}"

    # 급식정보 json으로 받아오기
    response = requests.get(meal_url).json()

    # 급식메뉴만 추출
    meal = str(response["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"])
    meal = re.sub("(<([^>]+)>)", "\n", meal)
    meal = re.sub("[0-9.]", "", meal)

    embed = nextcord.Embed(
        title=f"***{tomorrow_y}년 {tomorrow_m}월 {tomorrow_d}일 급식***",
        description="\u200B",
        colour=0xB0BEC5,
    )
    embed.add_field(name=f"**{meal}**", value="(중식)", inline=False)

    await ctx.send(embed=embed)


# 버스 API URL
Bus_URL = "http://openapi.tago.go.kr/openapi/service/\
ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"


# 집버스
@bot.command(aliases=["집", "ㅈ"])
async def 집버스(ctx):
    # 버스 파라미터
    Bus_params = {
        "serviceKey": bus_KEY,
        "cityCode": "#수정하기#",
        "nodeId": "#수정하기#",
        "routeId": "#수정하기#",
    }

    # 버스 정보 받아오기
    response = requests.get(Bus_URL, params=Bus_params)

    # 버스 도착 예정 시간, 남은 정류장 추출
    bus_xml = ET.fromstring(response.content)
    item_tag = bus_xml.findall(".//item[1]")

    for i in item_tag:
        time = int(i.findtext("arrtime"))
        cnt = f"(남은 정거장 수 : {i.findtext('arrprevstationcnt')})"

    # 도착 예정 시간 초를 분,초로 변환
    sec = time % 60
    min = int(time / 60 % 60)

    embed = nextcord.Embed(
        title="***버스 도착 정보***", description="\u200B", colour=0x2196F3
    )
    embed.add_field(name="**버스 정보**", value="#수정하기#", inline=False)
    embed.add_field(name="**정거장 정보**", value="#수정하기#", inline=False)
    embed.add_field(
        name="**버스 도착 예정 시간**", value=(f"{min}분 {sec}초 {cnt}"), inline=False
    )

    await ctx.send(embed=embed)


# 학교 버스
@bot.command(aliases=["학교", "ㅎㄱ"])
async def 학교버스(ctx):
    # 버스 파라미터
    Bus_params = {
        "serviceKey": bus_KEY,
        "cityCode": "#수정하기#",
        "nodeId": "#수정하기#",
        "routeId": "#수정하기#",
    }

    # 버스 정보 받아오기
    response = requests.get(Bus_URL, params=Bus_params)

    # 버스 도착 예정 시간, 남은 정류장 추출
    bus_xml = ET.fromstring(response.content)
    item_tag = bus_xml.findall(".//item[1]")

    for i in item_tag:
        time = int(i.findtext("arrtime"))
        cnt = f"(남은 정거장 수 : {i.findtext('arrprevstationcnt')})"

    # 도착 예정 시간 초를 분,초로 변환
    sec = time % 60
    min = int(time / 60 % 60)

    embed = nextcord.Embed(
        title="***버스 도착 정보***", description="\u200B", colour=0x2196F3
    )
    embed.add_field(name="**버스 정보**", value="#수정하기#)", inline=False)
    embed.add_field(name="**정거장 정보**", value="#수정하기#", inline=False)
    embed.add_field(
        name="**버스 도착 예정 시간**", value=(f"{min}분 {sec}초 {cnt}"), inline=False
    )

    await ctx.send(embed=embed)


bot.run(Token)

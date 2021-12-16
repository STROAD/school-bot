import discord
from discord.ext import commands
from datetime import datetime
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
bus_KEY = "#수정하기#"  # 이곳에 자신의 국토교통부 버스도착정보 Open API 인증키 입력

GitHub = "https://github.com/STROAD/school-bot"

##############################################################################


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.listening , name="!도움말"))
    print(f"{bot.user.name}({bot.user.id}) 연결 완료")


@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(title="***도움말***", description="명령어 리스트")
    embed.add_field(name="1. **정보**", value="`!정보\n!info`", inline=False)
    embed.add_field(name="2. **현재 시간 확인**", value="`!현재시간\n!time`", inline=False)
    embed.add_field(name="3. **지연시간 확인**", value="`!핑\n!ping`", inline=False)
    embed.add_field(name="4. **시간표**", value="`!시간표`", inline=False)
    embed.add_field(name="5. **급식정보 확인**", value="`!급식\n!오늘급식\n내일급식`", inline=False)
    embed.add_field(name="5. **버스 도착 정보 확인**", value="`!집버스\n!학교버스`", inline=False)

    await ctx.send(embed=embed)


@bot.command(aliases=['정보'])
async def info(ctx):
    embed = discord.Embed(title="***정보***", description="\u200B", inline=False)
    embed.add_field(name="디스코드 봇", value="급식, 버스정보 확인가능", inline=False)
    embed.add_field(name="자세한 정보는", value=f"[여기서]({GitHub}) 확인 가능", inline=False)
    embed.add_field(name="\u200B", value="\u200B", inline=False)
    embed.add_field(name="*버전* : 1.1.0", value=f"[GitHub]({GitHub})", inline=False)

    await ctx.send(embed=embed)


@bot.command(aliases=['시간', '현재시간'])
async def time(ctx):
    apm = datetime.now().strftime('%p')

    if apm == "AM":
        ampm = "오전"
    else:
        ampm = "오후"

    days = ["월", "화", "수", "목", "금", "토", "일"]
    d = datetime.now().weekday()

    await ctx.send(datetime.now().strftime(f'> **%Y년 %m월 %d일 \
{days[d]}요일**\n> **{ampm} %I시 %M분 %S초**'))


@bot.command(aliases=['핑'])
async def ping(ctx):
    await ctx.send(f"Ping : {round(bot.latency * 1000)}ms")


@bot.command()
async def 시간표(ctx):
    await ctx.send("""
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
""")


@bot.command(aliases=['오늘급식'])
async def 급식(ctx):
    today_time = datetime.now().strftime("%Y%m%d")
    today_y = datetime.now().strftime('%Y')
    today_m = datetime.now().strftime('%m')
    today_d = datetime.now().strftime('%d')


    meal_url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?key={meal_KEY}\
&Type=json&pIndex=1&pSize=100\
&ATPT_OFCDC_SC_CODE=#수정하기#&SD_SCHUL_CODE=#수정하기#\
&MMEAL_SC_CODE=2&MLSV_YMD={today_time}"

    response = requests.get(meal_url).json()

    meal = str(response["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"])
    meal = re.sub('(<([^>]+)>)', '\n', meal)
    meal = re.sub('[0-9.]', '', meal)

    embed = discord.Embed(title=f"***{today_y}년 {today_m}월 {today_d}일 급식***", description="\u200B")
    embed.add_field(name=f"**{meal}**", value="(중식)", inline=False)

    await ctx.send(embed=embed)


@bot.command(aliases=["ㄴㅇㄱㅅ", "ㄴㅇ"])
async def 내일급식(ctx):
    tomorrow_time = int(datetime.now().strftime("%Y%m%d")) + 1
    tomorrow_y = int(datetime.now().strftime("%Y"))
    tomorrow_m = int(datetime.now().strftime("%m"))
    tomorrow_d = int(datetime.now().strftime("%d")) + 1

    meal_url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?key={meal_KEY}\
&Type=json&pIndex=1&pSize=100\
&ATPT_OFCDC_SC_CODE=#수정하기#&SD_SCHUL_CODE=#수정하기#\
&MMEAL_SC_CODE=2&MLSV_YMD={tomorrow_time}"

    response = requests.get(meal_url).json()

    meal = str(response["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"])
    meal = re.sub('(<([^>]+)>)', '\n', meal)
    meal = re.sub('[0-9.]', '', meal)

    embed = discord.Embed(title=f"***{tomorrow_y}년 {tomorrow_m}월 {tomorrow_d}일 급식***", description="\u200B")
    embed.add_field(name=f"**{meal}**", value="(중식)", inline=False)

    await ctx.send(embed=embed)


Bus_URL = 'http://openapi.tago.go.kr/openapi/service/\
ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'

@bot.command(aliases=['집', 'ㅈ'])
async def 집버스(ctx):

    h_Bus_params = {'serviceKey': bus_KEY, 'cityCode': '#수정하기#',
                    'nodeId': '#수정하기#', 'routeId': '#수정하기#'}

    h_response = requests.get(Bus_URL, params=h_Bus_params)

    h_bus_xml = ET.fromstring(h_response.content)
    h_item_tag = h_bus_xml.findall('.//item[1]')

    for h_i in h_item_tag:
        h_time = int(h_i.findtext('arrtime'))
        h_cnt = (f"(남은 정거장 수 : {h_i.findtext('arrprevstationcnt')})")

    h_sec = h_time % 60
    h_min = int(h_time / 60 % 60)

    embed = discord.Embed(title="***버스 도착 정보***", description="\u200B")
    embed.add_field(name="**버스 정보**", value="#수정하기#", inline=False)
    embed.add_field(name="**정거장 정보**", value="#수정하기#", inline=False)
    embed.add_field(name="**버스 도착 예정 시간**", value=(f"{h_min}분 {h_sec}초 {h_cnt}"), inline=False)

    await ctx.send(embed=embed)


@bot.command(aliases=['학교', 'ㅎㄱ'])
async def 학교버스(ctx):

    s_Bus_params = {'serviceKey': bus_KEY, 'cityCode': '#수정하기#',
                    'nodeId': '#수정하기#', 'routeId': '#수정하기#'}

    s_response = requests.get(Bus_URL, params=s_Bus_params)

    s_bus_xml = ET.fromstring(s_response.content)
    s_item_tag = s_bus_xml.findall('.//item[1]')

    for s_i in s_item_tag:
        s_time = int(s_i.findtext('arrtime'))
        s_cnt = (f"(남은 정거장 수 : {s_i.findtext('arrprevstationcnt')})")

    s_sec = s_time % 60
    s_min = int(s_time / 60 % 60)

    embed = discord.Embed(title="***버스 도착 정보***", description="\u200B")
    embed.add_field(name="**버스 정보**", value="#수정하기#)", inline=False)
    embed.add_field(name="**정거장 정보**", value="#수정하기#", inline=False)
    embed.add_field(name="**버스 도착 예정 시간**", value=(f"{s_min}분 {s_sec}초 {s_cnt}"), inline=False)

    await ctx.send(embed=embed)


bot.run(Token)

import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET
import re
from config import Token
from config import meal_KEY
from config import open_API_KEY
from config import bot_status
from config import bot_activity
from config import schedule
from config import GitHub
from Meal import today_meal, tomorrow_meal
from Bus import bus_home, bus_school


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
    embed.add_field(name="2. **인사**", value="`!안녕\n!hi`", inline=False)
    embed.add_field(name="3. **현재 시간 확인**", value="`!현재시간\n!time`", inline=False)
    embed.add_field(name="4. **지연시간 확인**", value="`!핑\n!ping`", inline=False)
    embed.add_field(name="5. **시간표**", value="`!시간표`", inline=False)
    embed.add_field(name="6. **급식정보 확인**", value="`!급식\n!오늘급식\n!내일급식`", inline=False)
    embed.add_field(name="7. **버스 도착 정보 확인**", value="`!집버스\n!학교버스`", inline=False)
    embed.add_field(name="8. **날씨정보 확인**", value="`!날씨`", inline=False)

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
    await ctx.send(schedule)


# 오늘급식
@bot.command(aliases=["오늘급식"])
async def 급식(ctx):
    await today_meal(ctx)


# 내일급식
@bot.command(aliases=["ㄴㅇㄱㅅ", "ㄴㅇ"])
async def 내일급식(ctx):
    await tomorrow_meal(ctx)


# 집버스
@bot.command(aliases=["집", "ㅈ"])
async def 집버스(ctx):
    await bus_home(ctx)


@bot.command(aliases=["학교", "ㅎㄱ"])
async def 학교버스(ctx):
    await bus_school(ctx)


# 날씨 API URL
weather_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"


# 날씨
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
    # 호출결과 코드
    resultCode = response["response"]["header"]["resultCode"]

    # 정상적으로 호출되었을 경우
    if resultCode == "00":
        # 날씨정보
        weather_data = response.get("response").get("body").get("items")

        # 날씨정보 추출
        for item in weather_data["item"]:
            # 1시간 기온
            if item["category"] == "TMP":
                tmp = item["fcstValue"]

            # 하늘상태
            if item["category"] == "SKY":
                sky_code = item["fcstValue"]

                if sky_code == "1":
                    sky = "맑음"
                elif sky_code == "3":
                    sky = "구름많음"
                elif sky_code == "4":
                    sky = "흐림"
                else:
                    sky = "정보없음"

            # 강수형태
            if item["category"] == "PTY":
                pty_code = item["fcstValue"]

                if pty_code == "0":
                    pty = "강수없음"
                elif pty_code == "1":
                    pty = "비"
                elif pty_code == "2":
                    pty = "비/눈"
                elif pty_code == "3":
                    pty = "눈"
                elif pty_code == "4":
                    pty = "소나기"
                else:
                    pty = "정보없음"

            # 강수확률
            if item["category"] == "POP":
                pop = item["fcstValue"]

            # 1시간 강수량
            if item["category"] == "PCP":
                pcp = item["fcstValue"]

                if pcp == "강수없음":
                    pcp = pcp
                else:
                    pcp = f"{pcp} mm"

            # 습도
            if item["category"] == "REH":
                reh = item["fcstValue"]

            # 1시간 신적설
            if item["category"] == "SNO":
                sno = item["fcstValue"]

                if sno == "적설없음":
                    sno = sno
                else:
                    sno = f"{sno} cm"

    # 정상적으로 호출되지 못했을 경우
    else:
        print("오류! 잠시후 다시 시도해주시기 바랍니다.")

    embed = nextcord.Embed(title="***날씨 정보***", description="ㅇㅇ동", colour=0x2196F3)
    embed.add_field(name="***기온***", value=f"{tmp}°C")
    embed.add_field(name="***습도***", value=f"{reh}%")
    embed.add_field(name="***하늘***", value=f"{sky}")
    embed.add_field(name="***강수확률***", value=f"{pop}%")
    # 강수형태가 있을 경우에만 임베드 추가
    if pty_code != "0":
        embed.add_field(name="**강수형태**", value=f"{pty}")
        embed.add_field(name="**강수량**", value=f"{pcp}")
    # 적설이 있을 경우에만 임베드 추가
    if sno != "적설없음":
        embed.add_field(name="**적설량**", value=f"{sno}")

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


bot.run(Token)

import discord
from discord.ext import commands
from datetime import datetime
from config import TOKEN, APPLICATION_ID, bot_status, bot_activity, schedule, GITHUB


"""API 정보

##############################################################################

[나이스교육정보개방포털](급식식단정보)
(https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&
rows=10&sortColumn=&sortDirection=&infId=OPEN17320190722180924242823&infSeq=1)


[기본인자]

{변수설명}{변수명}{예시}{타입}
인증키                = KEY     = -    = 필수
호출 문서(xml, json)  = Type    = xml  = 필수
페이지 위치           = pIndex  = 1    = 필수
페이지 당 요청 숫자   = pSize   = 100  = 필수


[요청인자]

{변수설명}{변수명}{예시}{타입}
시도교육청코드  = ATPT_OFCDC_SC_CODE  = A01       = 필수
표준학교코드    = SD_SCHUL_CODE       = 0123456   = 필수
식사코드        = MMEAL_SC_CODE       = 0         = 선택
급식일자        = MLSV_YMD            = yyyymmdd  = 선택
급식시작일자    = MLSV_FROM_YMD       = yyyymmdd  = 선택
급식종료일자    = MLSV_TO_YMD         = yyyymmdd  = 선택


[출력값]

{출력명}{출력 설명}
SCHUL_NM        = 학교명
MMEAL_SC_CODE   = 식사코드
MMEAL_SC_NM     = 식사명
MLSV_YMD        = 급식일자
DDISH_NM        = 요리명
1MLSV_FROM_YMD  = 급식시작일자
1MLSV_TO_YMD    = 급식종료일자

##############################################################################

[나이스교육정보개방포털](학사일정)
(https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&
rows=10&sortColumn=&sortDirection=&infId=OPEN17220190722175038389180&infSeq=1)


[기본인자]

{변수설명}{변수명}{예시}{타입}
인증키                = KEY     = -    = 필수
호출 문서(xml, json)  = Type    = xml  = 필수
페이지 위치           = pIndex  = 1    = 필수
페이지 당 요청 숫자   = pSize   = 100  = 필수

[신청인자]

{변수설명}{변수명}{예시}{타입}
시도교육청코드  = ATPT_OFCDC_SC_CODE  = A01       = 필수
표준학교코드    = SD_SCHUL_CODE       = 0123456   = 필수
주야과정명      = DGHT_CRSE_SC_NM     = 주간      = 선택
학교과정명      = SCHUL_CRSE_SC_NM    = 고등학교  = 선택
학사일자        = AA_YMD              = yyyymmdd  = 선택
학사시작일자    = AA_FROM_YMD         = yyyymmdd  = 선택
학사종료일자    = AA_TO_YMD           = yyyymmdd  = 선택


[출력값]

{출력명}{출력 설명}
ATPT_OFCDC_SC_NM  = 시도교육청명
SCHUL_NM          = 학교명
AY                = 학년도
SBTR_DD_SC_NM     = 수업공제일명
AA_YMD            = 학사일자
1EVENT_NM         = 행사명
1EVENT_CNTNT      = 행사내용
1LOAD_DTM         = 수정일

##############################################################################

[공공데이터포털](국토교통부_(TAGO)_버스도착정보)
(https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15098530)


-정류소별특정노선버스 도착예정정보 목록조회-


[요청변수(Request Parameter)]

{항목명(국문)}{항목명(영문)}{예시}{항목구분}
서비스키           = serviceKey  = -             = 필수
페이지 번호        = pageNo      = 1             = 옵션
한 페이지 결과 수  = numOfRows   = 10            = 옵션
데이터 타입        = _type       = xml           = 옵션
도시코드           = cityCode    = 12345         = 필수
정류소ID           = nodeId      = ABC12345678   = 필수
노선ID             = routeId     = ABC123456789  = 필수


[출력결과(Response Element)]

{항목명(국문)}{항목명(영문)}{예시}
결과코드                       = resultCode         = 00
결과메시지                     = resultMsg          = OK
한 페이지 결과 수              = numOfRows          = 10
페이지 번호                    = pageNo             = 1
전체 결과 수                   = totalCount         = 3
정류소ID                       = nodeid             = ABC12345678
정류소명                       = nodenm             = OO정류소
노선ID                         = routeid            = ABC123456789
노선번호                       = routeno            = 1
노선유형                       = routetp            = 일반버스
도착예정버스 남은 정류장 수    = arrprevstationcnt  = 12
도착예정버스 차량유형          = vehicletp          = 일반차량
도착예정버스 도착예상시간[초]  = arrtime            = 123

##############################################################################

[공공데이터포털](기상청_단기예보 ((구)_동네예보) 조회서비스)
(https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15084084)


-단기예보조회-


[요청변수(Request Parameter)]

{항목명(국문)}{항목명(영문)}{예시}{항목구분}
서비스키           = ServiceKey  = -         = 필수
페이지 번호        = pageNo      = 1         = 필수
한 페이지 결과 수  = numOfRows   = 10        = 필수
응답자료형식       = dataType    = JSON      = 옵션
발표일자           = base_date   = 20220215  = 필수
발표시각           = base_time   = 1100      = 필수
예보지점 X 좌표    = nx          = 55        = 필수
예보지점 Y 좌표    = ny          = 127       = 필수


[출력결과(Response Element)]

{항목명(국문)}{항목명(영문)}{예시}
결과코드           = resultCode  = 00
결과메시지         = resultMsg   = OK
한 페이지 결과 수  = numOfRows   = 10
페이지 번호        = pageNo      = 1
전체 결과 수       = totalCount  = 3
데이터 타입        = dataType    = JSON
발표일자           = baseDate    = 20220215
발표시각           = baseTime    = 1100
예보일자           = fcstDate    = 20220215
예보시각           = fcstTime    = 1200
자료구분문자       = category    = TMP
예보 값            = fcstValue   = 10
예보지점 X 좌표    = nx          = 55
예보지점 Y 좌표    = ny          = 127

##############################################################################

"""


intents = discord.Intents.all()


class School_Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            sync_command=True,
            application_id=APPLICATION_ID,
            help_command=None,
        )
        self.initial_extension = [
            "cogs.bus",
            "cogs.help",
            "cogs.meal",
            "cogs.noti",
            "cogs.schedule",
            "cogs.weather",
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)
        await bot.tree.sync()

    async def on_ready(self):
        await self.change_presence(status=bot_status, activity=bot_activity)
        print(f"{self.user.name}({self.user.id}) 연결 완료")


bot = School_Bot()


# 정보
@bot.hybrid_command(name="정보", description="School_Bot 정보", aliases=["Info", "정보"])
async def info(ctx: commands.Context):
    embed = discord.Embed(title="***정보***", description="\u200B", colour=0xFFFF8D)
    embed.add_field(name="School_Bot", value="급식, 버스, 날씨 정보 등 확인 가능", inline=False)
    embed.add_field(name="자세한 정보는", value=f"[여기서]({GITHUB}) 확인 가능", inline=False)
    embed.add_field(name="\u200B", value="\u200B", inline=False)
    embed.add_field(name="*버전* : 5.0.0", value=f"[GitHub]({GITHUB})", inline=False)

    await ctx.send(embed=embed)


# 인사
@bot.hybrid_command(name="인사", description="인사하기", aliases=["Hi", "hi", "반가워"])
async def hi(ctx: commands.Context):
    await ctx.send(f"**{ctx.message.author.nick}님 안녕하세요!**  👋")


# 시간
@bot.hybrid_command(name="현재시간", description="현재시간 확인", aliases=["Time", "시간", "현재시간"])
async def time(ctx: commands.Context):
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


# 지연시간
@bot.hybrid_command(
    name="지연시간", description="봇의 지연시간 확인", aliases=["Ping", "핑", "지연시간"]
)
async def ping(ctx: commands.Context):
    await ctx.send(f"> **지연시간 : {round(bot.latency * 1000)}ms**")


# 시간표
@bot.hybrid_command(name="시간표", description="시간표")
async def 시간표(ctx: commands.Context):
    await ctx.send(schedule)


bot.run(TOKEN)

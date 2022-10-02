import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from requests import get
from xml.etree.ElementTree import fromstring
from re import sub
from config import NIES_KEY


def date_now():
    return datetime.now().strftime("%Y%m%d")


class Meal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Meal cog loaded.")

    @app_commands.command(name="급식", description="급식 식단 정보 확인")
    @app_commands.describe(meals="어느 식단을 확인하시겠습니까?")
    @app_commands.choices(
        meals=[
            discord.app_commands.Choice(name="중식", value=1),
            discord.app_commands.Choice(name="석식", value=2),
        ]
    )
    @app_commands.describe(date="날짜를 입력해주세요. (YYYYMMDD)")
    async def meal(
        self,
        interaction: discord.Interaction,
        meals: discord.app_commands.Choice[int],
        date: str = date_now(),
    ):
        await prt_meal(self, interaction, meals.value, date)


async def setup(bot):
    await bot.add_cog(Meal(bot))


# 급식 API URL
meal_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"


# 급식정보 가져오기
async def meal_parser(m_s_code, date):
    # 현재 날짜 구하기
    y = datetime.now().strftime("%Y")
    m = datetime.now().strftime("%m")
    d = datetime.now().strftime("%d")

    # 사용자 입력값으로 설정
    mlsv_ymd = date
    y = date[:-4]
    m = date[-4:-2]
    d = date[-2:]

    # 년도를 2글자만 썼을경우 앞에 20을 붙여줌
    if len(y) == 2:
        y = "20" + y
    # 4글자 모두 입력했으면 pass
    elif len(y) == 4:
        pass

    # 급식 파라미터
    meal_params = {
        "KEY": NIES_KEY,
        "Type": "xml",
        "ATPT_OFCDC_SC_CODE": "#수정하기#",
        "SD_SCHUL_CODE": "#수정하기#",
        "MMEAL_SC_CODE": m_s_code,
        "MLSV_YMD": mlsv_ymd,
    }

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
        meal = sub("<br/>", "\n", meal)
        meal = sub("[(\d.) ]+", "", meal)

        # 식사명 찾기
        msm = f'({meal_xml.findtext(".//MMEAL_SC_NM")})'

    # 급식이 없을경우
    elif result_code == "INFO-200":
        meal = "급식정보가 존재하지 않습니다."
        msm = " "

    return meal, msm, y, m, d


# 급식 정보 출력
async def prt_meal(self, interaction, meals, date):
    if meals == 1:
        m_s_code = "2"
    else:
        m_s_code = "3"

    if (
        (0 < int(date[-4:-2]) < 13)
        and (0 < int(date[-2:]) < 32)
        and (len(date) == 6 or len(date) == 8)
    ):
        date = date

    else:
        embed = discord.Embed(title=f"***오류!***", description="\u200B", colour=0xB0BEC5)
        embed.add_field(name="**잘못된 값을 입력하였습니다.**", value=f"입력값 : {date}", inline=False)

        await interaction.response.send_message(embed=embed)

    meal, msm, y, m, d = await meal_parser(m_s_code, date)

    embed = discord.Embed(
        title=f"🍽️ ***{y}년 {m}월 {d}일 급식***  🍽️", description="\u200B", colour=0xB0BEC5
    )
    embed.add_field(name=f"**{meal}**", value="\u200B", inline=False)
    embed.set_footer(text=f"{msm}")

    await interaction.response.send_message(embed=embed)


# 특정 채널로 급식정보 보내기
async def meal_noti(bot, m_s_code):
    date = datetime.now().strftime("%Y%m%d")

    # meal_parser함수 실행
    meal, msm, y, m, d = await meal_parser(m_s_code, date)

    embed = discord.Embed(
        title=f"🍽️ ***{y}년 {m}월 {d}일 급식***  🍽️", description="\u200B", colour=0xB0BEC5
    )
    embed.add_field(name=f"**{meal}**", value="\u200B", inline=False)
    embed.set_footer(text=f"{msm}")

    await bot.get_channel("#수정하기# -> int").send(embed=embed)

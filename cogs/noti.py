from discord.ext import commands, tasks
from datetime import datetime
from .meal import meal_noti


class Noti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.meal_Notification.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Noti cog loaded.")

    # 특정 시간에 급식정보 보내기
    @tasks.loop(seconds=1.0)
    async def meal_Notification(self):
        # 월~금 요일의 12:30:00 PM 일때
        if (
            datetime.now().strftime("%p") == "AM"
            and 0 <= datetime.now().weekday() < 5
            and datetime.now().hour == 12
            and datetime.now().minute == 30
            and datetime.now().second == 00
        ):
            m_s_code = "2"

            # meal_noti함수 실행
            await meal_noti(self.bot, m_s_code)

        # 월~금 요일의 17:30:00 PM 일때
        if (
            datetime.now().strftime("%p") == "PM"
            and 0 <= datetime.now().weekday() < 5
            and datetime.now().hour == 17
            and datetime.now().minute == 30
            and datetime.now().second == 00
        ):
            m_s_code = "3"

            # meal_noti함수 실행
            await meal_noti(self.bot, m_s_code)


async def setup(bot):
    await bot.add_cog(Noti(bot))

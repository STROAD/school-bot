import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime


class Select_Help(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="정보", description="정보 명령어 도움말"),
            discord.SelectOption(label="인사", description="인사 명령어 도움말"),
            discord.SelectOption(label="현재시간", description="현재시간 명령어 도움말"),
            discord.SelectOption(label="지연시간", description="지연시간 명령어 도움말"),
            discord.SelectOption(label="시간표", description="시간표 명령어 도움말"),
            discord.SelectOption(label="급식", description="급식 명령어 도움말"),
            discord.SelectOption(label="버스", description="버스 명령어 도움말"),
            discord.SelectOption(label="날씨", description="날씨 명령어 도움말"),
            discord.SelectOption(label="학사일정", description="학사일정 명령어 도움말"),
        ]
        super().__init__(
            placeholder="도움말을 확인할 명령어를 선택하세요.",
            max_values=1,
            min_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "정보":
            embed = discord.Embed(
                title="***도움말(정보 명령어)***",
                description="사용법: `!정보` or `!info`",
                colour=0xFFFF8D,
            )
            embed.add_field(
                name="상세정보",
                value="School_Bot의 정보를 확인할 수 있습니다.",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "인사":
            embed = discord.Embed(
                title="***도움말(인사 명령어)***",
                description="사용법: `!안녕` or `!hi`",
                colour=0xFFFF8D,
            )
            embed.add_field(
                name="상세정보",
                value="School_Bot과 인사할 수 있습니다.",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "현재시간":
            embed = discord.Embed(
                title="***도움말(현재시간 명령어)***",
                description="사용법: `!현재시간` or `!time`",
                colour=0xFFFF8D,
            )
            embed.add_field(
                name="상세정보",
                value="현재시간을 확인할 수 있습니다.",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "지연시간":
            embed = discord.Embed(
                title="***도움말(지연시간 확인 명령어)***",
                description="사용법: `!핑` or `!ping`",
                colour=0xFFFF8D,
            )
            embed.add_field(
                name="상세정보",
                value="School_Bot의 지연시간을 확인할 수 있습니다.",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "시간표":
            embed = discord.Embed(
                title="***도움말(시간표 명령어)***",
                description="사용법: `!시간표`",
                colour=0xFFFF8D,
            )
            embed.add_field(
                name="상세정보",
                value="시간표를 확인할 수 있습니다.",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "급식":
            today = datetime.now().strftime("%Y%m%d")

            embed = discord.Embed(
                title="***도움말(급식 명령어)***",
                description="사용법: `/급식 [필수: meals] [선택: date]`",
                colour=0xFFFF8D,
            )
            embed.add_field(
                name="상세정보",
                value="오늘의 급식 혹은 사용자가 입력한 날짜의 급식(중식, 석식)을 확인할 수 있습니다.\n\n\
[date] 미선택 시 오늘의 급식을 확인합니다.\n\
[date]는 YYYYMMDD 형식으로 입력해야합니다.",
                inline=False,
            )
            embed.add_field(
                name="**예시**",
                value=f"`/급식 [meals: 중식] [date: {today}]`",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "버스":
            embed = discord.Embed(
                title="***도움말(버스 도착 정보 확인 명령어)***",
                description="사용법: `/버스 [필수: direction]`",
                colour=0xFFFF8D,
            )
            embed.add_field(
                name="상세정보",
                value="선택한 방면의 버스 도착 예정 정보를 확인할 수 있습니다.",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "날씨":
            embed = discord.Embed(
                title="***도움말(날씨정보 확인 명령어)***",
                description="사용법: `/날씨`",
                colour=0xFFFF8D,
            )
            embed.add_field(
                name="상세정보",
                value="특정지역의 날씨(단기예보)정보를 확인을 확인할 수 있습니다.",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "학사일정":
            embed = discord.Embed(
                title="***도움말(학사일정 확인 명령어)***",
                description="사용법: `/학사일정`",
                colour=0xFFFF8D,
            )
            embed.add_field(
                name="상세정보",
                value="특정학교의 학사일정을 확인을 확인할 수 있습니다.\n\n\
기본적으로 한달간의 학사일정을 확인합니다.",
                inline=False,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Select_Help())


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help cog loaded.")

    @app_commands.command(name="도움말", description="School_Bot 도움말")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="**도움말**", description="School_Bot 명령어 목록", colour=0xFFFF8D
        )
        embed.add_field(name="1. **정보**", value="`/정보`", inline=False)
        embed.add_field(name="2. **인사**", value="`/안녕`", inline=False)
        embed.add_field(name="3. **현재시간 확인**", value="`/시간`", inline=False)
        embed.add_field(name="4. **지연시간 확인**", value="`/지연시간`", inline=False)
        embed.add_field(name="5. **시간표**", value="`/시간표`", inline=False)
        embed.add_field(name="6. **급식정보 확인**", value="`/급식`", inline=False)
        embed.add_field(name="7. **버스 도착 정보 확인**", value="`/버스`", inline=False)
        embed.add_field(name="8. **날씨정보 확인**", value="`/날씨`", inline=False)
        embed.add_field(name="9. **학사일정 확인**", value="`/학사일정`", inline=False)
        embed.set_footer(text="!도움말 [명령어]로 해당 명령어 상세정보 확인가능")

        await interaction.response.send_message(embed=embed, view=SelectView())


async def setup(bot):
    await bot.add_cog(Help(bot))

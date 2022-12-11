import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime


class Select_Help(discord.ui.Select):
    pass


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

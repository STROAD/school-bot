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

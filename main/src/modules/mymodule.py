"""
All Commands of type ______
"""


import discord
from discord import app_commands
from discord.ext import commands

from typing import Any, Dict

from ..bot import TheBot
from ..utils import *


class Message(commands.Cog):
    """Contains All the _________ Commands"""
    def __init__(self, bot: TheBot):
        self.bot = bot
        
        
    @app_commands.command(name="hello")
    async def hello(self, interaction: discord.Interaction, to: discord.Member, message: str):
        """DMs a user

        Parameters
        -----------
        to:
            Member to message
        message: 
            Message to send
        """
        await interaction.response.send_message(f"DMing `{to.mention}`: {message}", ephemeral=True)
        self.bot.log(f"{interaction.user.name} : {interaction.user.id} sent a message to {to.name}: {message}")
        await interaction.followup.send(f"Haha u got fooled. I didn't DM anyone.", ephemeral=True)

async def setup(bot: TheBot):
    await bot.add_cog(Message(bot))

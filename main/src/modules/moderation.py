"""
All Admin-Only Commands
"""

import os
import traceback
import discord
from discord.ext import commands
from discord import app_commands

from typing import List

from ..bot import TheBot
from ..utils import *

class Moderator(commands.Cog):
    """Contains All the Admin Commands"""
    def __init__(self, bot: TheBot):
        self.bot = bot

    def admin_only_command() -> app_commands.check: # type: ignore
        """Checks if the User is an Admin"""
        def predicate(interaction: discord.Interaction):
            bot: TheBot = interaction.client # type: ignore
            return interaction.permissions.manage_messages == True
        return app_commands.check(predicate)

    @app_commands.command(
        name="clear"
    )
    @admin_only_command()
    async def clear(self, interaction: discord.Interaction, msg_count: int, user: discord.User = None):  # type: ignore
        """Clears a given amount of messages in the channel

        Args:
            msg_count (int): Amount of messages to delete
            user: User to delete messages from
        """
        msg_count += 1
        if user:
            await interaction.response.defer(thinking=True)
            await interaction.followup.send(f"Deleting {msg_count} messages from {user.mention}")
            await interaction.channel.purge(limit=msg_count, check=lambda msg: msg.author == user)
            await interaction.edit_original_response(content=f"Deleted {msg_count} messages from {user.mention}")
        else:
            await interaction.response.defer(thinking=True)
            await interaction.followup.send(f"Deleting {msg_count} messages")
            await interaction.channel.purge(limit=msg_count)
            await interaction.edit_original_response(content=f"Deleted {msg_count} messages")
            

async def setup(bot: TheBot):
    await bot.add_cog(Moderator(bot))

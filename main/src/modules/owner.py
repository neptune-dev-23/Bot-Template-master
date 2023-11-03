"""
All Owner-Only Commands
"""

import os
import traceback
import discord
from discord.ext import commands
from discord import app_commands

from typing import List

from ..bot import TheBot
from ..utils import *


class Owner(commands.Cog):
    """Contains All the Owner Commands"""
    def __init__(self, bot: TheBot):
        self.bot = bot

    def owner_only_command() -> app_commands.check: # type: ignore
        """Checks if the User is the Owner"""
        def predicate(interaction: discord.Interaction):
            bot: TheBot = interaction.client # type: ignore
            return interaction.user.id == bot.owner_id
        return app_commands.check(predicate)


    @app_commands.command(
        name="reload"
    )
    @owner_only_command()
    async def reload(self, interaction: discord.Interaction, cog: str):
        """Reloads Module(s)
        
        Parameters
        -----------
        cog:
            The Cog to Reload.
        """
        await interaction.response.defer(ephemeral=True, thinking=True)
        if not cog: # Reload All Cogs
            description = ""
            checklist = {}
            extensions = os.listdir("./src/modules/")
            for ext in extensions:
                if ext.endswith(".py") and not ext.startswith("_"):
                    checklist[ext] = ["`\U000023F3`", "\n"]
            for ext, value in checklist.items():
                description += f"{value[0]} `{ext}`{value[1]}"

            embed = discord.Embed(
                title="Reloading Cogs . . .",
                colour=discord.Colour.light_grey(),
                description=description
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

            ERROR = False
            SUCCESS = False
            for ext in extensions:
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        try:
                            await self.bot.unload_extension(f"src.modules.{ext[:-3]}")
                        except commands.ExtensionNotLoaded:
                            pass
                        finally:
                            await self.bot.load_extension(f"src.modules.{ext[:-3]}")
                    except commands.ExtensionFailed as E:
                        ERROR = True
                        checklist[ext] = ["`\U0000274C`", f"\n```\n{E.original}\n```\n"]
                    else:
                        SUCCESS = True
                        checklist[ext] = ["`\U00002705`", "\n"]
                    finally:
                        description = ""
                        for extension, value in checklist.items():
                            description += f"{value[0]} `{extension}`{value[1]}"
                        if (SUCCESS is True) and (ERROR is False):
                            embed.colour = discord.Colour.green()
                        elif (SUCCESS is True) and (ERROR is True):
                            embed.colour = discord.Colour.yellow()
                        elif (SUCCESS is False) and (ERROR is True):
                            embed.colour = discord.Colour.red()
                        embed.description = description

            embed.title="Reloaded Cogs:"
            await interaction.edit_original_response(embed=embed)
        else:
            ext = f"{cog.lower()}.py"
            embed = discord.Embed(
                title="Reloading Cogs . . .",
                colour=discord.Colour.light_grey(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            if not os.path.exists(f"./src/modules/{ext}"):
                embed.title="Reloaded Cogs:"
                embed.colour = discord.Colour.red()
                embed.description = f"`\U0000274C` `{ext}`\n```{cog} is Invalid!```"
                await interaction.edit_original_response(embed=embed)
            else:
                try:
                    try:
                        await self.bot.unload_extension(f"src.modules.{ext[:-3]}")
                    except commands.ExtensionNotLoaded:
                        pass
                    finally:
                        await self.bot.load_extension(f"src.modules.{ext[:-3]}")
                except commands.ExtensionFailed as E:
                    traceback_string = "".join(traceback.format_exception(etype=None, value=E, tb=E.__traceback__)) # type: ignore 
                    embed.title="Reloaded Cogs:"
                    embed.colour = discord.Colour.red()
                    embed.description = f"`\U0000274C` `{ext}`\n```{traceback_string}```"
                    await interaction.edit_original_response(embed=embed)
                else:
                    embed.title="Reloaded Cogs:"
                    embed.colour = discord.Colour.green()
                    embed.description = f"`\U00002705` `{ext}`"
                    await interaction.edit_original_response(embed=embed)

    @reload.autocomplete("cog")
    async def reload_autocomplete(self, interaction: discord.Interaction, user_input: str) -> List[app_commands.Choice[str]]:
        user_input = user_input.lower()
        cogs = [cog for cog in self.bot.cogs if user_input in cog.lower()]
        return [
            app_commands.Choice(name=cog, value=cog) for cog in cogs
        ]


        

async def setup(bot: TheBot):
    await bot.add_cog(Owner(bot))

"""
The Bot Instance.
"""

# Standard Libraries
import os
import logging

# External Libraries
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime

# Local Libraries
from .utils import *

from typing import Any, Dict


class TheBot(commands.Bot):
    """The Bot"""
    def __init__(self, *args, **kwargs) -> None:
        """Initialising the Bot"""
        logger = kwargs.pop("logger")
        super().__init__(*args, **kwargs)
        self.logger: logging.Logger = logger
   
    @property
    def info(self) -> Dict[str, Any]:
        """Returns the Data from 'info.json'"""
        return read_json(self.cwd + "/config/" + "info.json")
    
    @property
    def cwd(self) -> str:
        """Returns the Current Directory Path."""
        return resolve_path()

    def log(self, text: str) -> None: 
        """Log to a File"""
        with open("log.txt", "a") as File:
            File.write(f"[{str(datetime.now())}]\n{text}\n")


    # DISCORD-EVENTS
    async def setup_hook(self):
        """Initalisation"""
        # Creating Session
        self.session = aiohttp.ClientSession(loop=self.loop)

        # Loading Cogs
        for file in os.listdir(self.cwd + "/modules"):
            if file.endswith(".py") and not file.startswith("_"):
                await self.load_extension(f"src.modules.{file[:-3]}")
        
        # Loading Commands
        await self.tree.sync()

    async def on_ready(self):
        """Called when the Bot is READY"""
        os.system("cls" if os.name == "nt" else "clear")
        self.logger.info(f"{self.user} is READY!")
        self.logger.info(f"Bot ID: {self.user.id}")
        self.logger.info(f"Guild Count: {len(self.guilds)}\n")
    
    async def on_message(self, message: discord.Message):
        """Called when the Bot sees a Message"""
        return # As there are No Prefixed Commands

"""
The Main-Running File.
"""

import logging
import coloredlogs
import discord

from src.bot import TheBot

if __name__ == "__main__":
    # Setting-Up Logs
    logger = logging.getLogger("discord")
    coloredlogs.install(
        logger=logger,
        fmt="%(asctime)s [%(levelname)s] %(message)s"
    )
  
    # Initialising Bot
    bot = TheBot(
        command_prefix="!", # Compulsory
        case_insensitive=True,
        owner_id=1042669689844805713, # Change based on your ID
        intents=discord.Intents.default(),
        logger=logger
    )

    # Running the Bot
    bot.run(
        bot.info['DISCORD-TOKEN'],
        log_handler=None
    )

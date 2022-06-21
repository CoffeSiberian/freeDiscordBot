from functions.dirt import getConf
from bot.bot_main import Bot

import os

config = getConf()

os.system('cls')
bot = Bot(command_prefix=config['prefix'])
bot.run(config['DISCORD_TOKEN'])
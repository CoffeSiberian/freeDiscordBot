from functions.dirt import getConf
from bot.bot_main import Bot

config = getConf()

bot = Bot(command_prefix=config['prefix'])
bot.run(config['DISCORD_TOKEN'])
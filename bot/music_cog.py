from operator import truediv
from discord.ext import commands

from functions.dirt import getConf
from bot.validations_cog import validaciones

config = getConf()

class musica(commands.Cog):

    def __init__(self, bot) -> None:
        self.FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
        'options': '-vn'
        }
        self.ffmpeg = config['ffmpeg_dir']
        self.voldef = config['volumen']
        self.bot = bot
        self.validacion = validaciones(bot)

    @commands.command()
    async def conectar(self, ctx):
        status = await self.validacion.isConected(ctx)
        if await self.validacion.sameChannel(ctx) != True:
            return
        if status != False:
            if status.is_connected() == True:
                return
        await ctx.author.voice.channel.connect()
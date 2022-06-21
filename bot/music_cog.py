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
        if await self.validacion.isConectedChannel(ctx) != True:
            return await ctx.send("Conecta primero a un canal "+str(ctx.author.mention))
        if await self.validacion.isConected(ctx):
            return await ctx.send("Ya me encuentro conectado "+str(ctx.author.mention))
        await ctx.author.voice.channel.connect()
    
    @commands.command()
    async def desconectar(self, ctx):
        if await self.validacion.isConected(ctx):
            if await self.validacion.sameChannel(ctx) != True:
                return
            if await self.validacion.isPlaying(ctx):
                await self.stop(ctx)
            return await ctx.voice_client.disconnect()
        await ctx.send("No me encuentro conectado a un canal actualmente "+str(ctx.author.mention))

    @commands.command()
    async def stop(self, ctx):
        if await self.validacion.isConected(ctx):
            if await self.validacion.sameChannel(ctx):
                ctx.voice_client.stop()
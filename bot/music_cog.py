from discord.ext import commands
import discord

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
        self.prefix = config['prefix']
        self.bot = bot
        self.validacion = validaciones(bot)

    def pcmAudio(self, url):
        return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=url, executable=self.ffmpeg, **self.FFMPEG_OPTIONS))

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
    async def pausa(self, ctx):
        if self.validacion.isConected:
            if self.validacion.sameChannel:
                if self.validacion.isPlaying:
                    return ctx.voice_client.pause()

    @commands.command()
    async def continuar(self, ctx):
        if self.validacion.isConected:
            if self.validacion.sameChannel:
                if self.validacion.isPlaying:
                    return ctx.voice_client.resume()

    @commands.command()
    async def stop(self, ctx):
        if await self.validacion.isConected(ctx):
            if await self.validacion.sameChannel(ctx):
                ctx.voice_client.stop()
    
    @commands.command()
    async def play(self, ctx, stream='None'):
        if await self.validacion.isPlaying(ctx) == False:
            if await self.validacion.isConectedChannel(ctx) == False:
                return
            elif await self.validacion.isConected(ctx) == False:
                return await ctx.send(f'Utiliza {self.prefix}conectar primero {str(ctx.author.mention)}')
            elif await self.validacion.isConected(ctx):
                if await self.validacion.sameChannel(ctx) != True:
                    return
                if stream != 'None':
                    ctx.voice_client.play(self.pcmAudio(stream))
                    ctx.voice_client.source.volume = self.voldef/100
                    await ctx.send(f'Escuchas: {stream} - Volumen: {str(self.voldef)}')
                else:
                    await ctx.send(f'Tienes que usar {self.prefix}play [URL-stream] {str(ctx.author.mention)}')
        else:
            await ctx.send(f'Ya me encuentro reproduciendo música {str(ctx.author.mention)} Utiliza {self.prefix}stop')
from discord.ext import commands
import discord
import validators

from functions.dirt import getConf
from bot.validations_cog import validaciones
from apis.youtubeapi import youtube

config = getConf()

class MusicaYT(commands.Cog):

    def __init__(self, bot):
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
        self.apiyt =youtube()

    def pcmAudio(self, url):
        return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=url, executable=self.ffmpeg, **self.FFMPEG_OPTIONS))

    async def afterPlay(self, ctx, yplay):
        if yplay == None:
            await ctx.send(f'No encotramos lo que buscas o tu URL no es correcta {str(ctx.author.mention)}')
            return False
        if await self.validacion.isPlaying(ctx):
            return False
        return True

    @commands.command()
    async def yt(self, ctx, url='None'):
        v = await self.validacion.isConected(ctx)
        if await self.validacion.isConectedChannel(ctx) != True:
            return
        elif v == False:
            await ctx.send(f'Utiliza {self.prefix}conectar primero {str(ctx.author.mention)}')
            return
        elif v != False:
            if await self.validacion.sameChannel(ctx) != True:
                return
        if url != 'None':
            if validators.url(url):
                yplay = self.apiyt.findVideoInfoURL(url)
                if await self.afterPlay(ctx, yplay):
                    await self.yt_play(ctx, yplay['url'])
                    return await ctx.send(f'Escuchas: {yplay["title"]} - Volumen: {str(self.voldef)}')
            else:
                yplay = self.apiyt.search(url)
                if await self.afterPlay(ctx, yplay):
                    await self.yt_play(ctx, yplay["entries"][0]["url"])
                    return await ctx.send(f'Escuchas: {yplay["entries"][0]["title"]} - Volumen: {str(self.voldef)}')
        else:
            return await ctx.send(f'Tienes que usar {self.prefix}yt [URL] {str(ctx.author.mention)}')

    async def yt_play(self, ctx, url):
        ctx.voice_client.play(source=self.pcmAudio(url))
        ctx.voice_client.source.volume = self.voldef/100
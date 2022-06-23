from discord.ext import commands

from functions.dirt import getConf
from bot.nocogs.validations import validaciones
from bot.nocogs.play_sound import PlaySoundBot
from bot.nocogs.spotify_music import MusicaSP
from bot.nocogs.youtube_music import MusicaYT
from apis.youtubeapi import youtube
from apis.spotifyapi import spotifyPlay

config = getConf()

class Musica(commands.Cog):

    def __init__(self, bot) -> None:
        self.voldef = config['volumen']
        self.prefix = config['prefix']
        self.spClienId = config['spotify_clienId']
        self.spClienSecret = config['spotify_cliensecret']
        self.bot = bot
        self.validacion = validaciones(bot)
        self.apiyt = youtube()
        self.pmusic = PlaySoundBot(bot, self.apiyt)
        self.apisp = spotifyPlay(self.spClienId, self.spClienSecret)
        self.musicaSp = MusicaSP(bot, self.pmusic, self.apiyt, self.apisp)
        self.musicaYt = MusicaYT(bot, self.pmusic, self.apiyt)

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
    async def vol(self, ctx, volume=-1):
        if await self.validacion.isPossibleChangeVol(ctx):
            if volume >=1 and volume <= 100: 
                ctx.voice_client.source.volume = volume/100
                return True
            await ctx.send(f'Tienes que ingresar un volumen entre 1 y 100 {str(ctx.author.mention)}')

    @commands.command()
    async def play(self, ctx, *args):
        parameter = " ".join(args[:])
        if parameter != '':
            if self.validacion.isUrl(parameter):
                try:
                    link = parameter.split(sep='.')[1]
                    if link == 'youtube' or link == 'be':
                        return await self.musicaYt.ytUrl(ctx, parameter)
                    elif link == 'spotify':
                        return await self.musicaSp.valid(ctx, parameter)
                    else:
                        return await self.urlPlay(ctx, parameter)
                except IndexError:
                    pass
        else:
            await ctx.send(f'Tienes que usar {self.prefix}play [lo que buscas] {str(ctx.author.mention)}')
            return False
        await self.musicaYt.ytSearch(ctx, parameter)

    async def urlPlay(self, ctx, stream):
        if await self.validacion.isPossiblePlay(ctx):
            await self.pmusic.playSound(ctx, stream)
            await ctx.send(f'Escuchas: {stream} - Volumen: {str(self.voldef)}')
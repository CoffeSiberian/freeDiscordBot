from discord.ext import commands

from functions.dirt import getConf
from bot.nocogs.validations import validaciones
from bot.nocogs.youtube_music import MusicaYT
from bot.nocogs.play_sound import PlaySoundBot

config = getConf()

class Musica(commands.Cog):

    def __init__(self, bot) -> None:
        self.voldef = config['volumen']
        self.prefix = config['prefix']
        self.bot = bot
        self.validacion = validaciones(bot)
        self.pmusic = PlaySoundBot()
        self.musicaYt = MusicaYT(bot, self.pmusic)

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
        if await self.validacion.isConected(ctx) == False:
            return await ctx.send(f'No me encuentro conectado a un canal actualmente {str(ctx.author.mention)}')
        elif await self.validacion.sameChannel(ctx) != True:
            return
        if ctx.voice_client.is_playing():
            if await self.validacion.sameChannel(ctx) != True:
                return
            if volume >=1 and volume <= 100: 
                ctx.voice_client.source.volume = volume/100
                return
        else:
            await ctx.send(f'No me encuentro reproduciendo música {str(ctx.author.mention)}')
            return
        return await ctx.send(f'Tienes que ingresar un volumen entre 1 y 100 {str(ctx.author.mention)}')

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
                    await self.pmusic.playSound(ctx, stream)
                    await ctx.send(f'Escuchas: {stream} - Volumen: {str(self.voldef)}')
                else:
                    await ctx.send(f'Tienes que usar {self.prefix}play [URL-stream] {str(ctx.author.mention)}')
        else:
            await ctx.send(f'Ya me encuentro reproduciendo música {str(ctx.author.mention)} Utiliza {self.prefix}stop')
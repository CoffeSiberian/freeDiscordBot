from functions.dirt import getConf
from bot.nocogs.validations import validaciones
from apis.youtubeapi import youtube

config = getConf()

class MusicaYT:

    def __init__(self, bot, playSound):
        self.voldef = config['volumen']
        self.prefix = config['prefix']
        self.bot = bot
        self.pmusic = playSound
        self.validacion = validaciones(bot)
        self.apiyt = youtube()

    async def afterPlay(self, ctx, yplay):
        if yplay == None:
            await ctx.send(f'No encotramos lo que buscas o tu URL no es correcta {str(ctx.author.mention)}')
            return False
        if await self.validacion.isPlaying(ctx):
            return False
        return True

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
            if self.validacion.isUrl(url):
                yplay = self.apiyt.findVideoInfoURL(url)
                if await self.afterPlay(ctx, yplay):
                    await self.playSound(ctx, yplay['url'])
                    return await ctx.send(f'Escuchas: {yplay["title"]} - Volumen: {str(self.voldef)}')
            else:
                yplay = self.apiyt.search(url)
                if await self.afterPlay(ctx, yplay):
                    await self.playSound(ctx, yplay["entries"][0]["url"])
                    return await ctx.send(f'Escuchas: {yplay["entries"][0]["title"]} - Volumen: {str(self.voldef)}')
        else:
            return await ctx.send(f'Tienes que usar {self.prefix}yt [URL] {str(ctx.author.mention)}')
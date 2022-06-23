from functions.dirt import getConf
from bot.nocogs.validations import validaciones

config = getConf()

class MusicaYT:

    def __init__(self, bot, playSound, yt_instance):
        self.voldef = config['volumen']
        self.prefix = config['prefix']
        self.bot = bot
        self.pmusic = playSound
        self.validacion = validaciones(bot)
        self.apiyt = yt_instance

    async def afterPlay(self, ctx, yplay):
        if yplay == None:
            await ctx.send(f'No encotramos lo que buscas o tu URL no es correcta {str(ctx.author.mention)}')
            return False
        return True
        
    async def ytUrl(self, ctx, url):
        if await self.validacion.isPossiblePlay(ctx):
            yplay = self.apiyt.findVideoInfoURL(url)
            if await self.afterPlay(ctx, yplay):
                await self.pmusic.playSound(ctx, yplay['url'])
                return await ctx.send(f'Escuchas: {yplay["title"]} - Volumen: {str(self.voldef)}')

    async def ytSearch(self, ctx, url):
        if await self.validacion.isPossiblePlay(ctx):
            yplay = self.apiyt.search(url)
            if await self.afterPlay(ctx, yplay):
                await self.pmusic.playSound(ctx, yplay["entries"][0]["url"])
                return await ctx.send(f'Escuchas: {yplay["entries"][0]["title"]} - Volumen: {str(self.voldef)}')
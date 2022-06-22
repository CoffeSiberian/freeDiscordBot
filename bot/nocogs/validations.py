import validators

from functions.dirt import getConf

config = getConf()

class validaciones:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.prefix = config['prefix']

    #validar si la URL es valida o no
    def isUrl(url) -> bool:
        return validators.url(url)

    #validar si ya se encuentra el bot conectado a un canal de voz
    async def isConected(self, ctx) -> bool:
        for r in self.bot.voice_clients:
            if r.guild == ctx.author.guild:
                if r.is_connected() == True:
                    return True
        return False

    #validar si se esta conectado a un canal de voz
    async def isConectedChannel(self, ctx) -> bool:
        if ctx.author.voice is None:
            return False
        return True
    
    #valida si el cliente esta en el mismo canal de voz que el bot
    async def sameChannel(self, ctx):
        if await self.isConectedChannel(ctx):
            if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
                return await ctx.send(f'Tienes que conectar en el canal que me encuentro {str(ctx.author.mention)}')
            return True

    #valida si existe musica actualmente en reproduccion
    async def isPlaying(self, ctx) -> bool:
        if await self.isConected(ctx):
            if ctx.voice_client.is_playing() == False:
                if ctx.voice_client.is_paused() == False:
                    return False
            return True 
        return False
    
    #validar si se puede reproducir musica o no
    async def isPossiblePlay(self, ctx) -> bool:
        if await self.isPlaying(ctx) == False:
            if await self.isConectedChannel(ctx) == False:
                await ctx.send(f'Tienes que conectar en el canal que me encuentro {str(ctx.author.mention)}')
                return False
            elif await self.isConected(ctx) == False:
                await ctx.send(f'Utiliza {self.prefix}conectar primero {str(ctx.author.mention)}')
                return False
            elif await self.isConected(ctx):
                if await self.sameChannel(ctx) != True:
                    return False
        else:
            await ctx.send(f'Ya me encuentro reproduciendo música {str(ctx.author.mention)} Utiliza {self.prefix}stop')
            return False
        return True

    #identificar que tipo de sonido se necesita
    async def whatIs(self, ctx, str):
        if self.isUrl(str):
            try:
                link = str.split(sep='.')[1]
                if link == 'youtube':
                    pass
                elif link == 'spotify':
                    pass
            except IndexError:
                pass
        
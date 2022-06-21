class validaciones():
    def __init__(self, bot) -> None:
        self.bot = bot

    #validar si ya se encuentra el bot conectado a un canal
    async def isConected(self, ctx):
        for r in self.bot.voice_clients:
            if r.guild == ctx.author.guild:
                if r.is_connected() == True:
                    await ctx.send("Ya me encuentro conectado "+str(ctx.author.mention))
                return r
        return False

    async def sameChannel(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("Conecta primero a un canal "+str(ctx.author.mention))
        return True
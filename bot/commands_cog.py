from discord.ext import commands

class comandos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def holacogs(self, ctx):
        await ctx.channel.send('soy un cogs')
from discord.ext import commands
import discord

from bot.commands_cog import comandos
from bot.music.music_cog import Musica

class Bot(commands.Bot):
    
    def __init__(self, command_prefix):
        self.prefix = command_prefix
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=discord.Intents.all())
    
    # Startup Information
    async def on_ready(self):
        print(f'Connected to bot: {self.user.name}')
        await self.change_presence(
            activity=discord.Activity(
            type=discord.ActivityType.listening, name=f'Use {self.prefix}'))
        await self.cogsAdd()

    async def cogsAdd(self):
        await self.add_cog(comandos(self))
        await self.add_cog(Musica(self))
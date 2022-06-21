from discord.ext import commands

from bot.commands_cog import comandos
from bot.music_cog import musica

class Bot(commands.Bot):
    
    def __init__(self, command_prefix):
        commands.Bot.__init__(self, command_prefix=command_prefix)
        self.add_commands()
    
    # Startup Information
    async def on_ready(self):
        print(f'Connected to bot: {self.user.name}')
    
    def add_commands(self):
        self.add_cog(comandos(self))
        self.add_cog(musica(self))
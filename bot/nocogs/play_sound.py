import discord
import asyncio

from functions.music_queue import Queue
from functions.dirt import getConf
from bot.nocogs.validations import validaciones

config = getConf()

class PlaySoundBot:
    
    def __init__(self, bot, yt_instance) -> None:
        self.FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
        'options': '-vn'
        }
        self.voldef = config['volumen']
        self.ffmpeg = config['ffmpeg_dir']
        self.apiyt = yt_instance
        self.validacion = validaciones(bot)
        self.queue = Queue()

    def pcmAudio(self, url):
        return discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(source=url, executable=self.ffmpeg, **self.FFMPEG_OPTIONS))
    
    async def playSound(self, ctx, *args):
        self.addQueue(*args)
        if self.queue.currentTrack != False:
            await self.play(ctx)

    async def nextSound(self, ctx):
        if self.queue.setNextTrack() != False:
            await self.play(ctx)

    def addQueue(self, *args):
        self.queue.add(*args)

    def getOnlyUrl(self):
        '''
        if within the list there are strings that are not a 
        url they will be searched on youtube
        '''
        value = self.queue.currentTrack
        if value != False:
            if self.validacion.isUrl('value'):
                return value
            yplay = self.apiyt.search(value)
            return yplay["entries"][0]["url"]

    async def play(self, ctx):
        ctx.voice_client.play(source=self.pcmAudio(
            self.getOnlyUrl()), 
            after=lambda : asyncio.run(await self.nextSound(ctx)))
        ctx.voice_client.source.volume = self.voldef/100
import discord
import asyncio

from functions.music_queue import Queue
from functions.dirt import getConf
from bot.nocogs.validations import validaciones
from bot.nocogs.base_msj import *

config = getConf()

class PlaySoundBot:
    
    def __init__(self, bot, yt_instance) -> None:
        self.FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
        'options': '-vn'
        }
        self.bot=bot
        self.voldef = config['volumen']
        self.ffmpeg = config['ffmpeg_dir']
        self.apiyt = yt_instance
        self.validacion = validaciones(bot)
        self.queueObj = []

    def createQueue(self, ctx):
        self.queueObj.append(Queue(ctx.guild.id))
        return ctx.guild.id
    
    def getQueue(self, ctx):
        for r in self.queueObj:
            if r.guildId == ctx.guild.id:
                return (r)
        return False
    
    def delQueue(self, obj):
        self.queueObj.remove(obj)

    def pcmAudio(self, url):
        return discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(source=url, executable=self.ffmpeg, **self.FFMPEG_OPTIONS))

    async def playSound(self, ctx, *args, names, img):
        queueobj = self.getQueue(ctx)
        if queueobj == False:
            self.createQueue(ctx)
            queueobj = self.getQueue(ctx)
        queueobj.add(*args, names=names, img=img)
        if queueobj.currentTrack != False:
            if ctx.voice_client.is_playing() == False:
                await self.play(ctx, queueobj)
            if type(args[0]) is list:
                await self.infoMusicMsjQueue(ctx, items=len(args[0]))
                await self.infoMusicMsj(ctx)
            else:
                await self.infoMusicMsjQueue(ctx)
                await self.infoMusicMsj(ctx)

    async def nextSound(self, ctx, obj):
        if obj.setNextTrack() != False:
            await self.play(ctx, obj)
            await self.infoMusicMsj(ctx)
            return
        self.delQueue(obj)

    def getOnlyUrl(self, obj):
        '''
        if within the list there are strings that are not a 
        url they will be searched on youtube
        '''
        value = obj.currentTrack
        if value != False:
            if self.validacion.isUrl(value.replace('-','')):
                return value
            yplay = self.apiyt.search(value)
            return yplay["entries"][0]["url"]

    async def play(self, ctx, obj):
        ctx.voice_client.play(source=self.pcmAudio(
            self.getOnlyUrl(obj)),
            after=lambda e: print('Player error: %s' % e) if e else asyncio.run_coroutine_threadsafe(self.nextSound(ctx, obj), self.bot.loop))
        ctx.voice_client.source.volume = self.voldef/100
        
    '''
    Here are the informative messages of the state of the music
    '''
    async def infoMusicMsj(self, ctx):
        obj = self.getQueue(ctx)
        if obj != False:
            await musicInfo(
            ctx, 
            obj.currentTrackName, 
            ctx.author.display_name, 
            ctx.author.avatar, 
            obj.currentTrackImg, 
            self.voldef
            )

    async def infoMusicMsjQueue(self, ctx, items=1):
        obj = self.getQueue(ctx)
        if obj != False:
            await musicAdded(
            ctx, 
            items,
            obj.lastTrackName, 
            ctx.author.display_name, 
            ctx.author.avatar, 
            obj.lastTrackImg
            )

    '''
    Here are the functions to interact with the queue using commands
    '''
    def commandsStop(self, ctx):
        obj = self.getQueue(ctx)
        if obj != False:
            obj.empty()
        return False

    def commandsBack(self, ctx):
        obj = self.getQueue(ctx)
        if obj != False:
            return obj.back()
        return False
    
    def commandsSkip(self, ctx, pos):
        obj = self.getQueue(ctx)
        if obj != False:
            return obj.skip(pos)
        return False
    
    def remainingQueue(self, ctx):
        obj = self.getQueue(ctx)
        if obj != False:
            return obj.upcoming[1], obj.currentTrackImg, obj.currentTrackName
        return False
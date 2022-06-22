import discord

from functions.dirt import getConf

config = getConf()

class PlaySoundBot:
    def __init__(self) -> None:
        self.FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
        'options': '-vn'
        }
        self.voldef = config['volumen']
        self.ffmpeg = config['ffmpeg_dir']

    def pcmAudio(self, url):
        return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=url, executable=self.ffmpeg, **self.FFMPEG_OPTIONS))
    
    async def playSound(self, ctx, url):
        ctx.voice_client.play(source=self.pcmAudio(url))
        ctx.voice_client.source.volume = self.voldef/100
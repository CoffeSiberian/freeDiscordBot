import discord

async def musicInfo(ctx, songName, autor, autorImg, soundImg, volume):
    embed=discord.Embed(title='Escuchas', description=songName, color=0xdc21eb)
    embed.set_author(name=autor, icon_url=autorImg)
    embed.add_field(name='Volumen', value=volume, inline=True)
    embed.set_thumbnail(url=soundImg)
    embed.set_footer(icon_url='https://i.imgur.com/qS4B6Ux.png', text='by: Github.com/CoffeSiberian')
    await ctx.send(embed=embed)

async def musicAdded(ctx, items, songName, autor, autorImg, soundImg):
    embed=discord.Embed(title=f'Añadiste a la cola {items} items', description=songName, color=0xdc21eb)
    embed.set_author(name=autor, icon_url=autorImg)
    embed.set_thumbnail(url=soundImg)
    embed.set_footer(icon_url='https://i.imgur.com/qS4B6Ux.png', text='by: Github.com/CoffeSiberian')
    await ctx.send(embed=embed)

async def musicQueueList(ctx, queue, currentTrackImg, currentTrack):
    inter = 0

    embed=discord.Embed(title=f'Escuchas - {currentTrack}', 
    description='Utiliza next para la siguiente canción o skip para una canción de la lista de espera', 
    color=0xdc21eb)

    embed.add_field(name='Cola de musica', value=f'Existen {len(queue)} canciones en cola' , inline=False)
    embed.set_thumbnail(url=currentTrackImg)
    for r in queue:
        inter += 1
        embed.add_field(name=f'`{inter}` - {r}', value='\u200b' ,inline=False)
    embed.set_footer(icon_url='https://i.imgur.com/qS4B6Ux.png', text='by: Github.com/CoffeSiberian')
    await ctx.send(embed=embed)
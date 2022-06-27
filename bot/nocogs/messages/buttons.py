import discord

class QueueButton(discord.ui.View):
    def __init__(self, *, timeout=180, embed=None, upcoming):
        super().__init__(timeout=timeout)
        self.base_embed = embed
        self.upcoming = upcoming
        self.coun = 0
        self.last = 0
        self.page = 0
        self.setNext()
    
    def setNext(self):
        names = self.upcoming[self.coun:self.coun+10]
        self.last = 0
        if len(names) != 0:
            self.base_embed.clear_fields()
            self.base_embed.add_field(name='Cola de musica', value=f'Existen {len(self.upcoming)} canciones en cola' , inline=False)
            for r in names:
                self.coun += 1
                self.last += 1
                self.base_embed.add_field(name=f'`{self.coun}` - {r}', value='\u200b', inline=True)
        if self.last == 10:
            self.last = 0
        self.enableDisable()
        self.pageSet(self.page+1)
        return self.base_embed
    
    def setBack(self):
        if self.last == 0:
            first = (self.coun-self.last)-20
        else:
            first = (self.coun-self.last)-10
            
        self.last = 0
        names = self.upcoming[first:first+10]
        if len(names) != 0:
            self.base_embed.clear_fields()
            self.base_embed.add_field(name='Cola de musica', value=f'Existen {len(self.upcoming)} canciones en cola' , inline=False)
            self.coun = first
            for r in names:
                self.coun += 1
                self.base_embed.add_field(name=f'`{self.coun}` - {r}', value='\u200b', inline=True)
        self.enableDisable()
        self.pageSet(self.page-1)
        return self.base_embed

    def enableDisable(self):
        if self.coun == len(self.upcoming) and self.next.disabled == False:
            self.next.disabled = True
        elif self.coun < len(self.upcoming) and self.next.disabled == True:
            self.next.disabled = False
        if self.coun <= 10 and self.back.disabled == False:
             self.back.disabled = True
        elif self.coun >= 11 and self.back.disabled == True:
            self.back.disabled = False
    
    def pageSet(self, page):
        spit = str(len(self.upcoming)/10)
        split = spit.split(sep='.')
        self.page = page
        if int(split[1]) != 0:
            self.count.label = f'Page {self.page}/{int(split[0])+1}'
        else:
            self.count.label = f'Page {self.page}/{int(split[0])}'

    @discord.ui.button(label="Back", style=discord.ButtonStyle.primary, disabled=True)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.count.label = self.coun
        await interaction.response.edit_message(embed=self.setBack(), view=self)

    @discord.ui.button(label="None", style=discord.ButtonStyle.gray, disabled=True)
    async def count(self, interaction: discord.Interaction, child: discord.ui.Button):
        pass

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.count.label = self.coun
        await interaction.response.edit_message(embed=self.setNext(), view=self)
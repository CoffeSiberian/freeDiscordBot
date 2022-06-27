import discord

class QueueButton(discord.ui.View):
    def __init__(self, *, timeout=180, embed=None, upcoming):
        super().__init__(timeout=timeout)
        self.base_embed = embed
        self.upcoming = upcoming
        self.coun = 0
        self.last = 0
        self.setNext()
    
    def setNext(self):
        names = self.upcoming[self.coun:self.coun+10]
        self.last = 0
        if len(names) != 0:
            self.base_embed.clear_fields()
            for r in names:
                self.coun += 1
                self.last += 1
                self.base_embed.add_field(name=f'`{self.coun}` - {r}', value='\u200b', inline=False)
        if self.last == 10:
            self.last = 0
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
            self.coun = first
            for r in names:
                self.coun += 1
                self.base_embed.add_field(name=f'`{self.coun}` - {r}', value='\u200b', inline=False)
        return self.base_embed

    @discord.ui.button(label="Back", style=discord.ButtonStyle.primary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.count.label = self.coun
        await interaction.response.edit_message(embed=self.setBack(), view=self)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.gray, disabled=True)
    async def count(self, interaction: discord.Interaction, child: discord.ui.Button):
        pass

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.count.label = self.coun
        await interaction.response.edit_message(embed=self.setNext(), view=self)
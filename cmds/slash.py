import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from core.classes import Cog_Extention


class Slash(Cog_Extention):
    
    PinTwo = 935930665663340685
         
    @nextcord.slash_command(name = "hello", description="say hello to bot", guild_ids=[PinTwo])
    async def hello(self, interaction: Interaction):
        author = str(interaction.user)
        await interaction.response.send_message(f"hello {author[:-5]} :)")

def setup(client):
    client.add_cog(Slash(client))   
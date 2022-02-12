import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE.useful_function import func
from MODULE import EMBED
import datetime


class Help(Cog_Extention):
    
    PinTwo = 935930665663340685
    
    @nextcord.slash_command(name = "help", description="help message", guild_ids=[PinTwo])
    async def help(self, interaction: Interaction):
        embed = EMBED.Embed()
        embed.add(name='p!tags', value='add some tags to your roles', inline=False)
        embed.add(name="p!close", value='close the thread', inline=False)
        embed = embed.output()
        embed.set_footer(text = "You can also type / to check slash commands.")
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(Help(client))

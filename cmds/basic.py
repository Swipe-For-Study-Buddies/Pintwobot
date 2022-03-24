import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE import EMBED 

class Event(Cog_Extention):

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.delarr = []
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        msg = message.content
        if message.author != self.client.user:
            if "早ㄤ" in msg:
                await message.channel.send("早ㄤ!")
            elif "早安" in msg:
                await message.channel.send("早ㄤ")



def setup(client):
    client.add_cog(Event(client))
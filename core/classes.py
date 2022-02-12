import nextcord
from nextcord.ext import commands

class Cog_Extention(commands.Cog):
    def __init__(self, client):
        self.client = client
        
def setup(client):
  client.add_cog(Cog_Extention(client))

import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE import EMBED


class Member(Cog_Extention):

    @commands.Cog.listener()
    async def on_member_join(self, member):
      if member.guild.id == 935930665663340685:
        channel = member.guild.system_channel
        embed = EMBED.Embed()
        embed.add(name = "Welcome", value = f"{member.name} has droped in. \n", inline = False)
        embed = embed.output()
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
      if member.guild.id == 935930665663340685:
        channel = member.guild.system_channel
        embed = EMBED.Embed()
        embed.add(name = "Oh No!", value = f"{member.name} has gone.", inline = False)
        embed = embed.output()
        await channel.send(embed = embed)


def setup(client):
    client.add_cog(Member(client))

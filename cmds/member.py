import asyncio
import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE import EMBED


class Member(Cog_Extention):

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
      if member.guild.id == 935930665663340685:
        channel = member.guild.system_channel
        embed = EMBED.Embed()
        embed.add(name = "Welcome", value = f"{member.name} has droped in. \n", inline = False)
        embed = embed.output()
        await channel.send(embed = embed)
        
        guild:nextcord.Guild = self.client.get_guild(935930665663340685)
        overwrite = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            member: nextcord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel(
          name=f"intro-{member.name}",
          overwrites=overwrite,
          position=4
        )
        welcome_message = ("```"
                           "Welcome to PinTwo, "
                          "for the full experience, please typing `p!tags` to get the role, "
                          "if you've got the roles, typing `p!close_tag` to finish the verify, "
                          "after admin accept your appilcation, "
                          "you could enjoy your journal in this server:D"
                          "```")
        admin_channel = self.client.get_channel(943501281841016866)
        await channel.send(member.mention)
        await channel.send(welcome_message)
        await admin_channel.send(f"{member.name} is come in")
        
    @commands.command()
    async def close_tag(self, ctx: commands.Context):
      if ctx.channel.name.startswith("intro"):
            await ctx.send("Your going to close this channal...")
            if ctx.author.name == ctx.channel.name[6:]:
                role = ctx.guild.get_role(944496251938942996) 
                await ctx.author.add_roles(role)   
            await asyncio.sleep(0.5)
            await ctx.channel.delete()
            await ctx.author.send("You can enjoy your journal now")
    
 
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

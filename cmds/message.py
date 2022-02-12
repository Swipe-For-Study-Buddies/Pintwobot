import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE import EMBED 


def check_manage(ctx):
    return ctx.author.id == 625302301313073192 or ctx.author.id == 768806063545516034


class Say(Cog_Extention):
    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.check(check_manage)
    @commands.command()
    async def purge(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)
        embed = EMBED.Embed()
        embed.add('p!purge',f'purge {num} message', False)
        embed = embed.output()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Say(client))

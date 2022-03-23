import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os
import requests
from core.classes import Cog_Extention
from MODULE import EMBED


TOKEN = os.environ['TOKEN']
BotCommandChannel = os.environ['BotCommandChannel']


intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='p!', intents=intents)
client.remove_command('help')

def check(ctx):
    return ctx.author.id == 625302301313073192
    

@client.event
async def on_ready():
  print('>> Bot is online ')
  r = requests.head(url="https://discord.com/api/v1")
  try:
      print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
  except:
      print("No rate limit")
      


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} (ms)')

@client.slash_command(name = "tests", description = "testing", guild_ids=[935930665663340685])
async def tests(interaction: Interaction):
    await interaction.response.send_message("testing")

@client.command()
@commands.check(check)
async def load(ctx, file_name):
    client.load_extension(f"cmds.{file_name}")
    embed = EMBED.Embed()
    embed.add("p!load", f"{file_name} loaded successfully", False)
    embed = embed.output()
    await ctx.send(embed=embed)



@client.command()
@commands.check(check)
async def reload(ctx, file_name):
    client.reload_extension(f"cmds.{file_name}")
    embed = EMBED.Embed()
    embed.add('p!reload',f"{file_name} re-loaded successfully", False)
    embed = embed.output()
    await ctx.send(embed=embed)



@client.command()
@commands.check(check)
async def unload(ctx, file_name):
    client.unload_extension(f"cmds.{file_name}")
    embed = EMBED.Embed()
    embed.add('p!unload',f"{file_name} un-loaded successfully", False)
    embed = embed.output()
    await ctx.send(embed=embed)


for file in os.listdir('./cmds'):
    if file.endswith('.py') :
        if file != 'test.py':
            client.load_extension(f"cmds.{file[:-3]}")

if __name__ == "__main__":
  client.run(TOKEN)

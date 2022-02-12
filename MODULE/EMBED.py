import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
from MODULE.useful_function import func

class Embed():
  def __init__(self):
    self.embed  = nextcord.Embed(color=0x86ff00)
    self.embed.set_author(name="potato neko", url="https://youtu.be/dQw4w9WgXcQ",
                      icon_url="https://cdn.discordapp.com/emojis/905814312252215356.png?size=128")
    self.embed.set_thumbnail(
        url="https://cdn.discordapp.com/emojis/897077370530431026.png?size=128")
    self.embed.set_footer(text=func.get_date())

  
  def add(self, name, value, inline = True):
    self.embed.add_field(name=name,
                        value=value,
                        inline=inline)
  def output(self):
    return self.embed

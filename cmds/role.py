from typing import List
import nextcord
from nextcord.ext import commands
from core.classes import Cog_Extention
import json
import datetime


PinTwo = 935930665663340685

with open('JSONHome/role.json', 'r', encoding='utf-8') as f:
    roles = json.load(f)
    f.close()

def check(ctx: commands.Context):
    for role in ctx.author.roles:
        if role.id == 936117143286730772:
            return True
    else:
        return False

class RoleDropdown(nextcord.ui.Select):
    def __init__(self, client, choose, ctx):

        # Set the options that will be presented inside the dropdown
        self.choose = choose
        self.client = client
        self.ctx = ctx
        options = []
        for data in roles[self.choose].items():
            options.append(nextcord.SelectOption(
                label=data[0], description=f'{data[0]}', value=data[1]))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select one of these option...',
                         max_values=2, options=options)
    async def callback(self, interaction: nextcord.Interaction):
        for value in self.values:
            guild = self.client.get_guild(935930665663340685)
            user = self.ctx.author      
            role = guild.get_role(int(value))    
            await user.add_roles(role)  
        await interaction.response.send_message("success")
    
class RoleDropdownView(nextcord.ui.View):
    def __init__(self, client, choose, ctx):
        super().__init__()
        self.client = client
        self.choose = choose
        # Adds the dropdown to our view object.
        self.add_item(RoleDropdown(self.client, self.choose, ctx))
        
class Dropdown(nextcord.ui.Select):
    def __init__(self, client, ctx):

        # Set the options that will be presented inside the dropdown
        self.client = client
        self.ctx = ctx
        options = []
        for choose in roles:
            options.append(nextcord.SelectOption(
                label=choose, description=f'{choose}'))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select one of these option...',
                         min_values=1,max_values=1, options=options)
    async def callback(self, interaction: nextcord.Interaction):
        self.choose = self.values[0]
        # self.item_dict = data_dict[self.values[0]]
        # self.item_keys = list(self.item_dict.keys())
        view = RoleDropdownView(self.client, self.choose, self.ctx)

        await interaction.response.send_message("select some of these tags :D", view=view)
    
class DropdownView(nextcord.ui.View):
    def __init__(self, client, ctx):
        super().__init__()
        self.client = client
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.client, ctx))
        
class Create_role():
    def __init__(self, ctx: commands.Context, role_name: str):
        self.author: nextcord.Member = ctx.author
        self.guild: nextcord.Guild = ctx.guild
        self.role_name = role_name
        
    async def create_role(self):
        reason = f"Create {self.role_name} by {self.author.name}"
        self.role = await self.guild.create_role(
            name = self.role_name,
            reason=reason
        )
    async def create_class(self):
        overwrite = {
            self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            self.role: nextcord.PermissionOverwrite(read_messages=True)
        }
        self.category: nextcord.CategoryChannel = await self.guild.create_category(
            name = self.role_name,
            overwrites=overwrite         
        )
        self.chat_channel: nextcord.TextChannel = await self.guild.create_text_channel(
            name = "Chat",
            category = self.category         
        )
        self.help_channel: nextcord.TextChannel = await self.guild.create_text_channel(
            name = "Help",
            category = self.category         
        )
        self.share_channel: nextcord.TextChannel = await self.guild.create_text_channel(
            name = "Resource Sharing",
            category = self.category         
        )
        
class Roles(Cog_Extention):
    
    global PinTwo
    
    @commands.command()
    async def tags(self, ctx):
        """Get the tags"""

        # Create the view containing our dropdown
        view = DropdownView(self.client, ctx)

        # Sending a message containing our view
        await ctx.send('Pick an category:', view=view)
    
    @commands.command()
    @commands.check(check)
    async def add_tag(self, ctx: commands.Context,role_category: str, role_name: str):
        create = Create_role(ctx, role_name)
        await create.create_role()
        await create.create_class()
    
        if not role_category in roles.keys():
            roles[role_category] = {}
        roles[role_category][create.role.name] = create.role.id
        
        with open('JSONHome/role.json', 'w', encoding='utf8') as dataFile:
            json.dump(roles, dataFile, ensure_ascii=False, indent=4)
            dataFile.close()
        
def setup(client):
    client.add_cog(Roles(client))   
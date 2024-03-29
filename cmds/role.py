from http import client
import nextcord
from nextcord.ext import commands
from numpy import choose
from core.classes import Cog_Extention
import json

PinTwo: int = 935930665663340685
roles: dict = {}

with open('JSONHome/role.json', 'r', encoding='utf-8') as f:
    roles = json.load(f)
    
def check(ctx: commands.Context) -> bool:
    for role in ctx.author.roles:
        if role.id == 936117143286730772:
            return True
    else:
        return False
    
class Roles(Cog_Extention):
    
    @commands.command()
    async def tags(self, ctx):
        """Get the tags"""
        self.ctx: commands.Context = ctx
        # Create the view containing our dropdown
        view = DropdownView()

        # Sending a message containing our view
        await ctx.send('Pick an category:', view=view)
    
    @commands.command()
    @commands.check(check)
    async def add_tag(self, ctx: commands.Context,role_category: str, role_name: str):
        self.role_name = role_name
        create = Create_role(ctx, role_name)
        await create.create_role()
        await create.create_class()
    
        if not role_category in roles.keys():
            roles[role_category] = {}
        roles[role_category][create.role.name] = create.role.id
        
        with open('JSONHome/role.json', 'w', encoding='utf8') as dataFile:
            json.dump(roles, dataFile, ensure_ascii=False, indent=4)

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

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(Dropdown()) 
        
class Dropdown(nextcord.ui.Select, Roles):
    def __init__(self):
        super(Roles).__init__()
        # Set the options that will be presented inside the dropdown
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
        # self.item_dict = data_dict[self.values[0]]
        # self.item_keys = list(self.item_dict.keys())
        self.value = self.values[0]
        print(self.value)
        view = RoleDropdownView(self.value)

        await interaction.response.send_message("select some of these tags :D", view=view)      

class RoleDropdownView(nextcord.ui.View):
    def __init__(self, value):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(RoleDropdown(value))
        
class RoleDropdown(nextcord.ui.Select, Roles):
    def __init__(self, value):
        super().__init__()
        self.value = value
        # Set the options that will be presented inside the dropdown
        options = []
        for data in roles[self.value].items():
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
        
def setup(client):
    client.add_cog(Roles(client)) 
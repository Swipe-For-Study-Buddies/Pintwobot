from typing import List
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from core.classes import Cog_Extention
import json


with open("JSONHome/role_exception.json", 'r', encoding='utf-8') as f:
    ROLES_EXCEPTION = json.load(f)
    f.close()

PinTwo = 935930665663340685
ThreadID = 937346276515782656

class RoleDropdown(nextcord.ui.Select):
    def __init__(self, client: nextcord.Client, user_list: List, thread: nextcord.Thread):

        # Set the options that will be presented inside the dropdown
        self.client = client
        self.user_list = user_list
        self.thread = thread
        options = []
        length = len(self.user_list)
        for user in self.user_list:
            options.append(nextcord.SelectOption(
                label=user.name, value=user.id, description=f'{user.name}'))#之後接DB在description放個人簡介

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select one of these option...',
                        max_values=min(length, 3), options=options)
    async def callback(self, interaction: nextcord.Interaction):
        user_list = []
        for user_id in self.values:
            User: nextcord.User = self.client.get_user(int(user_id))
            user_list.append(User)
        for user in user_list:
            await self.thread.send(content= user.mention)
        
class RoleDropdownView(nextcord.ui.View):
    def __init__(self, client, user_list, thread):
        super().__init__()
        self.client = client
        # Adds the dropdown to our view object.
        self.add_item(RoleDropdown(self.client, user_list, thread))

class OpenThread():
    def __init__(self, client: nextcord.Client, role_id: int, user: nextcord.User):
        global PinTwo, ThreadID 
        self.client = client
        self.user = user
        self.guild: nextcord.Guild = self.client.get_guild(PinTwo)
        self.role: nextcord.Role = self.guild.get_role(role_id)      
        self.ThreadChannel: nextcord.TextChannel = self.client.get_channel(ThreadID)

    async def create_thread(self):
        thread = await self.ThreadChannel.create_thread(
            name = f"{self.role.name} discussions by {self.user.name}.",
            type = nextcord.ChannelType.public_thread
        )
        await self.ThreadChannel.send(f"discussions for {self.role.name} is created by {self.user.name}.")
        await thread.send(content= self.user.mention)
        await thread.send("type something if you want to close the thread.")
        user_list: List = []
        for user in self.role.members:
            if user != self.user:
                user_list.append(user)     
        # await thread.send(len(self.role.members))
        if len(user_list)==0:
            ctx = "there's no user having this tag, you could go to <#937345532895051786> to find someone to hang out with"
            await thread.send(content=ctx)
        else:    
            view = RoleDropdownView(self.client, user_list, thread)
            await thread.send("hi", view= view)

class Dropdown(nextcord.ui.Select):
    def __init__(self, client, role_list, user):

        # Set the options that will be presented inside the dropdown
        self.client = client
        self.role_list = role_list
        self.user = user
        options = []
        for role in self.role_list:
            options.append(nextcord.SelectOption(
                label=role.name, value=role.id , description=f'{role.name}'))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select one of these option...',
                         min_values=1,max_values=1, options=options)
    async def callback(self, interaction: nextcord.Interaction):
        # self.item_dict = data_dict[self.values[0]]
        # self.item_keys = list(self.item_dict.keys())

        #await interaction.response.send_message(self.values[0])
        # return self.values[0]
        thread = OpenThread(self.client, int(self.values[0]), self.user)
        #await interaction.response.send_message(f"{type(thread.guild)}, {type(thread.client)}, {type(thread.role)}")
        await thread.create_thread()
    
class DropdownView(nextcord.ui.View):
    def __init__(self, client, role_list, user):
        super().__init__()
        self.client = client
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.client, role_list, user))

class Thread(Cog_Extention):
    
    global PinTwo
    
    @nextcord.slash_command(name = "createthread", guild_ids=[PinTwo])
    async def createthread(self, interaction: Interaction):
        global ROLES_EXCEPTION
        USER = interaction.user
        Roles_list = []
        for role in USER.roles:
            if not role.id in ROLES_EXCEPTION:
                Roles_list.append(role)
        view = DropdownView(self.client, Roles_list, USER)
        channel = interaction.channel
        await interaction.response.send_message("choose a tags that you would like to chat for", view= view) 
        
    @commands.command()
    async def close(self, ctx: commands.Context):
        if type(ctx.channel) == nextcord.Thread:
            await ctx.channel.edit(locked=True, archived=True)
            channel = self.client.get_channel(ThreadID)
            await channel.send(f"{ctx.author.mention} Your thread has been closed")

        
def setup(client):
    client.add_cog(Thread(client))  
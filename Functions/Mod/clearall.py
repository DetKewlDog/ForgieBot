from time import sleep

from interactions import *

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="clearall", description="Use this command to clear all channels (100 messages at a time)", default_member_permissions=Permissions.ADMINISTRATOR)

    async def _clearall(self, ctx: CommandContext):
        await ctx.send("Please wait for the operation to finish!", ephemeral=True)
        for channel in ctx.guild.channels:
            if not channel.type == ChannelType.GUILD_TEXT:
                continue
            channel = Channel(id=channel.id, type=ChannelType.GUILD_TEXT, guild_id=ctx.guild_id, _client=self.client._http)
            messages = await channel.get_history(100)
            await ctx.send(f'Found {len(messages)} messages in {channel.mention}!', ephemeral=True)
            for message in messages:
                await message.delete()
                sleep(0.5)

def setup(client):
    Ext(client)
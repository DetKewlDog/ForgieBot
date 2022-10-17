from time import sleep

from interactions import *

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="clear", description="Use this command to clear a channel", default_member_permissions=Permissions.ADMINISTRATOR, options=[
            Option(name="channel", description="The target channel", type=OptionType.CHANNEL, required=True),
            Option(name="amount", description="Amount of messages to purge (max 100 at a time)", type=OptionType.INTEGER, required=False)])

    async def _clear(self, ctx: CommandContext, channel, amount = 100):
        if amount <= 0 or amount > 100:
            ctx.send('Amount must be more than 0 and less or equal to 100!', ephemeral=True)
        channel = Channel(id=channel.id, type=ChannelType.GUILD_TEXT, guild_id=ctx.guild_id, _client=self.client._http)
        messages = await channel.get_history(amount)
        await ctx.send(f'Found {len(messages)} messages in {channel.mention}! Please wait for the operation to finish!', ephemeral=True)
        for message in messages:
            await message.delete()
            sleep(0.5)
        await ctx.send('Removed messages!', ephemeral=True)

def setup(client):
    Ext(client)
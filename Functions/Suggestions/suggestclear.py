from interactions import *
from settings import *
from suggestion import *

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="suggestclear",
        description="Use this command to delete all suggestions",
        default_member_permissions=Permissions.ADMINISTRATOR
    )

    async def _suggestclear(self, ctx: CommandContext):
        with open(SUGGESTIONS_DIR, "r") as file:
            for line in file:
                msg_, id = line.split(' ')
                msg_id = msg_
                msg = await Message.get_from_url(msg_id, client=self.client._http)
                await msg.delete()
        with open(SUGGESTIONS_DIR, "w") as file:
            file.close()

        await ctx.send('Deleted suggestions!', ephemeral=True)

def setup(client):
    Ext(client)
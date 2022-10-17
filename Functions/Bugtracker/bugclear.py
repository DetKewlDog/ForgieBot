from interactions import *
from settings import *
from bugreport import *

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="bugclear",
        description="Use this command to delete all bugs",
        default_member_permissions=Permissions.ADMINISTRATOR
    )

    async def _bugclear(self, ctx: CommandContext):
        with open(BUG_REPORTS_DIR, "r") as file:
            for line in file:
                msg_, id, st = line.split(' ')
                msg_id = msg_
                msg = await Message.get_from_url(msg_id, client=self.client._http)
                await msg.delete()
        with open(BUG_REPORTS_DIR, "w") as file:
            file.close()

        await ctx.send('Deleted bugs!', ephemeral=True)

def setup(client):
    Ext(client)
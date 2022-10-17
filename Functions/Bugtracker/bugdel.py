from interactions import *
from settings import *
from bugreport import *

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="bugdel",
        description="Use this command to delete a bug",
        default_member_permissions=Permissions.ADMINISTRATOR,
        options=[Option(name="id", description="The ID of the bug report", type=OptionType.STRING, required=True)]
    )

    async def _bugdel(self, ctx: CommandContext, id):
        id = id.zfill(3)
        msg_id = 0
        lines = []

        found = False
        with open(BUG_REPORTS_DIR, "r") as file:
            for line in file:
                if ' ' + id + ' ' in line:
                    msg_, id, st = line.split(' ')
                    msg_id = msg_
                    found = True
                else:
                    lines.append(line)

        if not found:
            await ctx.send('Couldn\'t find bug with given ID!', ephemeral=True)
            return
        with open(BUG_REPORTS_DIR, "w") as file:
            file.writelines(lines)

        msg = await Message.get_from_url(msg_id, client=self.client._http)
        await msg.delete()
        await ctx.send('Deleted bug!', ephemeral=True)

def setup(client):
    Ext(client)
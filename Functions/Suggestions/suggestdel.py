from interactions import *
from settings import *
from suggestion import *

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="suggestdel",
        description="Use this command to delete a suggestion",
        default_member_permissions=Permissions.ADMINISTRATOR,
        options=[Option(name="id", description="The ID of the suggestion", type=OptionType.STRING, required=True)]
    )

    async def _suggestdel(self, ctx: CommandContext, id):
        id = id.zfill(3)
        msg_id = 0
        lines = []

        found = False
        with open(SUGGESTIONS_DIR, "r") as file:
            for line in file:
                if ' ' + id + ' ' in line:
                    msg_, id = line.split(' ')
                    msg_id = msg_
                    found = True
                else:
                    lines.append(line)

        if not found:
            await ctx.send('Couldn\'t find suggestion with given ID!', ephemeral=True)
            return
        with open(SUGGESTIONS_DIR, "w") as file:
            file.writelines(lines)

        msg = await Message.get_from_url(msg_id, client=self.client._http)
        await msg.delete()
        await ctx.send('Deleted suggestion!', ephemeral=True)

def setup(client):
    Ext(client)
from resources.bloxlink import instance as bloxlink
import resources.binds as binds
import resources.users as users
from resources.models import CommandContext
from resources.exceptions import UserNotVerified, Message
import hikari



@bloxlink.command(
    category="Account",
    defer=True,
    options=[
        hikari.commands.CommandOption(
            type=hikari.commands.OptionType.USER,
            name="user",
            description="update this user",
            is_required=True
        )
    ],
    permissions=hikari.Permissions.MANAGE_GUILD |
                hikari.Permissions.MANAGE_ROLES

)
class UpdateCommand:
    """update the roles and nickname of a specific user"""

    async def __main__(self, ctx: CommandContext):
        target_user = list(ctx.resolved.users.values())[0] if ctx.resolved else ctx.member

        roblox_account = None

        try:
            roblox_account = await users.get_user_account(target_user, raise_errors=False)
        except UserNotVerified:
            pass

        message_response = await binds.apply_binds(ctx.member, ctx.guild_id, roblox_account, moderate_user=True)

        await ctx.response.send(embed=message_response)
from resources.bloxlink import instance as bloxlink
import resources.users as users
from resources.models import CommandContext
from resources.exceptions import UserNotVerified, Message
from hikari.commands import CommandOption, OptionType



@bloxlink.command(
    category="Account",
    defer=True,
    options=[
        CommandOption(
            type=OptionType.USER,
            name="user",
            description="Retrieve the Roblox information of a specific user",
            is_required=False
        )
    ]

)
class WhoisCommand:
    """retrieve the Roblox information of a user"""

    async def __main__(self, ctx: CommandContext):
        target_user = list(ctx.resolved.users.values())[0] if ctx.resolved else ctx.member

        try:
            roblox_account = await users.get_user_account(target_user)
        except UserNotVerified:
            if target_user == ctx.member:
                raise UserNotVerified("You are not verified with Bloxlink!")
            else:
                raise UserNotVerified("This user is not verified with Bloxlink!")

        info_embed = await users.format_embed(roblox_account, target_user)

        await ctx.response.send(embed=info_embed)
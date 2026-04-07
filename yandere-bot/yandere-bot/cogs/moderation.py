import discord
from discord.ext import commands
from discord import app_commands
import random
import datetime
import data

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Issue a warning. Sweetly. 🌸")
    @app_commands.describe(user="Who to warn", reason="Why")
    @app_commands.default_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason given."):
        profile = data.get_user(user.id)
        warnings = profile["warnings"]
        warnings.append(reason)
        data.set_user(user.id, warnings=warnings)
        count = len(warnings)

        if count >= 3:
            desc = f"*{interaction.user.mention} places a gentle — then firm — hand on {user.mention}'s shoulder.*\n\n🔪 *\"This is your {count}{'st' if count==1 else 'nd' if count==2 else 'rd' if count==3 else 'th'} warning. I'm not angry. I'm just... noting things. 💕\"*\n\n**Reason:** {reason}"
        else:
            desc = f"*{interaction.user.mention} places a gentle hand on {user.mention}'s shoulder.*\n\n🌸 *\"Please be more careful. For everyone's sake. 💕\"*\n\n**Reason:** {reason}"

        embed = discord.Embed(
            title="⚠️ WARNING ISSUED",
            description=desc,
            color=RED if count >= 3 else PINK
        )
        embed.add_field(name="Total Warnings", value=str(count), inline=True)
        embed.set_footer(text="A warning is a kindness. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kick", description="Remove someone. For their own good. 🔪")
    @app_commands.describe(user="Who to kick", reason="Why")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason given."):
        try:
            await user.kick(reason=reason)
            embed = discord.Embed(
                title="👢 REMOVED",
                description=f"*{user.mention} has been asked to leave.*\n\n🌸 *\"This is for the best. You understand. 💕\"*\n\n**Reason:** {reason}",
                color=RED
            )
        except discord.Forbidden:
            embed = discord.Embed(description="🌸 *I don't have the power to remove them. Yet.*", color=PINK)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ban", description="Eliminate someone permanently. 🔪")
    @app_commands.describe(user="Who to ban", reason="Why")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason given."):
        try:
            await user.ban(reason=reason)
            embed = discord.Embed(
                title="🔪 PERMANENTLY REMOVED",
                description=f"*{user.mention} is gone.*\n\n🖤 *\"Goodbye. I won't miss you. 💕\"*\n\n**Reason:** {reason}",
                color=BLACK
            )
        except discord.Forbidden:
            embed = discord.Embed(description="🌸 *They're beyond my reach. For now.*", color=PINK)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="purge", description="Make the evidence disappear. 🌸")
    @app_commands.describe(amount="How many messages to delete (max 100)")
    @app_commands.default_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        amount = min(100, max(1, amount))
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        embed = discord.Embed(
            description=f"🌸 *{len(deleted)} messages erased.*\n\n*Clean. Like it never happened. 💕*",
            color=PINK
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="mute", description="Silence someone. 🤫")
    @app_commands.describe(user="Who to mute")
    @app_commands.default_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, user: discord.Member):
        try:
            await user.timeout(datetime.timedelta(minutes=10), reason="Muted by yandere bot")
            embed = discord.Embed(
                description=f"🤫 *{user.mention} has been silenced.*\n\n🌸 *\"Shh. It's better this way. 💕\"*",
                color=PINK
            )
        except discord.Forbidden:
            embed = discord.Embed(description="🌸 *I can't silence them. Unfortunately.*", color=PINK)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unmute", description="Allow them to speak again. 🌸")
    @app_commands.describe(user="Who to unmute")
    @app_commands.default_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, user: discord.Member):
        try:
            await user.timeout(None)
            embed = discord.Embed(
                description=f"🌸 *{user.mention} may speak again.*\n\n*\"Don't make me regret this. 💕\"*",
                color=PINK
            )
        except discord.Forbidden:
            embed = discord.Embed(description="🌸 *I can't reach them.*", color=PINK)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))

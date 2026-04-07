import discord
from discord.ext import commands
from discord import app_commands
import random
import data

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d

COOLDOWN_MSG = "🌸 *Patience... wait {:.0f}s. 💕*"


class Rival(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(COOLDOWN_MSG.format(error.retry_after), ephemeral=True)

    @app_commands.command(name="rival", description="Add someone to your rival list. 🔪")
    @app_commands.describe(user="Your new rival")
    @app_commands.checks.cooldown(1, 10.0)
    async def rival(self, interaction: discord.Interaction, user: discord.Member):
        if user.id == interaction.user.id:
            await interaction.response.send_message("🌸 *You can't rival yourself.*", ephemeral=True)
            return
        uid = interaction.user.id
        profile = data.get_user(uid)
        rivals = profile["rivals"]
        uid_str = str(user.id)
        obsession = data.get_obsession(uid)

        if uid_str in rivals:
            embed = discord.Embed(
                description=f"👁️ *{user.mention} is already on your list.*\n*I haven't forgotten about them. I never forget. 🔪*",
                color=RED
            )
        else:
            rivals.append(uid_str)
            new_sanity = max(0, profile["sanity"] - 10)
            data.set_user(uid, rivals=rivals, sanity=new_sanity)
            count = len(rivals)
            if obsession >= 70:
                desc = f"*{user.mention} has been added to the list.* 🔪\n*#{count}. The list is getting long. I don't mind.*"
            elif count == 1:
                desc = f"*{interaction.user.mention} writes {user.mention}'s name down very carefully.* 🔪\n*First on the list. How memorable.*"
            else:
                desc = f"*{user.mention}... noted.* 👁️\n*Rival #{count}. I'm keeping track of all of you. 🌸*"
            embed = discord.Embed(
                title="🔪 RIVAL IDENTIFIED",
                description=desc,
                color=RED if obsession >= 70 else PINK
            )
            embed.set_footer(text=f"Total rivals: {count} 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unrival", description="Remove someone from your rival list. 🌸")
    @app_commands.describe(user="Who to forgive. For now.")
    async def unrival(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        profile = data.get_user(uid)
        rivals = profile["rivals"]
        uid_str = str(user.id)
        if uid_str in rivals:
            rivals.remove(uid_str)
            data.set_user(uid, rivals=rivals)
            embed = discord.Embed(
                description=f"🌸 *{user.mention} has been removed from the list.*\n\n*You're lucky. Most people don't get second chances. 💕*",
                color=PINK
            )
        else:
            embed = discord.Embed(
                description=f"🌸 *{user.mention} wasn't on your list to begin with.*",
                color=PINK
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="eliminate", description="\"Eliminate\" a rival. Hypothetically. 🔪")
    @app_commands.describe(user="The rival to eliminate")
    async def eliminate(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        profile = data.get_user(uid)
        rivals = profile["rivals"]
        uid_str = str(user.id)
        was_rival = uid_str in rivals
        if was_rival:
            rivals.remove(uid_str)
            data.set_user(uid, rivals=rivals)

        obsession = data.get_obsession(uid)
        if obsession >= 80:
            methods = [
                f"*{user.mention} is no longer a concern.* 🔪\n*The details have been omitted. For everyone's benefit.*",
                f"*{interaction.user.mention} smiles.* 🌸\n*\"{user.mention}? Oh, they're... unavailable. Indefinitely. 💕\"*",
            ]
        else:
            methods = [
                f"*{user.mention} has been... taken care of.* 🔪\n*No evidence. No witnesses. Just results. 🌸*",
                f"*{interaction.user.mention} smiles sweetly at {user.mention}.*\n*\"Have a nice day. Forever. 💕\"*",
            ]

        embed = discord.Embed(
            title="🔪 RIVAL ELIMINATED",
            description=random.choice(methods),
            color=BLACK
        )
        remaining = len(data.get_user(uid)["rivals"])
        embed.set_footer(text=f"Rivals remaining: {remaining} 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="protect", description="Protect someone from all rivals. 💕")
    @app_commands.describe(user="Who to protect")
    async def protect(self, interaction: discord.Interaction, user: discord.Member):
        obsession = data.get_obsession(interaction.user.id)
        if obsession >= 70:
            desc = f"*{interaction.user.mention} steps directly between {user.mention} and everyone else.* 🔪\n*\"Touch them and I will not be responsible for what happens. 💕\"*"
        else:
            desc = f"🌸 *{interaction.user.mention} stands between {user.mention} and the world.*\n*\"No one gets near them. I made sure. 💕\"*"
        embed = discord.Embed(title="💕 PROTECTION ACTIVATED", description=desc, color=PINK)
        embed.set_footer(text="Always watching. Always protecting. 👁️")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="target", description="Mark someone as a target. 👁️")
    @app_commands.describe(user="Who to mark")
    async def target(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        profile = data.get_user(uid)
        targets = profile["targets"]
        uid_str = str(user.id)
        if uid_str not in targets:
            targets.append(uid_str)
            data.set_user(uid, targets=targets)
        embed = discord.Embed(
            title="👁️ TARGET MARKED",
            description=f"*{user.mention} has been marked.*\n\n*I'll keep a close eye on them. I'm very good at that. 🌸*",
            color=RED
        )
        embed.set_footer(text=f"Active targets: {len(targets)} 🔪")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clearlist", description="Clear all rivals and targets. 🌸")
    async def clearlist(self, interaction: discord.Interaction):
        uid = interaction.user.id
        profile = data.get_user(uid)
        count_r = len(profile["rivals"])
        count_t = len(profile["targets"])
        data.set_user(uid, rivals=[], targets=[])
        embed = discord.Embed(
            title="🌸 LIST CLEARED",
            description=f"*{count_r} rivals and {count_t} targets removed.*\n\n*A clean slate. How optimistic. How naive. 💕*",
            color=PINK
        )
        embed.set_footer(text="The list always fills up again. 🔪")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Rival(bot))

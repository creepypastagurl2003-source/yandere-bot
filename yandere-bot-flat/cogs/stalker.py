import discord
from discord.ext import commands
from discord import app_commands
import random
import data

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d

FAKE_LOCATIONS_SWEET = [
    "🌸 They're at the café on the corner. Third table from the left. They ordered their usual.",
    "💕 At school, near the library. They're alone right now.",
    "🌸 Home. Safe. I made sure.",
    "👁️ Currently in their room. Lights still on. Music playing softly.",
]
FAKE_LOCATIONS_POSSESSIVE = [
    "👁️ They stopped somewhere unexpected. I adjusted the route accordingly.",
    "🌸 Walking home. They took the long route today. I followed the whole way.",
    "💕 They met someone new today. I took note. I always take note.",
    "👁️ Still in the building. I'm waiting outside. It's fine. I'm comfortable here.",
]
FAKE_LOCATIONS_UNHINGED = [
    "🩸 I know exactly where they are. I'm not saying. Not yet.",
    "🔪 Location classified. I'm handling something. Don't ask.",
    "🩸 Closer than you think. Always closer than you think.",
    "👁️ They tried a different route today. It didn't work. 🌸",
]

LAST_SEEN_TIMES = [
    "3 minutes ago 👁️",
    "17 minutes ago 🌸",
    "an hour ago 💕",
    "this morning, near their usual spot 🌸",
    "last night. They looked tired. I noticed. 👁️",
    "moments before you asked. Almost like I knew you'd ask. 🌸",
]

SHADOW_SWEET = [
    "*Did you hear footsteps behind you?*\n\n*Don't worry. It's just me. 🌸*",
    "*{user} just felt a presence.*\n*Warm. Close. Familiar.*\n*\"I'm right here. I'm always right here. 💕\"*",
]
SHADOW_POSSESSIVE = [
    "*The shadow behind {user} doesn't move when the wind does.*\n\n*But it's watching. 👁️*",
    "*{user} turns around. Nobody there.*\n*But the feeling doesn't leave. Someone is close. Very close. 🌸*",
]
SHADOW_UNHINGED = [
    "*{user} hears breathing.*\n\n🩸 *Too close. Far too close. And it doesn't stop.*",
    "*The figure behind {user} doesn't hide anymore.*\n🔪 *\"I wanted you to know I'm here. You should know I'm always here.\"*",
    "*{user}'s shadow has company.*\n🩸 *It's been there for a while. It's not going anywhere.*",
]


def _levelup_field(embed: discord.Embed, lu: dict) -> None:
    if lu:
        embed.add_field(
            name=f"🆙 LEVEL {lu['new_level']} REACHED",
            value=f"*{data.levelup_text(lu['new_level'])}*\n`XP: {lu['new_xp']}/100`",
            inline=False
        )


class Stalker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stalk", description="Begin stalking someone. 🌸")
    @app_commands.describe(user="Who to stalk")
    @app_commands.checks.cooldown(1, 15.0)
    async def stalk(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        tone = data.sanity_tone(uid)
        detail = f"Joined: {user.joined_at.strftime('%b %d %Y') if user.joined_at else 'Unknown'} | Roles: {len(user.roles)-1}"

        if tone == "unhinged":
            desc = f"*{interaction.user.mention} has begun a detailed observation of {user.mention}.*\n\n📋 `{detail}`\n\n🩸 *This isn't new. I've been watching for a while. I'm just being honest about it now.*"
            color = RED
        elif tone == "possessive":
            desc = f"*{interaction.user.mention} opens a new file for {user.mention}.*\n\n📋 `{detail}`\n\n👁️ *I'll fill this in over time. I'm patient. 💕*"
            color = PINK
        else:
            desc = f"*{interaction.user.mention} has begun observing {user.mention}.*\n\n📋 `{detail}`\n\n🌸 *I'll know everything soon. I already know quite a bit.*"
            color = PINK

        lu = data.gain_xp(uid, 20)
        embed = discord.Embed(title=f"👁️ Stalking {user.display_name}", description=desc, color=color)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="Observation initiated. 💕")
        _levelup_field(embed, lu)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="location", description="Get a 'tracking update' on someone. 📍")
    @app_commands.describe(user="Who to locate")
    async def location(self, interaction: discord.Interaction, user: discord.Member):
        tone = data.sanity_tone(interaction.user.id)
        if tone == "unhinged":
            loc = random.choice(FAKE_LOCATIONS_UNHINGED)
        elif tone == "possessive":
            loc = random.choice(FAKE_LOCATIONS_POSSESSIVE)
        else:
            loc = random.choice(FAKE_LOCATIONS_SWEET)

        embed = discord.Embed(
            title=f"📍 Location Report — {user.display_name}",
            description=f"*Update requested by {interaction.user.mention}*\n\n{loc}",
            color=RED if tone == "unhinged" else PINK
        )
        embed.set_footer(text="This information is strictly for their safety. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="lastseen", description="When was someone last seen? 👁️")
    @app_commands.describe(user="Who to check")
    async def lastseen(self, interaction: discord.Interaction, user: discord.Member):
        tone = data.sanity_tone(interaction.user.id)
        suffix = (
            "\n\n🩸 *I never stop tracking. Ever.*"
            if tone == "unhinged" else
            "\n\n🌸 *I keep track. It helps me make sure they're okay.*"
        )
        embed = discord.Embed(
            title=f"🕐 Last Seen — {user.display_name}",
            description=f"*{user.mention} was last seen {random.choice(LAST_SEEN_TIMES)}*{suffix}",
            color=RED if tone == "unhinged" else PINK
        )
        embed.set_footer(text="I always keep track. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shadow", description="Make your presence known. Barely. 👁️")
    @app_commands.describe(user="Who you're shadowing")
    async def shadow(self, interaction: discord.Interaction, user: discord.Member):
        tone = data.sanity_tone(interaction.user.id)
        if tone == "unhinged":
            pool = SHADOW_UNHINGED
            color = BLACK
        elif tone == "possessive":
            pool = SHADOW_POSSESSIVE
            color = BLACK
        else:
            pool = SHADOW_SWEET
            color = PINK
        msg = random.choice(pool).replace("{user}", user.mention)
        embed = discord.Embed(title="👁️ SHADOW MODE", description=msg, color=color)
        embed.set_footer(text="Right behind you. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="presence", description="Reveal who you're currently watching. 👁️")
    async def presence(self, interaction: discord.Interaction):
        online = [m for m in interaction.guild.members if m.status != discord.Status.offline and not m.bot]
        tone = data.sanity_tone(interaction.user.id)
        if online:
            subject = random.choice(online)
            if tone == "unhinged":
                desc = f"*Currently watching: {subject.mention}*\n\n🩸 *They've been in my sights for a while now. They don't know. 🔪*"
            else:
                desc = f"*Currently watching: {subject.mention}*\n\n🌸 *They don't know. They never do. 💕*"
        else:
            desc = "*The server is quiet right now.*\n\n👁️ *But I'll be here when they return. Always.*"
        embed = discord.Embed(
            title="👁️ CURRENT PRESENCE",
            description=desc,
            color=RED if tone == "unhinged" else PINK
        )
        embed.set_footer(text="Watching. Always watching. 💕")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Stalker(bot))

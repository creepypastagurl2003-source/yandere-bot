import discord
from discord.ext import commands
from discord import app_commands
import random

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d

EVENTS = [
    ("🌸 THE ENCOUNTER", "You lock eyes with them across the room.\n\nTime slows. They look away first.\nYou don't.\n\n*This is the beginning of something. 💕*"),
    ("🔪 THE RIVAL APPEARS", "A new student arrives. Confident. Friendly.\n\nThey walk straight toward your person.\n\n*No. No no no. Not happening. Not today. 🌸*"),
    ("💕 THE NOTE", "You find a note in your locker.\n\nIt's from them. It says: *\"Thank you for always being there.\"*\n\n*They noticed. They noticed. They always noticed. 🌸*"),
    ("👁️ THE OBSERVATION", "You've been watching them for 3 hours.\n\nThey glance in your direction.\n\n*Do they know? They can't know. But maybe they should. 🌸*"),
    ("🩸 THE SLIP", "You said too much. You revealed too much.\n\nThey're quiet now.\n\n*It's okay. I can fix this. I can always fix this. 🔪*"),
    ("🌸 THE PERFECT DAY", "They walked with you. They laughed at your joke.\n\nFor one hour, everything was exactly right.\n\n*I'm going to hold onto this forever. 💕*"),
    ("🖤 THE DISTANCE", "They've been distant.\n\nTwo days without a real conversation.\n\n*Something is wrong. Someone did something. I'll find out. 🔪*"),
]

RUMORS = [
    "I heard they collect something unusual. What? Oh. You don't want to know. 🌸",
    "Did you know they reread certain conversations 40+ times? No reason. Just thought you should know. 💕",
    "Apparently they have a list. Of people. I won't say more. 🔪",
    "Word is they baked something last week and watched from a distance to see the reaction. Sweet. 🌸",
    "I heard they've memorized exactly what {user} orders at the café. Isn't that thoughtful? 💕",
]

SECRETS = [
    "*I have a collection. It's organized by date. You'd be surprised how many items I have. 🌸*",
    "*I practice conversations the night before. Every response. Every pause. 💕*",
    "*I've written 87 letters that I'll never send. But I kept them all. 📓*",
    "*I know exactly how many steps it takes to reach your classroom from mine. 👁️*",
    "*I've imagined every possible outcome. I've prepared for all of them. 🔪*",
    "*My diary has its own section just for you. It's the longest one. 🌸*",
]

ENDINGS = [
    "🌸 **TRUE ENDING** — You chose them. They chose you. The world shrank to just the two of you.\n\n*Everyone else was irrelevant anyway. 💕*",
    "🔪 **YANDERE ENDING** — They tried to leave. They couldn't.\n\n*You can't leave something that's already become part of you. 🌸*",
    "🖤 **DESPAIR ENDING** — They never knew. You watched from a distance until the very end.\n\n*At least they were happy. That's enough. That has to be enough.*",
    "💕 **DEVOTED ENDING** — You protected them from everything. Everyone.\n\n*There was nothing left but the two of you. Exactly how it should be. 🌸*",
    "👁️ **UNKNOWN ENDING** — ███████████.\n\n*The record has been altered. You were never here. 🌸*",
]


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="event", description="Trigger a random yandere scenario. 🎭")
    async def event(self, interaction: discord.Interaction):
        title, desc = random.choice(EVENTS)
        embed = discord.Embed(title=title, description=desc, color=random.choice([PINK, RED, BLACK]))
        embed.set_footer(text="Every moment is a scene in our story. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rumor", description="Spread a fake rumor about someone. 🌸")
    @app_commands.describe(user="Who the rumor is about")
    async def rumor(self, interaction: discord.Interaction, user: discord.Member):
        rumor = random.choice(RUMORS).replace("{user}", user.mention)
        embed = discord.Embed(
            title=f"🗣️ A Little Rumor About {user.display_name}",
            description=f"*{interaction.user.mention} leans in and whispers...*\n\n🌸 *\"{rumor}\"*",
            color=PINK
        )
        embed.set_footer(text="Don't tell anyone I said this. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="secret", description="Reveal one of your hidden secrets. 🤫")
    async def secret(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤫 A SECRET",
            description=f"*{interaction.user.mention} glances around, then leans forward.*\n\n{random.choice(SECRETS)}",
            color=BLACK
        )
        embed.set_footer(text="You're the only one I'd tell. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ending", description="Get a random story ending. 🎴")
    async def ending(self, interaction: discord.Interaction):
        ending = random.choice(ENDINGS)
        embed = discord.Embed(
            title="🎴 YOUR ENDING",
            description=ending,
            color=random.choice([PINK, RED, BLACK])
        )
        embed.set_footer(text="Every story ends. Some more permanently than others. 🌸")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Events(bot))

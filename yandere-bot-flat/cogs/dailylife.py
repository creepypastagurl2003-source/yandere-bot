import discord
from discord.ext import commands
from discord import app_commands
import random
import data

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d

MOODS = [
    ("🌸 Lovesick", "Thoughts of them keep interrupting everything. I can't concentrate. It's fine. I'm fine."),
    ("💕 Devoted", "Today was perfect. I watched them laugh from across the room. Perfect."),
    ("🔪 Jealous", "They talked to someone else today. I counted the seconds. 47."),
    ("👁️ Fixated", "I reorganized my collection. Everything labeled. Everything perfect."),
    ("🖤 Melancholy", "They didn't look at me today. I'll try harder tomorrow."),
    ("🩸 Unstable", "I'm fine. I said I'm fine. Please don't ask again."),
    ("🌸 Elated", "They said my name today. Just my name. I've been smiling since."),
]

DIARY_ENTRIES = [
    "*Dear diary,\n\nToday they walked past me in the hallway. Our shoulders almost touched. Almost.\nI've been thinking about it ever since.\nI think they're starting to notice me.\nThey will. Eventually. 🌸*",
    "*Dear diary,\n\nI made a list of everyone they spoke to today.\n12 people. I've assessed all of them.\nOnly 2 are concerning. I'm handling it.\nEverything is under control. 💕*",
    "*Dear diary,\n\nThey smiled at me.\nI've replayed it 83 times.\nI think it means something.\nIt means something. 👁️*",
    "*Dear diary,\n\nI trimmed a photo of them today. Just a small one. For my collection.\nThis is normal. People do this.\nI'm perfectly normal. 🌸*",
]

SCHEDULES = [
    "```\n📅 Today's Schedule\n\n7:00 AM  — Watch them arrive\n8:30 AM  — Sit nearby in class\n12:00 PM — Observe lunch (strategic seat)\n3:45 PM  — Follow home route (for safety)\n6:00 PM  — Update the diary\n9:00 PM  — Review the collection\n11:00 PM — Think about them until sleep\n```",
    "```\n📅 Today's Agenda\n\n7:00 AM  — Arrive early. Wait.\n8:00 AM  — Watch from usual spot\n10:30 AM — Assess any rivals\n12:15 PM — Leave gift in locker\n3:30 PM  — Follow at safe distance\n8:00 PM  — Write about today\n```",
]


class DailyLife(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="goodmorning", description="Start the day with devotion. 🌸")
    async def goodmorning(self, interaction: discord.Interaction):
        messages = [
            f"🌸 Good morning, {interaction.user.mention}.\n\n*I watched the sunrise and thought of you. I think of you first. Always.*",
            f"☀️ {interaction.user.mention}! You're awake!\n\n*I've been waiting. I made breakfast. I wasn't sure if you'd notice. Please notice. 💕*",
            f"🌸 Good morning.\n\n*Another day. Another chance. I'll make today count. 💕*",
        ]
        embed = discord.Embed(description=random.choice(messages), color=PINK)
        embed.set_footer(text="Today will be a good day. I'll make sure of it. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="goodnight", description="End the day with longing. 🖤")
    async def goodnight(self, interaction: discord.Interaction):
        uid = interaction.user.id
        profile = data.get_user(uid)
        new_sanity = min(100, profile["sanity"] + 5)
        data.set_user(uid, sanity=new_sanity)
        messages = [
            f"🌙 Goodnight, {interaction.user.mention}.\n\n*Sleep well. I'll be here when you wake up.\nI'm always here. 💕*",
            f"🖤 Goodnight.\n\n*Dream of me. Or don't. Either way, I'll be thinking of you. 🌸*",
            f"*{interaction.user.mention} should sleep now.*\n\n*I'll watch the notifications. Just in case. 👁️*",
        ]
        embed = discord.Embed(description=random.choice(messages), color=BLACK)
        embed.add_field(name="🌸 Sanity", value=f"`{profile['sanity']}` → `{new_sanity}` (+5)", inline=True)
        embed.set_footer(text="Sweet dreams. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mood", description="Check the current emotional status. 🌸")
    async def mood(self, interaction: discord.Interaction):
        mood_name, desc = random.choice(MOODS)
        embed = discord.Embed(
            title=f"Current Mood: {mood_name}",
            description=f"*{desc}*",
            color=PINK
        )
        embed.set_footer(text=f"Reported by {interaction.user.display_name} 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="diary", description="Read a diary entry. 📓")
    async def diary(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📓 Diary Entry",
            description=random.choice(DIARY_ENTRIES),
            color=PINK
        )
        embed.set_footer(text="This is private. But I'll share it with you. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="schedule", description="Review today's observational schedule. 📅")
    async def schedule(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📅 Daily Schedule",
            description=random.choice(SCHEDULES),
            color=PINK
        )
        embed.set_footer(text="Efficiency is devotion. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="lunch", description="Invite someone to lunch. With ulterior motives. 🍱")
    @app_commands.describe(user="Who to invite")
    async def lunch(self, interaction: discord.Interaction, user: discord.Member):
        invites = [
            f"🍱 *{interaction.user.mention} appears beside {user.mention} with a perfectly prepared bento box.*\n*\"I made extra. Sit with me? 🌸\"*",
            f"*{interaction.user.mention} saves a seat for {user.mention} every single day.*\n*Today they finally asked. 💕*",
            f"🍱 *\"I made this for you specifically. I researched your favorite foods. That's not weird. 🌸\"*",
        ]
        embed = discord.Embed(description=random.choice(invites), color=PINK)
        embed.set_footer(text="I made it from scratch. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="walkhome", description="Walk someone home. For protection. 🌸")
    @app_commands.describe(user="Who to walk home")
    async def walkhome(self, interaction: discord.Interaction, user: discord.Member):
        walks = [
            f"🌸 *{interaction.user.mention} falls into step beside {user.mention}.*\n*\"I'm going this way too. Coincidence. 💕\"*",
            f"*{interaction.user.mention} waits by the exit.*\n*\"Oh! You're heading home? Me too. Always. 🌸\"*",
            f"*{interaction.user.mention} walks {user.mention} home in comfortable silence.*\n*It isn't coincidence. It never is. 💕*",
        ]
        embed = discord.Embed(description=random.choice(walks), color=PINK)
        embed.set_footer(text="Safe. They're safe. I made sure. 👁️")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(DailyLife(bot))

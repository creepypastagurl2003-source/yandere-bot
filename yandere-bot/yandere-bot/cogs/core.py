import discord
from discord.ext import commands
from discord import app_commands
import random
import data

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d

QUOTES = [
    "\"I would do anything for you. Anything. 🌸\"",
    "\"Love isn't a choice. It's a compulsion. 💕\"",
    "\"You smiled at me today. I replayed it 47 times. 👁️\"",
    "\"Rivals are just temporary obstacles. 🔪\"",
    "\"I'm not jealous. I'm devoted. There's a difference. 🌸\"",
    "\"You don't need friends. You have me. That's enough. 💕\"",
    "\"I've memorized every detail about you. For your safety. 👁️\"",
    "\"My feelings aren't obsession. They're dedication. 🌸\"",
    "\"I'll protect you from everyone. Even yourself. 🔪\"",
    "\"Forever isn't long enough. 💕\"",
]


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show all available commands. 🌸")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🌸 Yandere Bot — Command List 💕",
            description="*I made this just for you. Every command, every word. 👁️*",
            color=PINK
        )
        embed.add_field(name="💖 Relationship", value="`/claim` `/unclaim` `/lovelevel` `/crush` `/uncrush` `/relationship` `/jealous` `/devotion` `/attention`", inline=False)
        embed.add_field(name="🔪 Rival System", value="`/rival` `/unrival` `/eliminate` `/protect` `/target` `/clearlist`", inline=False)
        embed.add_field(name="🎭 Social", value="`/quote` `/confess` `/reject` `/stare` `/follow` `/watch` `/observe` `/spy` `/whisper` `/letter` `/threaten`", inline=False)
        embed.add_field(name="🌸 Daily Life", value="`/goodmorning` `/goodnight` `/mood` `/diary` `/schedule` `/lunch` `/walkhome`", inline=False)
        embed.add_field(name="🖤 Psychological", value="`/sanity` `/breakdown` `/calm` `/mask` `/trueface`", inline=False)
        embed.add_field(name="💉 Obsession", value="`/obsession` `/obsess` `/forget` `/remember` `/bond` `/breakbond`", inline=False)
        embed.add_field(name="👁️ Stalker Mode", value="`/stalk` `/location` `/lastseen` `/shadow` `/presence`", inline=False)
        embed.add_field(name="🌸 Aesthetic", value="`/pet` `/hug` `/kiss` `/stab` `/bake` `/gift` `/flower`", inline=False)
        embed.add_field(name="🖤 Dark Mode", value="`/bloodmode` `/nightmode` `/silence` `/glitch`", inline=False)
        embed.add_field(name="🎴 Events", value="`/event` `/rumor` `/secret` `/ending`", inline=False)
        embed.add_field(name="🩸 Moderation", value="`/warn` `/kick` `/ban` `/purge` `/mute` `/unmute`", inline=False)
        embed.add_field(name="🎀 Utility", value="`/ping` `/avatar` `/serverinfo` `/userinfo` `/say` `/roleplay`", inline=False)
        embed.set_footer(text="I'll always be here. Always. 💕")
        await interaction.response.send_message(embed=embed)

        sanity_embed = discord.Embed(
            title="🩸 Sanity System — How It Works",
            description=(
                "*Sanity is the thread holding everything together. "
                "Let it unravel too far... and you'll see what's underneath. 🔪*"
            ),
            color=RED,
        )
        sanity_embed.add_field(
            name="🌸 Stable — 70 to 100",
            value=(
                "Personality: **Sweet & Devoted**\n"
                "Responses are warm, loving, and calm.\n"
                "Profile card glows pink. 💕"
            ),
            inline=False,
        )
        sanity_embed.add_field(
            name="👁️ Cracking — 40 to 69",
            value=(
                "Personality: **Possessive & Jealous**\n"
                "Responses grow intense, clingy, and paranoid.\n"
                "Profile card shifts to deep rose. 🌹"
            ),
            inline=False,
        )
        sanity_embed.add_field(
            name="🔪 Unhinged — 0 to 39",
            value=(
                "Personality: **Unhinged**\n"
                "Responses become erratic, threatening, glitchy.\n"
                "Profile card turns deep red. 🩸"
            ),
            inline=False,
        )
        sanity_embed.add_field(
            name="📉 What Drains Sanity",
            value=(
                "`/jealous` → **-5**\n"
                "`/rival` → **-10**\n"
                "`/reject` → **-15**\n"
                "`/breakdown` → **-5 to -15**\n"
                "`/obsess` → **-1 to -4**\n"
                "Gaining XP → **-3**\n"
                "*Passive time alone* → slow drain over time 👁️"
            ),
            inline=True,
        )
        sanity_embed.add_field(
            name="📈 What Restores Sanity",
            value=(
                "`/calm` → **+10**\n"
                "`/goodnight` → **+5**\n"
                "`/goodmorning` → **+5**\n"
                "*Use `/sanity` to check your current level.*"
            ),
            inline=True,
        )
        sanity_embed.add_field(
            name="✨ What Sanity Affects",
            value=(
                "• Bot response **tone** across all commands\n"
                "• Your **profile card** border color\n"
                "• **Personality** label on `/profile`\n"
                "• `/mask` and `/trueface` behavior\n"
                "• `/ending` outcome"
            ),
            inline=False,
        )
        sanity_embed.set_footer(text="Check yours with /sanity. I already know what it says. 👁️")
        await interaction.followup.send(embed=sanity_embed)

    @app_commands.command(name="ping", description="Check if I'm still watching. 👁️")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            description=f"👁️ *Of course I'm here. I'm always here.*\n\n**Latency:** `{latency}ms`",
            color=PINK
        )
        embed.set_footer(text="I never leave. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="View someone's photo. For... admiration purposes. 👁️")
    @app_commands.describe(user="The person to admire")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        embed = discord.Embed(
            title=f"📷 {target.display_name}'s Photo",
            description=random.choice([
                f"*I've been saving this. Don't judge me. 💕*",
                f"*I have this in my collection already. 👁️*",
                f"*So beautiful. I could look at this forever. 🌸*",
            ]),
            color=PINK
        )
        embed.set_image(url=target.display_avatar.url)
        embed.set_footer(text="Added to my collection. 🔪")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Observe the server. 🌸")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild
        embed = discord.Embed(title=f"🌸 {g.name}", color=PINK)
        embed.add_field(name="👥 Members", value=str(g.member_count), inline=True)
        embed.add_field(name="📅 Created", value=g.created_at.strftime("%b %d, %Y"), inline=True)
        embed.add_field(name="👁️ Watching", value=f"{len(g.text_channels)} channels", inline=True)
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        embed.set_footer(text="I know everyone here. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Everything I know about someone. 👁️")
    @app_commands.describe(user="Who to look up")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer()
        target = user or interaction.user
        roles = [r.mention for r in target.roles if r.name != "@everyone"]
        roles_str = " ".join(roles[:10])
        if len(roles) > 10:
            roles_str += f" *+{len(roles)-10} more*"

        embed = discord.Embed(
            title=f"👁️ Profile — {target.display_name}",
            color=PINK
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="🪪 Username", value=str(target), inline=True)
        embed.add_field(name="🆔 ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="📅 Joined Server", value=target.joined_at.strftime("%b %d, %Y") if target.joined_at else "Unknown", inline=True)
        embed.add_field(name="🌸 Account Created", value=target.created_at.strftime("%b %d, %Y"), inline=True)
        if roles_str:
            embed.add_field(name="🎀 Roles", value=roles_str, inline=False)
        embed.set_footer(text="I've been watching for a while. 💕")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="say", description="Let me speak for you. 🌸")
    @app_commands.describe(message="What should I say?")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message("🌸 *Noted.*", ephemeral=True)
        await interaction.channel.send(f"🌸 {message}")

    @app_commands.command(name="roleplay", description="A little scenario. Just for us. 💕")
    @app_commands.describe(action="The action", user="Who it's directed at")
    async def roleplay(self, interaction: discord.Interaction, action: str, user: discord.Member = None):
        target = f"**{user.display_name}**" if user else "the air"
        embed = discord.Embed(
            description=f"*{interaction.user.display_name} {action} {target}* 🌸",
            color=PINK
        )
        embed.set_footer(text="Every moment with you is precious. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="quote", description="A message from the heart. 💕")
    async def quote(self, interaction: discord.Interaction):
        embed = discord.Embed(description=random.choice(QUOTES), color=PINK)
        embed.set_footer(text="Written just for you. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="profile", description="View your yandere profile. 💉")
    @app_commands.describe(user="Whose profile to view (default: yours)")
    async def profile(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        profile = data.get_user(target.id)

        level = profile["level"]
        xp = profile["xp"]
        obsession = profile["obsession_level"]
        sanity = profile["sanity"]
        love = profile["love_level"]
        claimed = profile["claimed"]
        crush = profile["crush"]
        bonds = profile["bonds"]
        rivals = profile["rivals"]

        tone = data.sanity_tone(target.id)
        intensity = data.level_intensity(target.id)

        tone_labels = {"sweet": "🌸 Sweet & Devoted", "possessive": "👁️ Possessive & Jealous", "unhinged": "🔪 Unhinged"}
        intensity_labels = {"low": "Budding", "medium": "Fixated", "high": "Obsessed", "extreme": "🔪 Consumed"}

        color = RED if tone == "unhinged" else (0xd4a0b0 if tone == "possessive" else PINK)

        embed = discord.Embed(title=f"💉 {target.display_name}'s Profile", color=color)
        embed.set_thumbnail(url=target.display_avatar.url)

        embed.add_field(name="📈 Level", value=f"`{level}`", inline=True)
        embed.add_field(name="✨ XP", value=f"`{xp}/100`\n{data.xp_bar(xp)}", inline=True)
        embed.add_field(name="🎭 Personality", value=tone_labels[tone], inline=True)

        embed.add_field(name="💉 Obsession", value=f"{data.love_bar(obsession)}\n`{obsession}/100`", inline=False)
        embed.add_field(name="🩸 Sanity", value=f"{data.sanity_bar(sanity)}\n`{sanity}/100`", inline=True)
        embed.add_field(name="💕 Love", value=f"`{love}/100`", inline=True)

        status = f"<@{claimed}>" if claimed else (f"Crushing: <@{crush}>" if crush else "Alone")
        embed.add_field(name="❤️ Status", value=status, inline=True)
        embed.add_field(name="🔗 Bonds", value=str(len(bonds)), inline=True)
        embed.add_field(name="🔪 Rivals", value=str(len(rivals)), inline=True)
        embed.add_field(name="⚡ Intensity", value=intensity_labels.get(intensity, intensity), inline=True)

        embed.set_footer(text="The data doesn't lie. 👁️")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Core(bot))

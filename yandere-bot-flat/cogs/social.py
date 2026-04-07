import discord
from discord.ext import commands
from discord import app_commands
import random
import data

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d

COOLDOWN_MSG = "🌸 *Patience... wait {:.0f}s. 💕*"

# Sanity-tiered response pools
CONFESS_SWEET = [
    "{user} stands before {target}, hands clasped.\n*\"I think about you every single day. I've never said it before. I'm saying it now. 💕\"*",
    "{user} passes {target} a folded note.\n*It reads: \"You are the only thing that makes sense. Please don't run. 🌸\"*",
    "{user} takes a quiet breath.\n*\"I've loved you since the moment I saw you. I've been waiting. This is it. 🌸\"*",
]
CONFESS_POSSESSIVE = [
    "{user} steps closer to {target} than is comfortable.\n*\"I need you to know something. I've needed you to know for a long time. You're mine. In my head, you already are. 💕\"*",
    "*{user} has been drafting this confession for weeks.*\n*\"I don't know how to say this gently anymore. I love you. I need you. Don't say no.\"* 🔪",
    "{user} grabs {target}'s wrist — gently.\n*\"Listen. Please just listen. I can't keep pretending I don't feel this. 💕\"*",
]
CONFESS_UNHINGED = [
    "*{user}'s smile is too wide. Their voice is too calm.*\n🩸 *\"You don't understand yet. But you will. I love you more than you can process. You belong with me. That's just the truth.\"*",
    "*{user} laughs softly. It doesn't stop.*\n🔪 *\"I've been thinking about saying this for so long. Too long. So here it is: mine. You're mine. That's my confession. 🌸\"*",
    "*{user} reaches out and cups {target}'s face in their hands.*\n🩸 *\"Look at me. You never look at me enough. I love you. Say it back. Say it back.\"*",
]

FOLLOW_SWEET = [
    "*{user} follows {target} at a respectful distance.* 🌸\n*They don't notice. Most people don't notice until it's too late. 💕*",
    "*{user} happens to be going the same way as {target}.* 🌸\n*Every day. What a coincidence. 💕*",
    "*{user} keeps exactly seven steps behind {target}.*\n*\"For safety. Just in case. 🌸\"*",
]
FOLLOW_POSSESSIVE = [
    "*{user} follows {target} so closely their footsteps sync.* 👁️\n*\"I know all your routes now. I learned them. For you. 💕\"*",
    "*{user} has been following {target} for three blocks.*\n*They haven't noticed. {user} hopes they never notice. Or maybe hopes they do.* 🌸",
    "*{user} rounds the corner a second after {target}.*\n👁️ *\"I just like knowing where you are. That's love. That's what love is.\"*",
]
FOLLOW_UNHINGED = [
    "*{user} is everywhere {target} goes.*\n🩸 *There's no escaping it. There's no escaping {user}. Not anymore.*",
    "*{user} follows {target} home. And waits outside. And comes back tomorrow.*\n🔪 *\"I just want to be near you. Is that so wrong?\"*",
    "*{user}'s footsteps echo behind {target}.*\n🩸 *\"Don't turn around. I'm more comforting when you can't see me. 💕\"*",
]


def _pick(pool: list, user: str, target: str) -> str:
    return random.choice(pool).replace("{user}", user).replace("{target}", target)


def _levelup_field(embed: discord.Embed, lu: dict) -> None:
    if lu:
        embed.add_field(
            name=f"🆙 LEVEL {lu['new_level']} REACHED",
            value=f"*{data.levelup_text(lu['new_level'])}*\n`XP: {lu['new_xp']}/100`",
            inline=False
        )


class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(COOLDOWN_MSG.format(error.retry_after), ephemeral=True)

    @app_commands.command(name="confess", description="Confess your feelings. 🌸")
    @app_commands.describe(user="Who to confess to")
    @app_commands.checks.cooldown(1, 30.0)
    async def confess(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        tone = data.sanity_tone(uid)
        u = interaction.user.mention
        t = user.mention

        if tone == "sweet":
            desc = _pick(CONFESS_SWEET, u, t)
            color = PINK
        elif tone == "possessive":
            desc = _pick(CONFESS_POSSESSIVE, u, t)
            color = PINK
        else:
            desc = _pick(CONFESS_UNHINGED, u, t)
            color = RED

        lu = data.gain_xp(uid, 25)
        embed = discord.Embed(title="💕 CONFESSION", description=desc, color=color)
        embed.set_footer(text="Please say yes. 🔪")
        _levelup_field(embed, lu)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reject", description="Reject someone. How cruel. 🖤")
    @app_commands.describe(user="Who to reject")
    async def reject(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        profile = data.get_user(uid)
        new_sanity = max(0, profile["sanity"] - 15)
        data.set_user(uid, sanity=new_sanity)
        tone = data.sanity_tone(uid)

        if tone == "unhinged":
            responses = [
                f"*{interaction.user.mention} laughs. It doesn't stop.* 🩸\n*\"No? No? You think that matters? You think 'no' fixes anything? 🔪\"*",
                f"*{interaction.user.mention} stares at {user.mention} for a long time.*\n🩸 *\"I'll pretend I didn't hear that.\"*",
            ]
        elif tone == "possessive":
            responses = [
                f"*{interaction.user.mention} looks at {user.mention} very carefully.* 👁️\n*\"Okay. I heard you. I just don't accept it. 💕\"*",
                f"*{interaction.user.mention} turns away.* 🌸\n*\"That's fine. I'll wait. I'm very good at waiting. 🔪\"*",
            ]
        else:
            responses = [
                f"*{interaction.user.mention} looks at {user.mention} with cold eyes.*\n*\"No. Not now. Not ever. 🖤\"*",
                f"*{user.mention} reaches out. {interaction.user.mention} steps back.*\n*\"This isn't a good idea. For either of us. 💔\"*",
            ]

        embed = discord.Embed(description=random.choice(responses), color=BLACK)
        embed.add_field(name="🩸 Sanity", value=f"`{profile['sanity']}` → `{new_sanity}`", inline=True)
        embed.set_footer(text="Rejection is temporary. Devotion is forever. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stare", description="Stare at someone intensely. 👁️")
    @app_commands.describe(user="Who to stare at")
    async def stare(self, interaction: discord.Interaction, user: discord.Member):
        tone = data.sanity_tone(interaction.user.id)
        duration = random.choice(["3 seconds", "17 seconds", "an uncomfortably long time", "exactly long enough"])

        if tone == "unhinged":
            desc = f"*{interaction.user.mention} stares at {user.mention}.* 🩸\n*They don't blink. Not once. {user.mention} looks away first. {interaction.user.mention} is still staring. 🔪*"
            color = RED
        elif tone == "possessive":
            desc = f"*{interaction.user.mention} stares at {user.mention} for {duration}.* 👁️\n*\"I could watch you forever. Actually, I have been. 🌸\"*"
            color = PINK
        else:
            desc = f"*{interaction.user.mention} stares at {user.mention} for {duration} without blinking.* 👁️\n*{user.mention} finally looks up. {interaction.user.mention} is already smiling. 🌸*"
            color = PINK

        embed = discord.Embed(description=desc, color=color)
        embed.set_footer(text="I like watching. 👁️")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="follow", description="Follow someone. Casually. 🌸")
    @app_commands.describe(user="Who to follow")
    @app_commands.checks.cooldown(1, 15.0)
    async def follow(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        tone = data.sanity_tone(uid)
        u = interaction.user.mention
        t = user.mention

        if tone == "sweet":
            desc = _pick(FOLLOW_SWEET, u, t)
            color = PINK
        elif tone == "possessive":
            desc = _pick(FOLLOW_POSSESSIVE, u, t)
            color = PINK
        else:
            desc = _pick(FOLLOW_UNHINGED, u, t)
            color = RED

        lu = data.gain_xp(uid, 15)
        embed = discord.Embed(description=desc, color=color)
        embed.set_footer(text="I know the route. 👁️")
        _levelup_field(embed, lu)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="watch", description="Watch someone from afar. 👁️")
    @app_commands.describe(user="Who to watch")
    async def watch(self, interaction: discord.Interaction, user: discord.Member):
        tone = data.sanity_tone(interaction.user.id)
        if tone == "unhinged":
            desc = f"*{interaction.user.mention} has been watching {user.mention} for hours.* 🩸\n*Every laugh. Every breath. Every blink. Catalogued.*"
            color = BLACK
        else:
            desc = f"*{interaction.user.mention} watches {user.mention} quietly from a distance.* 👁️\n*Every laugh. Every movement. Every expression. Memorized. 🌸*"
            color = BLACK
        embed = discord.Embed(description=desc, color=color)
        embed.set_footer(text="You're so beautiful when you don't know I'm watching. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="observe", description="Observe everything around you. 👁️")
    async def observe(self, interaction: discord.Interaction):
        count = interaction.guild.member_count if interaction.guild else 1
        tone = data.sanity_tone(interaction.user.id)
        if tone == "unhinged":
            desc = f"*{interaction.user.mention}'s eyes sweep the room.* 🩸\n\n👥 {count} people. *I've ranked them. By threat level. By proximity. By relevance. 🔪*"
            color = RED
        else:
            desc = f"*{interaction.user.mention} surveys the area.*\n\n👥 {count} people present.\n*I've catalogued them all. Threat assessments complete. 🌸*"
            color = RED
        embed = discord.Embed(title="👁️ OBSERVATION COMPLETE", description=desc, color=color)
        embed.set_footer(text="Always observing. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="spy", description="Gather intel on someone. 🌸")
    @app_commands.describe(user="Who to spy on")
    async def spy(self, interaction: discord.Interaction, user: discord.Member):
        facts = [
            f"joined this server on **{user.joined_at.strftime('%b %d, %Y')}**" if user.joined_at else "has been here a while",
            f"has **{len(user.roles)-1}** roles",
            f"their account was created on **{user.created_at.strftime('%b %d, %Y')}**",
        ]
        tone = data.sanity_tone(interaction.user.id)
        if tone == "unhinged":
            suffix = "\n\n🩸 *I know more. I always know more. I just choose what to share. 🔪*"
        else:
            suffix = "\n\n*There's more. But I'll keep some things to myself. 💕*"

        embed = discord.Embed(
            title=f"🔍 Intel on {user.display_name}",
            description=f"*Report filed by {interaction.user.mention}*\n\n🌸 {random.choice(facts)}{suffix}",
            color=PINK
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="Knowledge is protection. 👁️")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="whisper", description="Send a private message. Just between us. 💕")
    @app_commands.describe(user="Who to whisper to", message="What to whisper")
    async def whisper(self, interaction: discord.Interaction, user: discord.Member, message: str):
        tone = data.sanity_tone(interaction.user.id)
        prefix = (
            "*Their voice is too soft. Too close. Too certain.*\n\n"
            if tone == "unhinged" else
            "*They lean in close...*\n\n"
        )
        embed = discord.Embed(
            title=f"💕 Whisper → {user.display_name}",
            description=f"{prefix}*\"{message}\"*",
            color=RED if tone == "unhinged" else PINK
        )
        embed.set_footer(text="Just for you. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="letter", description="Send a love letter. 💌")
    @app_commands.describe(user="Who to write to")
    async def letter(self, interaction: discord.Interaction, user: discord.Member):
        tone = data.sanity_tone(interaction.user.id)
        if tone == "unhinged":
            letters = [
                f"*To {user.mention},*\n\n*I've filled 12 pages and torn them all up. This one stays.*\n*You don't get to leave. I need you to understand that.*\n\n*— {interaction.user.mention} 🔪*",
            ]
        elif tone == "possessive":
            letters = [
                f"*To {user.mention},*\n\n*I know I shouldn't send this. But I need you to know.*\n*You're everything. And I don't share everything.*\n\n*— {interaction.user.mention} 💕*",
            ]
        else:
            letters = [
                f"*To {user.mention},*\n\n*I've been writing this for weeks. I've thrown away 23 drafts. This one is honest.*\n*You make everything make sense. Please don't go anywhere. Ever.*\n\n*— {interaction.user.mention} 🌸*",
                f"*To my dearest {user.mention},*\n\n*I press flowers between pages of my diary with your name on them.*\n*Is that strange? It doesn't feel strange.*\n\n*— {interaction.user.mention} 💕*",
            ]
        embed = discord.Embed(
            title="💌 LOVE LETTER",
            description=random.choice(letters),
            color=RED if tone == "unhinged" else PINK
        )
        embed.set_footer(text="Sealed with something. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="threaten", description="Deliver a gentle warning. 🔪")
    @app_commands.describe(user="Who to warn")
    async def threaten(self, interaction: discord.Interaction, user: discord.Member):
        tone = data.sanity_tone(interaction.user.id)
        if tone == "unhinged":
            threats = [
                f"*{interaction.user.mention} steps very close to {user.mention}.* 🩸\n*\"I'm going to say this once. Once. And I need you to take it seriously. 🔪\"*",
                f"*{interaction.user.mention} doesn't say anything. Just stares.*\n*The silence is the threat. 🌸*",
            ]
        else:
            threats = [
                f"*{interaction.user.mention} smiles at {user.mention} very sweetly.* 🌸\n*\"I just want you to be careful. Accidents happen. 💕\"*",
                f"*{interaction.user.mention} leans in close.* 🔪\n*\"You seem smart. Smart people make good choices. 🌸\"*",
                f"*{interaction.user.mention} hands {user.mention} a folded note.*\n*It reads: \"I know your schedule. Just a reminder. 💕\"*",
            ]
        embed = discord.Embed(description=random.choice(threats), color=RED)
        embed.set_footer(text="This was a kindness. 🔪")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Social(bot))

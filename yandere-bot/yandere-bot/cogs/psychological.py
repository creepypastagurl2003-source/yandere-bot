import discord
from discord.ext import commands
from discord import app_commands
import random
import data

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d

GLITCH_CHARS = ["\u0300", "\u0301", "\u0302", "\u0308", "\u0327", "\u0330", "\u0333"]

COOLDOWN_MSG = "🌸 *Patience... wait {:.0f}s. 💕*"


def zalgo(text: str) -> str:
    result = []
    for ch in text:
        result.append(ch)
        for _ in range(random.randint(0, 3)):
            result.append(random.choice(GLITCH_CHARS))
    return "".join(result)


class Psychological(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(COOLDOWN_MSG.format(error.retry_after), ephemeral=True)

    @app_commands.command(name="sanity", description="Check your current sanity level. 🩸")
    async def sanity(self, interaction: discord.Interaction):
        level = data.get_sanity(interaction.user.id)
        obsession = data.get_obsession(interaction.user.id)
        bar = data.sanity_bar(level)
        state = data.sanity_state(level)

        if state == "stable":
            desc = "🌸 *Composed. Warm. Completely normal. Nothing to worry about.*"
            color = PINK
        elif state == "cracking":
            desc = "👁️ *The cracks are showing. You're managing. Barely.*"
            color = PINK
        elif state == "unstable":
            desc = "🩸 *The mask is slipping. People are starting to notice.*"
            color = RED
        else:
            desc = "🔪 *Gone. The mask is gone. This is all that's left.*"
            color = BLACK

        embed = discord.Embed(title="🩸 SANITY REPORT", color=color)
        embed.add_field(name="Sanity", value=f"{bar}\n`{level}/100`", inline=False)
        embed.add_field(name="Obsession", value=f"`{obsession}/100`", inline=True)
        embed.add_field(name="State", value=state.title(), inline=True)
        embed.add_field(name="Assessment", value=desc, inline=False)
        embed.set_footer(text=f"Report filed for {interaction.user.display_name} 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="breakdown", description="Have a dramatic breakdown. 🩸")
    @app_commands.checks.cooldown(1, 60.0)
    async def breakdown(self, interaction: discord.Interaction):
        uid = interaction.user.id
        profile = data.get_user(uid)
        drop = random.randint(10, 25)
        new_sanity = max(0, profile["sanity"] - drop)
        data.set_user(uid, sanity=new_sanity)

        if new_sanity <= 10:
            text = f"*{interaction.user.mention} is gone. Completely gone.*\n\n🩸 *There's nothing behind the eyes anymore. Just... devotion. Pure and total.*"
        elif new_sanity <= 30:
            text = f"*{interaction.user.mention}'s composure shatters completely.*\n\n🔪 *\"I do everything for them. EVERYTHING. And they just—\"*\n*The sentence dissolves into something quieter. Something scarier.*"
        else:
            text = f"*{interaction.user.mention} sinks down.*\n\n🩸 *\"I'm fine. I said I'm fine. Please don't ask again.\"*\n*Their hands are shaking. The smile doesn't reach their eyes.*"

        embed = discord.Embed(
            title="🩸 BREAKDOWN",
            description=f"{text}\n\n**Sanity:** `{profile['sanity']}/100` → `{new_sanity}/100`",
            color=BLACK
        )
        embed.set_footer(text="It passes. It always passes. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="calm", description="Attempt to regain composure. 🌸")
    @app_commands.checks.cooldown(1, 30.0)
    async def calm(self, interaction: discord.Interaction):
        uid = interaction.user.id
        profile = data.get_user(uid)
        gain = random.randint(5, 15)
        new_sanity = min(100, profile["sanity"] + gain)
        data.set_user(uid, sanity=new_sanity)

        if new_sanity >= 80:
            text = f"🌸 *{interaction.user.mention} straightens up. Smiles. Looks completely normal.*\n*\"See? Fine. I'm always fine. 💕\"*"
        elif new_sanity >= 50:
            text = f"*{interaction.user.mention} breathes slowly.*\n🌸 *\"It's okay. Everything is okay. I have to believe that.\"*"
        else:
            text = f"*{interaction.user.mention} tries. It helps a little.*\n🌸 *\"Tomorrow. Tomorrow will be better.\"*\n*Maybe.*"

        embed = discord.Embed(
            description=f"{text}\n\n**Sanity:** `{profile['sanity']}/100` → `{new_sanity}/100`",
            color=PINK
        )
        embed.set_footer(text="Composed. For now. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mask", description="Put the mask back on. 🌸")
    async def mask(self, interaction: discord.Interaction):
        sanity = data.get_sanity(interaction.user.id)
        if sanity >= 70:
            text = f"*{interaction.user.mention} adjusts their expression into something soft and approachable.*\n\n🌸 *\"Good morning! How are you? I'm great. Everything is great.\"*\n*Nobody notices the difference. Nobody ever does.*"
        elif sanity >= 40:
            text = f"*{interaction.user.mention} practices their smile in their phone screen.*\n\n🌸 *It's a little off. But close enough. Nobody looks that carefully anyway.*"
        else:
            text = f"*{interaction.user.mention} tries to put the mask back on.*\n\n🩸 *It doesn't fit right anymore. The edges show. But it's the best they can do.*"
        embed = discord.Embed(title="🌸 MASK ON", description=text, color=PINK)
        embed.set_footer(text="Smile. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="trueface", description="Drop the act. Show who you really are. 🔪")
    async def trueface(self, interaction: discord.Interaction):
        obsession = data.get_obsession(interaction.user.id)
        sanity = data.get_sanity(interaction.user.id)

        if obsession >= 80 and sanity <= 40:
            text = f"*{interaction.user.mention}'s smile fades completely.*\n\n🔪 *\"You want to see the real me? Fine. I will never — ever — let go. Not of you. Not of any of this. You are mine and I am yours and that is the end of it.\"*"
        elif obsession >= 60:
            text = f"*The warmth drains from {interaction.user.mention}'s face.*\n\n👁️ *\"I've been watching. I've been waiting. I've been very patient. And patient people always get what they want. 🔪\"*"
        else:
            text = f"*{interaction.user.mention} tilts their head.*\n\n🌸 *\"Did you think I was pretending? I've always been exactly this. You just weren't paying attention. 💕\"*"

        embed = discord.Embed(
            title="🔪 TRUE FACE REVEALED",
            description=text,
            color=RED if obsession >= 60 else PINK
        )
        embed.set_footer(text="This is who I am. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bloodmode", description="Toggle blood mode for darker responses. 🩸")
    async def bloodmode(self, interaction: discord.Interaction):
        gid = interaction.guild_id
        guild = data.get_guild(gid)
        new_state = not guild["blood_mode"]
        data.set_guild(gid, blood_mode=new_state)
        embed = discord.Embed(
            title=f"🩸 Blood Mode {'ACTIVATED' if new_state else 'DEACTIVATED'}",
            description=f"*{'The darkness is welcome here now. 🔪' if new_state else 'Back to the light. For now. 🌸'}*",
            color=RED if new_state else PINK
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="nightmode", description="Toggle night mode. 🌙")
    async def nightmode(self, interaction: discord.Interaction):
        gid = interaction.guild_id
        guild = data.get_guild(gid)
        new_state = not guild["night_mode"]
        data.set_guild(gid, night_mode=new_state)
        embed = discord.Embed(
            title=f"🌙 Night Mode {'ON' if new_state else 'OFF'}",
            description=f"*{'The lights are off. Good. I prefer the dark. 👁️' if new_state else 'The lights return. How ordinary. 🌸'}*",
            color=BLACK if new_state else PINK
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="silence", description="The bot goes quiet. 🤫")
    async def silence(self, interaction: discord.Interaction):
        embed = discord.Embed(description="*...*\n\n*I'm still here. I'm just not speaking.*\n\n*👁️*", color=BLACK)
        embed.set_footer(text="Silence isn't emptiness. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="glitch", description="A creepy glitch message. 👁️")
    @app_commands.checks.cooldown(1, 15.0)
    async def glitch(self, interaction: discord.Interaction):
        obsession = data.get_obsession(interaction.user.id)
        messages = [
            "I love you I love you I love you I love you",
            "Don't leave. Please. Don't leave.",
            "I see everything. Everything.",
            "You're mine. You've always been mine.",
            "The list is growing. Don't worry about the list.",
        ] if obsession < 70 else [
            "I would do anything. Anything. You understand? ANYTHING.",
            "There is no version of this where I let go.",
            "Mine mine mine mine mine mine mine mine",
            "I counted your heartbeats. 72 per minute. Beautiful.",
        ]
        glitched = zalgo(random.choice(messages))
        embed = discord.Embed(title="📡 SIGNAL ERROR", description=f"```\n{glitched}\n```", color=RED)
        embed.set_footer(text="Error. Or not. 🌸")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Psychological(bot))

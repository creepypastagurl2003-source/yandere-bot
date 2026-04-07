import discord
from discord.ext import commands
from discord import app_commands
import random

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d

FLOWERS = ["🌸 Cherry Blossom", "🌹 Red Rose", "💐 Bouquet", "🌷 Tulip", "🌺 Hibiscus", "🪷 Lotus"]
GIFTS = ["🍰 Homemade cake", "📚 Their favorite book (annotated)", "🎀 A handmade bracelet", "📷 A photo album", "🕯️ Scented candles", "🧸 A stuffed animal"]
BAKED = ["🍪 Cookies (your favorites, I checked)", "🎂 A cake with your name on it", "🥐 Fresh croissants", "🧁 Cupcakes (pink frosting)", "🍫 Handmade chocolates"]


class Aesthetic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pet", description="Give someone gentle head pats. 🌸")
    @app_commands.describe(user="Who to pet")
    async def pet(self, interaction: discord.Interaction, user: discord.Member):
        pats = [
            f"*{interaction.user.mention} gently pats {user.mention}'s head.*\n🌸 *\"Good. You're so good. Stay close. 💕\"*",
            f"*{interaction.user.mention} reaches out and softly ruffles {user.mention}'s hair.*\n🌸 *\"You're precious. Do you know that?\"*",
            f"*pat pat* 🌸\n*{user.mention} receives the gentlest, most carefully calculated head pat.*",
        ]
        embed = discord.Embed(description=random.choice(pats), color=PINK)
        embed.set_footer(text="So soft. So precious. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hug", description="A warm, slightly too-long hug. 💕")
    @app_commands.describe(user="Who to hug")
    async def hug(self, interaction: discord.Interaction, user: discord.Member):
        hugs = [
            f"*{interaction.user.mention} hugs {user.mention} tight and doesn't let go.*\n💕 *\"Just a little longer. Please. 🌸\"*",
            f"*{interaction.user.mention} wraps their arms around {user.mention}.*\n🌸 *\"Don't move. Let me stay like this. Just for a while. 💕\"*",
            f"*The hug lasts 47 seconds.* 🌸\n*{interaction.user.mention} counted.*",
        ]
        embed = discord.Embed(description=random.choice(hugs), color=PINK)
        embed.set_footer(text="I counted the seconds. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kiss", description="A soft, devoted kiss. 🌸")
    @app_commands.describe(user="Who to kiss")
    async def kiss(self, interaction: discord.Interaction, user: discord.Member):
        kisses = [
            f"*{interaction.user.mention} kisses {user.mention} on the cheek, very softly.* 🌸\n*\"I've imagined that 300 times. It was exactly right. 💕\"*",
            f"*{interaction.user.mention} leans in and—*\n\n🌸 *For a moment, everything is still.*\n*\"I love you,\" {interaction.user.mention} whispers. \"More than is probably healthy. 💕\"*",
        ]
        embed = discord.Embed(description=random.choice(kisses), color=PINK)
        embed.set_footer(text="Just for you. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stab", description="A completely fictional, absolutely harmless stab. 🔪")
    @app_commands.describe(user="Who to (fake) stab")
    async def stab(self, interaction: discord.Interaction, user: discord.Member):
        stabs = [
            f"*{interaction.user.mention} pulls out a foam knife.*\n🔪 *poke*\n*\"This is a metaphor. Probably. 🌸\"*",
            f"*{interaction.user.mention} dramatically pulls out a rubber knife.*\n🔪 *\"BETRAYAL\"*\n*{user.mention} survives. Barely. 🌸*",
            f"*{interaction.user.mention} narrows their eyes at {user.mention}.*\n🔪 *\"I would never. Hypothetically I would, but I never would. 💕\"*",
        ]
        embed = discord.Embed(
            description=random.choice(stabs),
            color=RED
        )
        embed.set_footer(text="Completely fictional. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bake", description="\"I made this for you. From scratch.\" 🍰")
    @app_commands.describe(user="Who you baked for")
    async def bake(self, interaction: discord.Interaction, user: discord.Member):
        item = random.choice(BAKED)
        embed = discord.Embed(
            description=f"*{interaction.user.mention} slides a carefully wrapped package toward {user.mention}.*\n\n🌸 **{item}**\n\n*\"I woke up at 5 AM to make this. I wanted it to be perfect. Is it perfect? Tell me it's perfect. 💕\"*",
            color=PINK
        )
        embed.set_footer(text="Made from scratch. With devotion. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gift", description="Give someone a very thoughtful gift. 🎀")
    @app_commands.describe(user="Who to gift")
    async def gift(self, interaction: discord.Interaction, user: discord.Member):
        item = random.choice(GIFTS)
        embed = discord.Embed(
            title=f"🎀 A Gift for {user.display_name}",
            description=f"*{interaction.user.mention} presents {user.mention} with:*\n\n**{item}**\n\n🌸 *\"I've been planning this for a while. I pay attention. I always pay attention. 💕\"*",
            color=PINK
        )
        embed.set_footer(text="No occasion needed. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="flower", description="Present a flower to someone. 🌸")
    @app_commands.describe(user="Who to give flowers to")
    async def flower(self, interaction: discord.Interaction, user: discord.Member):
        flower = random.choice(FLOWERS)
        meanings = {
            "🌸 Cherry Blossom": "fleeting beauty, devotion",
            "🌹 Red Rose": "deep, consuming love",
            "💐 Bouquet": "everything I cannot say aloud",
            "🌷 Tulip": "a declaration",
            "🌺 Hibiscus": "delicate obsession",
            "🪷 Lotus": "purity rising from darkness",
        }
        meaning = meanings.get(flower, "something only I understand")
        embed = discord.Embed(
            description=f"*{interaction.user.mention} holds out a {flower} to {user.mention}.*\n\n🌸 *\"In the language of flowers, this means: {meaning}. 💕\"*",
            color=PINK
        )
        embed.set_footer(text="I pressed one in my diary. 🌸")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Aesthetic(bot))

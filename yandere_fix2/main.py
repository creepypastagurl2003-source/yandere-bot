import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from keep_alive import keep_alive
import data
import os
import random
import logging
import asyncio

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("yandere-bot")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="~", intents=intents)

AMBIENT_MESSAGES = [
    "🌸 *I've been watching you. Don't worry — I always will. 💕*",
    "👁️ *Did you feel that? Someone is thinking about you very, very hard right now.*",
    "🔪 *Everything is fine. Everything is always fine when I'm nearby. 🌸*",
    "💕 *I wrote about you in my diary again today. You'd blush if you knew.*",
    "🌸 *Don't talk to them. You don't need anyone else. You have me. 💕*",
    "👁️ *I memorized your schedule. Just so I know you're safe. That's all. 🌸*",
    "🔪 *Rivals come and go. But I never leave. Remember that. 💕*",
    "🌸 *Your smile today was for me. I know it was. It had to be.*",
]


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} ({bot.user.id})")
    if not ambient_task.is_running():
        ambient_task.start()
    if not passive_obsession_task.is_running():
        passive_obsession_task.start()
    logger.info("Background tasks started.")


async def setup_hook_load():
    cogs = [
        "cogs.core", "cogs.relationship", "cogs.rival",
        "cogs.social", "cogs.dailylife", "cogs.psychological",
        "cogs.moderation", "cogs.stalker", "cogs.aesthetic", "cogs.events",
        "cogs.reactionroles", "cogs.characters",
    ]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logger.info(f"Loaded cog: {cog}")
        except Exception as e:
            logger.error(f"Failed to load {cog}: {e}")


def _get_ambient_channel(guild: discord.Guild) -> discord.TextChannel | None:
    """Return the configured ambient channel, or fall back to first available."""
    cid = data._db.get("guild_config", {}).get(str(guild.id), {}).get("ambient_channel")
    if cid:
        ch = guild.get_channel(int(cid))
        if ch and ch.permissions_for(guild.me).send_messages:
            return ch
    return next(
        (ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages),
        None,
    )


@tasks.loop(hours=24)
async def ambient_task():
    if random.random() > 0.5:
        return
    message = random.choice(AMBIENT_MESSAGES)
    for guild in bot.guilds:
        channel = _get_ambient_channel(guild)
        if channel:
            try:
                await channel.send(message)
            except Exception:
                pass


@tasks.loop(minutes=30)
async def passive_obsession_task():
    """Passively increase obsession for users who have claims or crushes."""
    changed = False
    for uid_str, profile in data._db.get("users", {}).items():
        if profile.get("claimed") or profile.get("crush"):
            bump = random.randint(1, 4)
            new_level = min(100, profile.get("obsession_level", 0) + bump)
            if new_level != profile.get("obsession_level", 0):
                profile["obsession_level"] = new_level
                sanity_drop = random.randint(0, 2)
                profile["sanity"] = max(0, profile.get("sanity", 85) - sanity_drop)
                changed = True
    if changed:
        data.save()
        logger.info("Passive obsession tick applied.")


@ambient_task.before_loop
@passive_obsession_task.before_loop
async def before_tasks():
    await bot.wait_until_ready()
    await asyncio.sleep(random.randint(60, 180))


async def main():
    data.load()
    async with bot:
        await setup_hook_load()
        TOKEN = os.environ.get("BOT4_TOKEN")
        if not TOKEN:
            raise RuntimeError("BOT4_TOKEN is not set.")
        keep_alive()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

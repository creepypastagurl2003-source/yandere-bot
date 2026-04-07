import discord
from discord.ext import commands
from discord import app_commands
import data
import logging
import re

logger = logging.getLogger("yandere-bot.rr")

PINK = 0xff4d6d
RED = 0x8b0000
BLACK = 0x0d0d0d
MIDNIGHT = 0x1a0a2e   # deep purple — used for gate/vent embeds

GATE_TITLE_DEFAULT = "🔒 Channel Access"
GATE_DESC_DEFAULT = "React below to gain access to this channel."
GATE_RULES_DEFAULT = ""

PANEL_TITLE_DEFAULT = "✨ Role Selection"
PANEL_DESC_DEFAULT = "React to choose your role."
PANEL_RULES_DEFAULT = ""

# Matches a single unicode emoji or a custom Discord emoji <:name:id> / <a:name:id>
EMOJI_RE = re.compile(
    r"(?:<a?:\w+:\d+>|"
    r"[\U00010000-\U0010ffff]|"
    r"[\u2600-\u27BF]|"
    r"[\uD800-\uDBFF][\uDC00-\uDFFF])"
)


# ── Pure helpers (also used by tests) ─────────────────────────────────────────

def _parse_pairs(args: tuple | list) -> list[tuple[str, str]] | None:
    """
    Parse alternating (emoji, role_name) from a flat token sequence.
    Role names may contain spaces — tokens that aren't emojis are joined.
    Returns list of (emoji_str, role_name_str) or None on bad input.
    """
    pairs = []
    tokens = list(args)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if not EMOJI_RE.search(token):
            return None  # Expected an emoji here
        emoji = token
        i += 1
        role_parts = []
        while i < len(tokens) and not EMOJI_RE.search(tokens[i]):
            role_parts.append(tokens[i])
            i += 1
        if not role_parts:
            return None  # No role name after emoji
        pairs.append((emoji, " ".join(role_parts)))
    return pairs if pairs else None


def _parse_pairs_from_string(raw: str) -> list[tuple[str, str]] | None:
    """Split a raw string on whitespace and delegate to _parse_pairs."""
    tokens = raw.strip().split()
    return _parse_pairs(tokens) if tokens else None


def _save_rr(message_id: int, guild_id: int, channel_id: int, role_map: dict[str, int]) -> None:
    data._db["reaction_roles"][str(message_id)] = {
        "guild_id": guild_id,
        "channel_id": channel_id,
        "roles": role_map,
    }
    data.save()


def _get_rr(message_id: int) -> dict | None:
    return data._db.get("reaction_roles", {}).get(str(message_id))


# ── Extracted listener logic (also tested directly) ────────────────────────────

async def handle_reaction_add(bot, payload) -> None:
    """Core logic for on_raw_reaction_add. Extracted for testability."""
    if payload.user_id == bot.user.id:
        return
    if not payload.guild_id:
        return

    entry = _get_rr(payload.message_id)
    if not entry:
        return

    emoji_str = str(payload.emoji)
    role_id = entry["roles"].get(emoji_str)
    if not role_id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
    member = guild.get_member(payload.user_id)
    role = guild.get_role(role_id)
    if member and role:
        try:
            import discord as _discord
            await member.add_roles(role, reason="Reaction role")
            logger.debug(f"Gave role {role.name} to {member} via reaction")
        except Exception as e:
            logger.error(f"Failed to give role: {e}")


async def handle_reaction_remove(bot, payload) -> None:
    """Core logic for on_raw_reaction_remove. Extracted for testability."""
    if payload.user_id == bot.user.id:
        return
    if not payload.guild_id:
        return

    entry = _get_rr(payload.message_id)
    if not entry:
        return

    emoji_str = str(payload.emoji)
    role_id = entry["roles"].get(emoji_str)
    if not role_id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
    member = guild.get_member(payload.user_id)
    role = guild.get_role(role_id)
    if member and role:
        try:
            await member.remove_roles(role, reason="Reaction role removed")
            logger.debug(f"Removed role {role.name} from {member} via reaction")
        except Exception as e:
            logger.error(f"Failed to remove role: {e}")


# ── Shared setup logic ────────────────────────────────────────────────────────

async def _do_setup(
    bot,
    guild: discord.Guild,
    target_channel: discord.TextChannel,
    pairs: list[tuple[str, str]],
    reply_fn,          # async callable(str, delete_after=N) for error messages
    delete_invoker_fn, # async callable() or None
) -> bool:
    """
    Core setup logic shared between prefix and slash commands.
    Returns True on success.
    """
    resolved: list[tuple[str, discord.Role]] = []
    for emoji, role_name in pairs:
        role = discord.utils.find(
            lambda r, n=role_name.lower(): r.name.lower() == n,
            guild.roles
        )
        if not role:
            await reply_fn(f"🩸 *Role `{role_name}` not found. Check the spelling. 🔪*")
            return False
        if role >= guild.me.top_role:
            await reply_fn(f"🔪 *I can't assign `{role.name}` — it's above my highest role.*")
            return False
        resolved.append((emoji, role))

    if len(resolved) > 20:
        await reply_fn("🌸 *Maximum 20 reaction roles per message.*")
        return False

    embed = discord.Embed(
        title="🌸 Reaction Roles",
        description=(
            "*React to receive a role. Remove your reaction to lose it.*\n\n"
            "*Choose your role… I'll be watching. 👁️🌸*"
        ),
        color=PINK,
    )
    for emoji, role in resolved:
        embed.add_field(name=emoji, value=role.mention, inline=True)
    embed.set_footer(text="I notice everything. Every choice. 🔪")

    try:
        msg = await target_channel.send(embed=embed)
    except discord.Forbidden:
        await reply_fn(f"🔪 *I can't send messages to {target_channel.mention}.*")
        return False

    for emoji, _ in resolved:
        try:
            await msg.add_reaction(emoji)
        except discord.HTTPException:
            await reply_fn(
                f"⚠️ *Couldn't add reaction `{emoji}` — it may be invalid or external.*"
            )

    role_map = {emoji: role.id for emoji, role in resolved}
    _save_rr(msg.id, guild.id, target_channel.id, role_map)

    if delete_invoker_fn:
        try:
            await delete_invoker_fn()
        except discord.HTTPException:
            pass

    logger.info(f"RR set up: msg={msg.id} guild={guild.id} roles={list(role_map.keys())}")
    return True


def _build_panel_embed(
    pairs: list[tuple[str, str]],
    title: str = PANEL_TITLE_DEFAULT,
    description: str = PANEL_DESC_DEFAULT,
    rules: str = PANEL_RULES_DEFAULT,
    color: int = MIDNIGHT,
) -> discord.Embed:
    """Build a styled multi-role panel embed with pairs listed in the body."""
    role_lines = "\n".join(f"{emoji} — {name}" for emoji, name in pairs)
    desc = f"{description}\n\n{role_lines}" if description else role_lines
    embed = discord.Embed(title=title, description=desc, color=color)
    if rules:
        embed.add_field(name="\u200b", value=rules, inline=False)
    return embed


def _build_gate_embed(
    emoji: str,
    title: str = GATE_TITLE_DEFAULT,
    description: str = GATE_DESC_DEFAULT,
    rules: str = GATE_RULES_DEFAULT,
    color: int = MIDNIGHT,
) -> discord.Embed:
    """Build a styled channel-gate embed."""
    desc = f"{description}\n\n**React below to enter:**\n{emoji} — Access"
    embed = discord.Embed(title=title, description=desc, color=color)
    if rules:
        embed.add_field(name="\u200b", value=rules, inline=False)
    return embed


def _build_list_embed(guild: discord.Guild) -> discord.Embed | None:
    rr_data = data._db.get("reaction_roles", {})
    guild_entries = {
        mid: entry for mid, entry in rr_data.items()
        if entry.get("guild_id") == guild.id
    }
    if not guild_entries:
        return None
    embed = discord.Embed(title="👁️ Active Reaction Role Messages", color=PINK)
    for mid, entry in guild_entries.items():
        ch = guild.get_channel(entry["channel_id"])
        ch_str = ch.mention if ch else f"`#{entry['channel_id']}`"
        role_lines = "\n".join(
            f"{emoji} → <@&{rid}>" for emoji, rid in entry["roles"].items()
        )
        embed.add_field(
            name=f"Message `{mid}`",
            value=f"Channel: {ch_str}\n{role_lines}",
            inline=False,
        )
    embed.set_footer(text="I keep track of everything. 🔪")
    return embed


# ── Cog ───────────────────────────────────────────────────────────────────────

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ════════════════════════════════════════════════════════════════════
    # SLASH COMMANDS  (/rr setup | /rr list | /rr delete)
    # ════════════════════════════════════════════════════════════════════

    rr_slash = app_commands.Group(
        name="rr",
        description="Reaction role management 🌸",
        guild_only=True,
    )

    @rr_slash.command(name="setup", description="Send a reaction role message to a channel 🌸")
    @app_commands.describe(
        channel="Channel to post the reaction role message in",
        pairs='Emoji + role pairs e.g. "🌸 Soft 🔪 Killer 🖤 Obsessed"',
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_rr_setup(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        pairs: str,
    ):
        parsed = _parse_pairs_from_string(pairs)
        if not parsed:
            await interaction.response.send_message(
                "🔪 *Bad format. Use alternating emoji and role name:*\n"
                "`🌸 Soft 🔪 Killer 🖤 Obsessed`",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        async def reply(msg):
            await interaction.followup.send(msg, ephemeral=True)

        ok = await _do_setup(self.bot, interaction.guild, channel, parsed, reply, None)
        if ok:
            await interaction.followup.send(
                f"🌸 *Reaction roles set up in {channel.mention}. I'm watching. 👁️*",
                ephemeral=True,
            )

    @slash_rr_setup.error
    async def slash_rr_setup_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "🌸 *You need `Manage Roles` to use this. 💕*", ephemeral=True
            )
        else:
            logger.error(f"Slash RR setup error: {error}")
            await interaction.response.send_message(
                f"🩸 *Something went wrong: `{error}`*", ephemeral=True
            )

    @rr_slash.command(name="list", description="List active reaction role messages 👁️")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_rr_list(self, interaction: discord.Interaction):
        embed = _build_list_embed(interaction.guild)
        if embed is None:
            await interaction.response.send_message(
                "🌸 *No reaction role messages set up yet. 💕*", ephemeral=True
            )
            return
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash_rr_list.error
    async def slash_rr_list_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "🌸 *You need `Manage Roles` to use this. 💕*", ephemeral=True
            )

    @rr_slash.command(name="delete", description="Remove a reaction role setup by message ID 🔪")
    @app_commands.describe(message_id="The ID of the reaction role message to remove")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_rr_delete(self, interaction: discord.Interaction, message_id: str):
        await interaction.response.defer(ephemeral=True)
        rr_data = data._db.get("reaction_roles", {})
        entry = rr_data.get(message_id)
        if not entry or entry.get("guild_id") != interaction.guild.id:
            await interaction.followup.send(
                "🌸 *No reaction role message found with that ID. 💕*", ephemeral=True
            )
            return

        channel = interaction.guild.get_channel(entry.get("channel_id"))
        msg_deleted = False
        if channel:
            try:
                msg = await channel.fetch_message(int(message_id))
                await msg.delete()
                msg_deleted = True
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                pass

        del data._db["reaction_roles"][message_id]
        data.save()

        if msg_deleted:
            await interaction.followup.send(
                f"🔪 *Reaction role message deleted from {channel.mention} and removed from tracking. 🌸*",
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                f"🌸 *Removed from tracking. (Message `{message_id}` may have already been deleted.) 💕*",
                ephemeral=True,
            )

    @slash_rr_delete.error
    async def slash_rr_delete_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "🌸 *You need `Manage Roles` to use this. 💕*", ephemeral=True
            )

    @rr_slash.command(name="gate", description="Send a styled channel-gate message 🌙")
    @app_commands.describe(
        channel="Channel to post the gate message in",
        emoji="Reaction emoji users click to gain access (e.g. 🧸)",
        role="Role to assign when someone reacts",
        title="Embed title (leave blank for default vent-space title)",
        description="Body text (leave blank for default)",
        rules="Footer rules text (leave blank for default)",
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_rr_gate(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        emoji: str,
        role: discord.Role,
        title: str = GATE_TITLE_DEFAULT,
        description: str = GATE_DESC_DEFAULT,
        rules: str = GATE_RULES_DEFAULT,
    ):
        emoji = emoji.strip()
        if not EMOJI_RE.search(emoji):
            await interaction.response.send_message(
                "🌙 *That doesn't look like a valid emoji.*", ephemeral=True
            )
            return

        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                f"🔪 *I can't assign `{role.name}` — it's above my highest role.*",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        embed = _build_gate_embed(emoji, title=title, description=description, rules=rules)
        try:
            msg = await channel.send(embed=embed)
        except discord.Forbidden:
            await interaction.followup.send(
                f"🔪 *I can't send messages to {channel.mention}.*", ephemeral=True
            )
            return

        try:
            await msg.add_reaction(emoji)
        except discord.HTTPException:
            await interaction.followup.send(
                f"⚠️ *Couldn't add reaction `{emoji}` — may be invalid or external.*",
                ephemeral=True,
            )

        _save_rr(msg.id, interaction.guild.id, channel.id, {emoji: role.id})

        await interaction.followup.send(
            f"🌙 *Gate message sent to {channel.mention}. Reacting with {emoji} will give `{role.name}`. 👁️*",
            ephemeral=True,
        )
        logger.info(f"Gate set up: msg={msg.id} guild={interaction.guild.id} emoji={emoji} role={role.id}")

    @slash_rr_gate.error
    async def slash_rr_gate_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "🌸 *You need `Manage Roles` to use this. 💕*", ephemeral=True
            )
        else:
            logger.error(f"Slash gate error: {error}")
            await interaction.response.send_message(
                f"🩸 *Something went wrong: `{error}`*", ephemeral=True
            )

    @rr_slash.command(name="panel", description="Send a styled multi-role selection panel ✨")
    @app_commands.describe(
        channel="Channel to post the panel in",
        pairs='Emoji + role pairs e.g. "🎀 Senpai 🌸 Kawaii 🐾 Neko"',
        title="Panel title",
        description="Intro text shown above the role list",
        rules="Footer text shown at the bottom (separate lines with \\n)",
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_rr_panel(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        pairs: str,
        title: str = PANEL_TITLE_DEFAULT,
        description: str = PANEL_DESC_DEFAULT,
        rules: str = PANEL_RULES_DEFAULT,
    ):
        parsed = _parse_pairs_from_string(pairs)
        if not parsed:
            await interaction.response.send_message(
                "✨ *Bad format. Alternate emoji and role name:*\n`🎀 Senpai 🌸 Kawaii 🐾 Neko`",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        resolved: list[tuple[str, discord.Role]] = []
        for emoji, role_name in parsed:
            role = discord.utils.find(
                lambda r, n=role_name.lower(): r.name.lower() == n,
                interaction.guild.roles,
            )
            if not role:
                await interaction.followup.send(
                    f"🩸 *Role `{role_name}` not found. Check the spelling.*", ephemeral=True
                )
                return
            if role >= interaction.guild.me.top_role:
                await interaction.followup.send(
                    f"🔪 *I can't assign `{role.name}` — it's above my highest role.*", ephemeral=True
                )
                return
            resolved.append((emoji, role))

        if len(resolved) > 20:
            await interaction.followup.send("✨ *Maximum 20 roles per panel.*", ephemeral=True)
            return

        display_pairs = [(emoji, role.name) for emoji, role in resolved]
        rules_actual = rules.replace("\\n", "\n")
        embed = _build_panel_embed(display_pairs, title=title, description=description, rules=rules_actual)

        try:
            msg = await channel.send(embed=embed)
        except discord.Forbidden:
            await interaction.followup.send(
                f"🔪 *I can't send messages to {channel.mention}.*", ephemeral=True
            )
            return

        for emoji, _ in resolved:
            try:
                await msg.add_reaction(emoji)
            except discord.HTTPException:
                await interaction.followup.send(
                    f"⚠️ *Couldn't add reaction `{emoji}` — may be invalid or external.*",
                    ephemeral=True,
                )

        role_map = {emoji: role.id for emoji, role in resolved}
        _save_rr(msg.id, interaction.guild.id, channel.id, role_map)

        await interaction.followup.send(
            f"✨ *Panel sent to {channel.mention} with {len(resolved)} role(s). 👁️*", ephemeral=True
        )
        logger.info(f"Panel set up: msg={msg.id} guild={interaction.guild.id} roles={list(role_map.keys())}")

    @slash_rr_panel.error
    async def slash_rr_panel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "🌸 *You need `Manage Roles` to use this. 💕*", ephemeral=True
            )
        else:
            logger.error(f"Slash panel error: {error}")
            await interaction.response.send_message(
                f"🩸 *Something went wrong: `{error}`*", ephemeral=True
            )

    # ════════════════════════════════════════════════════════════════════
    # PREFIX COMMANDS — ~rr <subcommand>
    #   ~rr #channel emoji Role...   → setup
    #   ~rr list                     → list active messages
    #   ~rr del <id>                 → remove a message
    #   ~rr gate #channel emoji Role → gate embed
    #   ~rr panel #channel emoji...  → panel embed
    # Also available standalone: ~gate, ~panel
    # ════════════════════════════════════════════════════════════════════

    @commands.group(name="rr", aliases=["reactrole", "reactionrole"], invoke_without_command=True)
    @commands.guild_only()
    async def rr(self, ctx: commands.Context, channel: discord.TextChannel = None, *args):
        """
        Reaction roles group.
        ~rr #channel emoji Role ...  — set up reaction roles
        ~rr list                     — list active messages
        ~rr del <id>                 — remove a message
        ~rr gate #channel emoji Role — styled gate embed
        ~rr panel #channel emoji...  — styled multi-role panel
        """
        if channel is None:
            await ctx.send(
                "🌸 **Reaction Roles**\n"
                "`~rr #channel emoji Role ...` — set up\n"
                "`~rr list` — see active messages\n"
                "`~rr del <id>` — remove a message\n"
                "`~rr gate #channel emoji Role` — single-access gate\n"
                "`~rr panel #channel emoji Role...` — multi-role panel",
                delete_after=20,
            )
            return

        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("🌸 *You need `Manage Roles` for this. 💕*", delete_after=10)
            return

        if not args:
            await ctx.send(
                "🌸 *Usage:* `~rr #channel emoji Role emoji Role ...`\n"
                "*Example:* `~rr #roles 🌸 Soft 🔪 Killer`",
                delete_after=15,
            )
            return

        parsed = _parse_pairs(list(args))
        if not parsed:
            await ctx.send(
                "🔪 *Bad format — alternate emoji and role name.*\n"
                "*Example:* `~rr #roles 🌸 Soft 🔪 Killer`",
                delete_after=15,
            )
            return

        async def reply(msg):
            await ctx.send(msg, delete_after=15)

        ok = await _do_setup(self.bot, ctx.guild, channel, parsed, reply, ctx.message.delete)
        if ok:
            await ctx.send(
                f"🌸 *Reaction roles set up in {channel.mention}. I'm watching every reaction. 👁️*",
                delete_after=8,
            )

    @rr.error
    async def rr_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send(
                "🔪 *Channel not found.*\n"
                "*Tip: use `~rr list` to see active messages, or `~rr` for help.*",
                delete_after=12,
            )
        else:
            logger.error(f"RR group error: {error}")
            await ctx.send(f"🩸 *Something went wrong: `{error}`*", delete_after=10)

    # ── Subcommand: list ──────────────────────────────────────────────

    @rr.command(name="list", aliases=["l", "ls"])
    @commands.guild_only()
    async def rr_list(self, ctx: commands.Context):
        """List all active reaction role messages in this server."""
        embed = _build_list_embed(ctx.guild)
        if embed is None:
            await ctx.send("🌸 *No reaction role messages set up yet. 💕*", delete_after=10)
            return
        await ctx.send(embed=embed)

    # ── Subcommand: del ───────────────────────────────────────────────

    @rr.command(name="del", aliases=["delete", "remove"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def rr_del(self, ctx: commands.Context, message_id: int):
        """Remove a reaction role setup by message ID and delete the message from the channel."""
        key = str(message_id)
        entry = data._db.get("reaction_roles", {}).get(key)
        if not entry or entry.get("guild_id") != ctx.guild.id:
            await ctx.send("🌸 *No reaction role message found with that ID. 💕*", delete_after=10)
            return

        channel = ctx.guild.get_channel(entry.get("channel_id"))
        msg_deleted = False
        if channel:
            try:
                msg = await channel.fetch_message(message_id)
                await msg.delete()
                msg_deleted = True
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                pass

        del data._db["reaction_roles"][key]
        data.save()

        if msg_deleted:
            await ctx.send(
                f"🔪 *Reaction role message deleted from {channel.mention} and removed from tracking. 🌸*",
                delete_after=8,
            )
        else:
            await ctx.send(
                f"🌸 *Removed from tracking. (Message `{message_id}` may have already been deleted.) 💕*",
                delete_after=10,
            )

    @rr_del.error
    async def rr_del_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🌸 *Usage:* `~rr del <message_id>`", delete_after=10)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("🌸 *You need `Manage Roles` for this. 💕*", delete_after=10)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("🔪 *That doesn't look like a valid message ID.*", delete_after=10)

    # ── Subcommand: gate ──────────────────────────────────────────────

    @rr.command(name="gate", aliases=["vent"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def rr_gate(self, ctx: commands.Context, channel: discord.TextChannel, emoji: str, *role_parts):
        """Send a styled single-access gate embed. Usage: ~rr gate #channel emoji Role"""
        await self._do_gate(ctx, channel, emoji, role_parts)

    @rr_gate.error
    async def rr_gate_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🌙 *You need `Manage Roles` for this. 💕*", delete_after=10)
        elif isinstance(error, (commands.MissingRequiredArgument, commands.ChannelNotFound)):
            await ctx.send("🌙 *Usage:* `~rr gate #channel emoji RoleName`", delete_after=10)

    # ── Subcommand: panel ─────────────────────────────────────────────

    @rr.command(name="panel", aliases=["roles"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def rr_panel(self, ctx: commands.Context, channel: discord.TextChannel, *args):
        """Send a styled multi-role panel. Usage: ~rr panel #channel emoji Role emoji Role"""
        await self._do_panel(ctx, channel, args)

    @rr_panel.error
    async def rr_panel_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("✨ *You need `Manage Roles` for this. 💕*", delete_after=10)
        elif isinstance(error, (commands.MissingRequiredArgument, commands.ChannelNotFound)):
            await ctx.send("✨ *Usage:* `~rr panel #channel emoji Role emoji Role ...`", delete_after=10)

    # ── Standalone aliases: ~gate  ~panel ────────────────────────────

    @commands.command(name="gate", aliases=["vent", "ventspace"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def gate(self, ctx: commands.Context, channel: discord.TextChannel, emoji: str, *role_parts):
        """Standalone alias for ~rr gate."""
        await self._do_gate(ctx, channel, emoji, role_parts)

    @gate.error
    async def gate_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🌙 *You need `Manage Roles` for this. 💕*", delete_after=10)
        elif isinstance(error, (commands.MissingRequiredArgument, commands.ChannelNotFound)):
            await ctx.send(
                "🌙 *Usage:* `~gate #channel emoji RoleName`\n"
                "*Or:* `~rr gate #channel emoji RoleName`",
                delete_after=12,
            )

    @commands.command(name="panel", aliases=["rolepanel"])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def panel(self, ctx: commands.Context, channel: discord.TextChannel, *args):
        """Standalone alias for ~rr panel."""
        await self._do_panel(ctx, channel, args)

    @panel.error
    async def panel_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("✨ *You need `Manage Roles` for this. 💕*", delete_after=10)
        elif isinstance(error, (commands.MissingRequiredArgument, commands.ChannelNotFound)):
            await ctx.send(
                "✨ *Usage:* `~panel #channel emoji Role emoji Role ...`\n"
                "*Or:* `~rr panel #channel emoji Role ...`",
                delete_after=12,
            )

    # ── Shared implementation helpers ─────────────────────────────────

    async def _do_gate(self, ctx, channel, emoji, role_parts):
        if not role_parts:
            await ctx.send(
                "🌙 *Usage:* `~rr gate #channel emoji RoleName`", delete_after=15
            )
            return
        emoji = emoji.strip()
        if not EMOJI_RE.search(emoji):
            await ctx.send("🌙 *That doesn't look like a valid emoji.*", delete_after=10)
            return
        role_name = " ".join(role_parts)
        role = discord.utils.find(
            lambda r, n=role_name.lower(): r.name.lower() == n, ctx.guild.roles
        )
        if not role:
            await ctx.send(f"🩸 *Role `{role_name}` not found. Check the spelling.*", delete_after=15)
            return
        if role >= ctx.guild.me.top_role:
            await ctx.send(f"🔪 *I can't assign `{role.name}` — it's above my highest role.*", delete_after=10)
            return
        embed = _build_gate_embed(emoji)
        try:
            msg = await channel.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(f"🔪 *I can't send to {channel.mention}.*", delete_after=10)
            return
        try:
            await msg.add_reaction(emoji)
        except discord.HTTPException:
            await ctx.send(f"⚠️ *Couldn't add reaction `{emoji}`.*", delete_after=10)
        _save_rr(msg.id, ctx.guild.id, channel.id, {emoji: role.id})
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass
        await ctx.send(
            f"🌙 *Gate sent to {channel.mention}. {emoji} gives `{role.name}`. 👁️*", delete_after=8
        )
        logger.info(f"Gate set up: msg={msg.id} guild={ctx.guild.id} emoji={emoji} role={role.id}")

    async def _do_panel(self, ctx, channel, args):
        if not args:
            await ctx.send(
                "✨ *Usage:* `~rr panel #channel emoji Role emoji Role ...`", delete_after=15
            )
            return
        parsed = _parse_pairs(list(args))
        if not parsed:
            await ctx.send(
                "✨ *Bad format — alternate emoji and role name.*", delete_after=15
            )
            return
        resolved: list[tuple[str, discord.Role]] = []
        for emoji, role_name in parsed:
            role = discord.utils.find(
                lambda r, n=role_name.lower(): r.name.lower() == n, ctx.guild.roles
            )
            if not role:
                await ctx.send(f"🩸 *Role `{role_name}` not found.*", delete_after=15)
                return
            if role >= ctx.guild.me.top_role:
                await ctx.send(f"🔪 *Can't assign `{role.name}` — above my highest role.*", delete_after=10)
                return
            resolved.append((emoji, role))
        if len(resolved) > 20:
            await ctx.send("✨ *Maximum 20 roles per panel.*", delete_after=10)
            return
        display_pairs = [(e, r.name) for e, r in resolved]
        embed = _build_panel_embed(display_pairs)
        try:
            msg = await channel.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(f"🔪 *I can't send to {channel.mention}.*", delete_after=10)
            return

        for emoji, _ in resolved:
            try:
                await msg.add_reaction(emoji)
            except discord.HTTPException:
                await ctx.send(
                    f"⚠️ *Couldn't add reaction `{emoji}` — may be invalid or external.*",
                    delete_after=15,
                )

        role_map = {emoji: role.id for emoji, role in resolved}
        _save_rr(msg.id, ctx.guild.id, channel.id, role_map)

        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        await ctx.send(
            f"✨ *Panel sent to {channel.mention} with {len(resolved)} role(s). 👁️*",
            delete_after=8,
        )
        logger.info(f"Panel set up: msg={msg.id} guild={ctx.guild.id} roles={list(role_map.keys())}")

    # ════════════════════════════════════════════════════════════════════
    # REACTION LISTENERS
    # ════════════════════════════════════════════════════════════════════

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await handle_reaction_add(self.bot, payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await handle_reaction_remove(self.bot, payload)


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))

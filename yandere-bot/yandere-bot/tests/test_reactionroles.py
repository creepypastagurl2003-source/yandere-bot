"""
Unit tests for cogs/reactionroles.py

Covers:
  - _parse_pairs / _parse_pairs_from_string  (pure logic, no Discord)
  - _save_rr / _get_rr                       (data-layer helpers)
  - data module initialises reaction_roles    (startup safety)
  - on_raw_reaction_add listener             (async, mocked Discord)
  - on_raw_reaction_remove listener          (async, mocked Discord)
"""

import sys
import os
import asyncio
import unittest
from unittest.mock import MagicMock, AsyncMock, patch

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# ── Stub the entire discord namespace before any bot import ───────────────────
_discord_stub = MagicMock()
_discord_stub.TextChannel = type("TextChannel", (), {})
_discord_stub.Guild = type("Guild", (), {})
_discord_stub.Role = type("Role", (), {})
_discord_stub.Member = type("Member", (), {})
_discord_stub.Embed = MagicMock(return_value=MagicMock())
_discord_stub.utils = MagicMock()
_discord_stub.Forbidden = Exception
_discord_stub.HTTPException = Exception

_commands_stub = MagicMock()
_commands_stub.Cog = type("Cog", (), {"listener": staticmethod(lambda f: f)})
_commands_stub.command = lambda **kw: (lambda f: f)
_commands_stub.has_permissions = lambda **kw: (lambda f: f)
_commands_stub.guild_only = lambda: (lambda f: f)

_app_commands_stub = MagicMock()

sys.modules.setdefault("discord", _discord_stub)
sys.modules.setdefault("discord.ext", MagicMock())
sys.modules.setdefault("discord.ext.commands", _commands_stub)
sys.modules.setdefault("discord.ext.tasks", MagicMock())
sys.modules.setdefault("discord.app_commands", _app_commands_stub)

# ── Now import the modules under test ─────────────────────────────────────────
import data  # real module
from cogs.reactionroles import (
    _parse_pairs,
    _parse_pairs_from_string,
    _save_rr,
    _get_rr,
    handle_reaction_add,
    handle_reaction_remove,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════

def _reset_db():
    """Give data module a clean in-memory store."""
    data._db = {"users": {}, "guilds": {}, "reaction_roles": {}}


# ═══════════════════════════════════════════════════════════════════════════════
# 1. _parse_pairs
# ═══════════════════════════════════════════════════════════════════════════════

class TestParsePairs(unittest.TestCase):

    def test_single_pair(self):
        result = _parse_pairs(["🌸", "Soft"])
        self.assertEqual(result, [("🌸", "Soft")])

    def test_multiple_pairs(self):
        result = _parse_pairs(["🌸", "Soft", "🔪", "Killer", "🖤", "Obsessed"])
        self.assertEqual(result, [
            ("🌸", "Soft"),
            ("🔪", "Killer"),
            ("🖤", "Obsessed"),
        ])

    def test_multi_word_role_name(self):
        result = _parse_pairs(["🌸", "Soft", "Kitten", "🔪", "Dark", "Mode"])
        self.assertEqual(result, [
            ("🌸", "Soft Kitten"),
            ("🔪", "Dark Mode"),
        ])

    def test_custom_emoji(self):
        result = _parse_pairs(["<:yandere:123456789>", "VIP"])
        self.assertEqual(result, [("<:yandere:123456789>", "VIP")])

    def test_animated_emoji(self):
        result = _parse_pairs(["<a:sparkle:987654321>", "Sparkler"])
        self.assertEqual(result, [("<a:sparkle:987654321>", "Sparkler")])

    def test_empty_returns_none(self):
        self.assertIsNone(_parse_pairs([]))

    def test_no_emoji_first_returns_none(self):
        self.assertIsNone(_parse_pairs(["Soft", "🌸"]))

    def test_emoji_without_role_returns_none(self):
        self.assertIsNone(_parse_pairs(["🌸"]))

    def test_trailing_emoji_returns_none(self):
        # Valid pair, then a lone emoji with no role after it
        self.assertIsNone(_parse_pairs(["🌸", "Soft", "🔪"]))


class TestParsePairsFromString(unittest.TestCase):

    def test_basic_string(self):
        result = _parse_pairs_from_string("🌸 Soft 🔪 Killer")
        self.assertEqual(result, [("🌸", "Soft"), ("🔪", "Killer")])

    def test_empty_string_returns_none(self):
        self.assertIsNone(_parse_pairs_from_string("   "))

    def test_whitespace_preserved_in_role(self):
        result = _parse_pairs_from_string("🌸 Soft Kitten 🔪 Killer")
        self.assertEqual(result, [("🌸", "Soft Kitten"), ("🔪", "Killer")])


# ═══════════════════════════════════════════════════════════════════════════════
# 2. _save_rr / _get_rr
# ═══════════════════════════════════════════════════════════════════════════════

class TestSaveAndGetRR(unittest.TestCase):

    def setUp(self):
        _reset_db()

    def test_save_and_retrieve(self):
        _save_rr(
            message_id=111,
            guild_id=222,
            channel_id=333,
            role_map={"🌸": 444, "🔪": 555},
        )
        entry = _get_rr(111)
        self.assertIsNotNone(entry)
        self.assertEqual(entry["guild_id"], 222)
        self.assertEqual(entry["channel_id"], 333)
        self.assertEqual(entry["roles"]["🌸"], 444)
        self.assertEqual(entry["roles"]["🔪"], 555)

    def test_get_missing_returns_none(self):
        self.assertIsNone(_get_rr(99999))

    def test_multiple_messages_independent(self):
        _save_rr(1, 10, 20, {"🌸": 100})
        _save_rr(2, 10, 20, {"🔪": 200})
        self.assertEqual(_get_rr(1)["roles"]["🌸"], 100)
        self.assertEqual(_get_rr(2)["roles"]["🔪"], 200)
        self.assertIsNone(_get_rr(1)["roles"].get("🔪"))

    def test_save_persists_to_db_dict(self):
        _save_rr(42, 1, 2, {"🖤": 999})
        self.assertIn("42", data._db["reaction_roles"])


# ═══════════════════════════════════════════════════════════════════════════════
# 3. data module initialises reaction_roles on load
# ═══════════════════════════════════════════════════════════════════════════════

class TestDataInit(unittest.TestCase):

    def test_reaction_roles_key_present_after_reset(self):
        _reset_db()
        self.assertIn("reaction_roles", data._db)
        self.assertIsInstance(data._db["reaction_roles"], dict)

    def test_setdefault_is_idempotent(self):
        _reset_db()
        data._db["reaction_roles"]["existing"] = {"roles": {}}
        # Simulate what load() does
        data._db.setdefault("reaction_roles", {})
        # Must NOT have wiped existing data
        self.assertIn("existing", data._db["reaction_roles"])


# ═══════════════════════════════════════════════════════════════════════════════
# 4. Reaction listeners (async)
# ═══════════════════════════════════════════════════════════════════════════════

def _make_payload(message_id, user_id, guild_id, emoji_str):
    payload = MagicMock()
    payload.message_id = message_id
    payload.user_id = user_id
    payload.guild_id = guild_id
    payload.emoji = MagicMock()
    payload.emoji.__str__ = lambda self: emoji_str
    return payload


def _make_member(user_id):
    m = MagicMock()
    m.id = user_id
    m.add_roles = AsyncMock()
    m.remove_roles = AsyncMock()
    return m


def _make_role(role_id):
    r = MagicMock()
    r.id = role_id
    r.name = f"Role_{role_id}"
    return r


def _make_guild(guild_id, member, role):
    g = MagicMock()
    g.id = guild_id
    g.get_member = MagicMock(return_value=member)
    g.get_role = MagicMock(return_value=role)
    return g


def _make_bot(bot_user_id, guild):
    b = MagicMock()
    b.user = MagicMock()
    b.user.id = bot_user_id
    b.get_guild = MagicMock(return_value=guild)
    return b


class TestReactionListeners(unittest.IsolatedAsyncioTestCase):
    """
    Tests for the extracted handle_reaction_add / handle_reaction_remove
    functions (imported directly — no cog class instantiation needed).
    """

    def setUp(self):
        _reset_db()
        # Seed a known reaction role entry
        _save_rr(
            message_id=9001,
            guild_id=7777,
            channel_id=8888,
            role_map={"🌸": 1001},
        )
        self.role = _make_role(1001)
        self.member = _make_member(user_id=42)
        self.guild = _make_guild(7777, self.member, self.role)
        self.bot = _make_bot(bot_user_id=0, guild=self.guild)

    # ── reaction add ──────────────────────────────────────────────────────────

    async def test_reaction_add_gives_role(self):
        payload = _make_payload(9001, user_id=42, guild_id=7777, emoji_str="🌸")
        await handle_reaction_add(self.bot, payload)
        self.member.add_roles.assert_awaited_once_with(self.role, reason="Reaction role")

    async def test_reaction_add_ignores_bot(self):
        payload = _make_payload(9001, user_id=0, guild_id=7777, emoji_str="🌸")
        await handle_reaction_add(self.bot, payload)
        self.member.add_roles.assert_not_awaited()

    async def test_reaction_add_ignores_unknown_message(self):
        payload = _make_payload(message_id=5555, user_id=42, guild_id=7777, emoji_str="🌸")
        await handle_reaction_add(self.bot, payload)
        self.member.add_roles.assert_not_awaited()

    async def test_reaction_add_ignores_unknown_emoji(self):
        payload = _make_payload(9001, user_id=42, guild_id=7777, emoji_str="💀")
        await handle_reaction_add(self.bot, payload)
        self.member.add_roles.assert_not_awaited()

    async def test_reaction_add_ignores_dm(self):
        payload = _make_payload(9001, user_id=42, guild_id=None, emoji_str="🌸")
        await handle_reaction_add(self.bot, payload)
        self.member.add_roles.assert_not_awaited()

    # ── reaction remove ───────────────────────────────────────────────────────

    async def test_reaction_remove_revokes_role(self):
        payload = _make_payload(9001, user_id=42, guild_id=7777, emoji_str="🌸")
        await handle_reaction_remove(self.bot, payload)
        self.member.remove_roles.assert_awaited_once_with(self.role, reason="Reaction role removed")

    async def test_reaction_remove_ignores_bot(self):
        payload = _make_payload(9001, user_id=0, guild_id=7777, emoji_str="🌸")
        await handle_reaction_remove(self.bot, payload)
        self.member.remove_roles.assert_not_awaited()

    async def test_reaction_remove_ignores_unknown_emoji(self):
        payload = _make_payload(9001, user_id=42, guild_id=7777, emoji_str="🔪")
        await handle_reaction_remove(self.bot, payload)
        self.member.remove_roles.assert_not_awaited()

    async def test_reaction_remove_ignores_dm(self):
        payload = _make_payload(9001, user_id=42, guild_id=None, emoji_str="🌸")
        await handle_reaction_remove(self.bot, payload)
        self.member.remove_roles.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()

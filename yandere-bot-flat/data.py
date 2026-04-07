import json
import logging
from pathlib import Path

logger = logging.getLogger("yandere-bot.data")

DB_FILE = Path(__file__).parent / "data.json"

_DEFAULT_USER: dict = {
    "claimed": None,
    "crush": None,
    "rivals": [],
    "targets": [],
    "obsession_level": 0,
    "sanity": 100,
    "love_level": 0,
    "bonds": [],
    "warnings": [],
    "level": 1,
    "xp": 0,
}

_DEFAULT_GUILD: dict = {
    "blood_mode": False,
    "night_mode": False,
}

_db: dict = {"users": {}, "guilds": {}}


def load() -> None:
    global _db
    if DB_FILE.exists():
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                _db = json.load(f)
            logger.info(
                f"Loaded data.json ({len(_db.get('users', {}))} users, "
                f"{len(_db.get('guilds', {}))} guilds)"
            )
        except Exception as e:
            logger.warning(f"Failed to load data.json: {e}. Starting fresh.")
            _db = {"users": {}, "guilds": {}}
    else:
        logger.info("No data.json found — starting fresh.")
    _db.setdefault("users", {})
    _db.setdefault("guilds", {})
    _db.setdefault("reaction_roles", {})


def save() -> None:
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(_db, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save data.json: {e}")


def get_user(user_id: int) -> dict:
    key = str(user_id)
    if key not in _db["users"]:
        _db["users"][key] = {
            k: list(v) if isinstance(v, list) else v
            for k, v in _DEFAULT_USER.items()
        }
    user = _db["users"][key]
    for k, v in _DEFAULT_USER.items():
        if k not in user:
            user[k] = list(v) if isinstance(v, list) else v
    return user


def set_user(user_id: int, **kwargs) -> None:
    user = get_user(user_id)
    user.update(kwargs)
    save()


def get_guild(guild_id: int) -> dict:
    key = str(guild_id)
    if key not in _db["guilds"]:
        _db["guilds"][key] = dict(_DEFAULT_GUILD)
    guild = _db["guilds"][key]
    for k, v in _DEFAULT_GUILD.items():
        if k not in guild:
            guild[k] = v
    return guild


def set_guild(guild_id: int, **kwargs) -> None:
    guild = get_guild(guild_id)
    guild.update(kwargs)
    save()


# ── XP / Leveling ─────────────────────────────────────────────────────────────

def gain_xp(user_id: int, amount: int) -> dict | None:
    """
    Award XP. Returns level-up info dict if one or more levels were gained,
    otherwise returns None.
    Format: {"new_level": int, "new_xp": int}
    """
    user = get_user(user_id)
    user["xp"] += amount
    leveled_up = False
    while user["xp"] >= 100:
        user["xp"] -= 100
        user["level"] += 1
        leveled_up = True
        user["obsession_level"] = min(100, user["obsession_level"] + 5)
        user["sanity"] = max(0, user["sanity"] - 3)
    save()
    if leveled_up:
        return {"new_level": user["level"], "new_xp": user["xp"]}
    return None


LEVELUP_LINES = [
    "Your feelings are growing stronger… you can't stop now. 🔪",
    "Something has shifted inside you. You can feel it. 💉",
    "The obsession deepens. You don't even try to fight it anymore. 🌸",
    "Level {level}. The devotion is consuming everything. 🩸",
    "You've crossed another threshold. There's no going back. 👁️",
]


def levelup_text(level: int) -> str:
    line = LEVELUP_LINES[level % len(LEVELUP_LINES)].replace("{level}", str(level))
    return line


# ── Sanity / Obsession helpers ─────────────────────────────────────────────────

def get_love(user_id: int) -> int:
    return get_user(user_id)["love_level"]


def get_obsession(user_id: int) -> int:
    return get_user(user_id)["obsession_level"]


def get_sanity(user_id: int) -> int:
    return get_user(user_id)["sanity"]


def get_level(user_id: int) -> int:
    return get_user(user_id)["level"]


def get_xp(user_id: int) -> int:
    return get_user(user_id)["xp"]


def sanity_tone(user_id: int) -> str:
    """Returns the personality tone based on sanity level."""
    s = get_sanity(user_id)
    if s >= 70:
        return "sweet"      # calm, loving, warm
    if s >= 40:
        return "possessive"  # jealous, clingy, intense
    return "unhinged"       # threatening, glitchy, erratic


def level_intensity(user_id: int) -> str:
    """Returns response intensity based on XP level."""
    lv = get_level(user_id)
    if lv >= 10:
        return "extreme"
    if lv >= 7:
        return "high"
    if lv >= 4:
        return "medium"
    return "low"


def obsession_intensity(level: int) -> str:
    if level >= 90:
        return "critical"
    if level >= 70:
        return "high"
    if level >= 40:
        return "medium"
    return "low"


def sanity_state(level: int) -> str:
    if level >= 70:
        return "stable"
    if level >= 40:
        return "cracking"
    if level >= 20:
        return "unstable"
    return "broken"


def love_bar(level: int) -> str:
    filled = round(level / 10)
    return "💕" * filled + "🖤" * (10 - filled)


def sanity_bar(level: int) -> str:
    filled = round(level / 10)
    return "🌸" * filled + "🩸" * (10 - filled)


def xp_bar(xp: int) -> str:
    filled = round(xp / 10)
    return "⬛" * filled + "░" * (10 - filled)

import discord
from discord.ext import commands
from discord import app_commands
import random
import data

PINK = 0xffb6c1
RED = 0x8b0000
BLACK = 0x0d0d0d

COOLDOWN_MSG = "🌸 *Patience... wait {:.0f}s before doing that again. 💕*"


def _obsession_color(level: int) -> int:
    if level >= 70:
        return RED
    if level >= 40:
        return PINK
    return PINK


def _claim_msg(claimer: discord.Member, target: discord.Member, obsession: int, already_claimed: bool, same_person: bool) -> str:
    if same_person:
        if obsession >= 70:
            return f"*{claimer.mention} tightens their grip.* 🔪\n*\"They were already mine. They've always been mine. Don't forget that. 💕\"*"
        return f"🌸 *{target.mention} is already yours, {claimer.mention}. You claimed them first. 💕*"
    if already_claimed:
        if obsession >= 70:
            return f"*{claimer.mention}'s smile doesn't reach their eyes.* 🔪\n*\"Replacing one claim with another... I'm not sure that's healthy. But here we are. {target.mention} is mine now.\"*"
        return f"*{claimer.mention} releases their old claim and reaches for {target.mention} instead.*\n🌸 *\"You. It's always been you. 💕\"*"
    if obsession >= 90:
        return f"*{claimer.mention} steps forward, eyes fixed on {target.mention}.* 🔪\n*\"Mine. That wasn't a question. 💕\"*"
    if obsession >= 60:
        return f"*{claimer.mention} reaches out and takes {target.mention}'s hand, firmly.*\n🌸 *\"You're mine now. I'll be very good to you. As long as you behave. 💕\"*"
    return f"*{claimer.mention} smiles warmly at {target.mention}.*\n🌸 *\"You're mine now. Don't worry — I mean that in the best possible way. 💕\"*"


def _obsess_msg(level: int) -> str:
    if level >= 95:
        return "🔪 *There is nothing left. Only them. Only this. This is all there is now.*"
    if level >= 80:
        return "🩸 *The fixation has become something else entirely. Something permanent. Something consuming.*"
    if level >= 60:
        return "💉 *Every thought ends with their name. You're past the point of pretending this is normal.*"
    if level >= 40:
        return "👁️ *It's growing. You can feel it. Warm and heavy and impossible to ignore.*"
    return "🌸 *A small, sweet fixation. Harmless. Probably. 💕*"


def _forget_msg(obsession: int) -> str:
    if obsession >= 80:
        return "🔪 *Forget? You can't forget. You've tried. The thoughts always come back. Louder each time.*"
    if obsession >= 50:
        return "🩸 *You try. You almost manage it. Then something reminds you again and it all floods back.*"
    return "🌸 *You let go a little. Just a little. It helps. For now.*"


class Relationship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                COOLDOWN_MSG.format(error.retry_after), ephemeral=True
            )

    @app_commands.command(name="claim", description="Claim someone as yours. 💕")
    @app_commands.describe(user="The one you're claiming")
    @app_commands.checks.cooldown(1, 15.0)
    async def claim(self, interaction: discord.Interaction, user: discord.Member):
        if user.id == interaction.user.id:
            await interaction.response.send_message("🌸 *You can't claim yourself, silly.*", ephemeral=True)
            return
        uid = interaction.user.id
        profile = data.get_user(uid)
        old_claim = profile["claimed"]
        same_person = old_claim == str(user.id)
        already_claimed = old_claim is not None and not same_person
        obsession = profile["obsession_level"]

        data.set_user(uid,
            claimed=str(user.id),
            love_level=min(100, profile["love_level"] + 20),
            obsession_level=min(100, obsession + 5),
        )

        msg = _claim_msg(interaction.user, user, obsession, already_claimed, same_person)
        color = _obsession_color(data.get_obsession(uid))
        lu = data.gain_xp(uid, 30)
        lv = data.get_level(uid)
        embed = discord.Embed(title="💕 CLAIMED", description=msg, color=color)
        embed.add_field(name="📊 Stats", value=f"Level `{lv}` · Obsession `{data.get_obsession(uid)}/100`", inline=True)
        embed.set_footer(text="Mine. Only mine. 🔪")
        if lu:
            embed.add_field(
                name=f"🆙 LEVEL {lu['new_level']} REACHED",
                value=f"*{data.levelup_text(lu['new_level'])}*\n`XP: {lu['new_xp']}/100`",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unclaim", description="Release someone. If you really want to. 🖤")
    @app_commands.describe(user="Who to release")
    async def unclaim(self, interaction: discord.Interaction, user: discord.Member):
        profile = data.get_user(interaction.user.id)
        if profile["claimed"] == str(user.id):
            data.set_user(interaction.user.id, claimed=None)
            embed = discord.Embed(
                description=f"🖤 *{interaction.user.mention} released {user.mention}...*\n*Why? Why would you let go? Are you okay?*",
                color=BLACK
            )
        else:
            embed = discord.Embed(description="🌸 *They were never yours to release.*", color=PINK)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="lovelevel", description="Check love level. 💕")
    @app_commands.describe(user="Who to check")
    async def lovelevel(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        level = data.get_love(target.id)
        bar = data.love_bar(level)
        if level >= 80:
            desc = "🔪 *Dangerously devoted. This has crossed several lines.*"
        elif level >= 50:
            desc = "💕 *Deep and growing. There's no coming back from this.*"
        elif level >= 20:
            desc = "🌸 *It's there. It's real. It's only getting stronger.*"
        else:
            desc = "💕 *Just getting started. 🌸*"
        embed = discord.Embed(
            title=f"💕 Love Level — {target.display_name}",
            description=f"{bar}\n**{level}/100**\n\n{desc}",
            color=_obsession_color(level)
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="crush", description="Confess your crush. 🌸")
    @app_commands.describe(user="Your crush")
    @app_commands.checks.cooldown(1, 20.0)
    async def crush(self, interaction: discord.Interaction, user: discord.Member):
        profile = data.get_user(interaction.user.id)
        old_crush = profile["crush"]
        data.set_user(interaction.user.id, crush=str(user.id))

        if old_crush and old_crush != str(user.id):
            desc = f"*{interaction.user.mention} quietly lets go of their previous feelings and turns to {user.mention}.*\n\n🌸 *\"It was always supposed to be you. I see that now. 💕\"*"
        elif old_crush == str(user.id):
            desc = f"🌸 *{interaction.user.mention} is still crushing on {user.mention}. Hard.*\n*\"Nothing has changed. Nothing will change. 💕\"*"
        else:
            desc = f"🌸 *{interaction.user.mention} has developed feelings for {user.mention}...*\n*How sweet. How delicate. How fragile. 💕*"

        embed = discord.Embed(description=desc, color=PINK)
        embed.set_footer(text="Guard it carefully. 🔪")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="uncrush", description="Try to move on. Good luck. 🖤")
    @app_commands.describe(user="Who you're trying to forget")
    async def uncrush(self, interaction: discord.Interaction, user: discord.Member):
        profile = data.get_user(interaction.user.id)
        if profile["crush"] == str(user.id):
            data.set_user(interaction.user.id, crush=None)
        embed = discord.Embed(
            description=f"🖤 *{interaction.user.mention} is trying to forget {user.mention}...*\n\n*You can try. You won't fully succeed. The heart remembers everything.*",
            color=BLACK
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="relationship", description="Check your relationship status. 💕")
    @app_commands.describe(user="Who to check with")
    async def relationship(self, interaction: discord.Interaction, user: discord.Member = None):
        profile = data.get_user(interaction.user.id)
        claimed = profile["claimed"]
        crush = profile["crush"]
        bonds = profile["bonds"]
        obsession = profile["obsession_level"]
        sanity = profile["sanity"]

        if claimed:
            status = f"💕 Claimed: <@{claimed}>"
        elif crush:
            status = f"🌸 Crushing on: <@{crush}>"
        else:
            status = "💔 Alone... for now."

        bond_str = ", ".join(f"<@{b}>" for b in bonds[:5]) if bonds else "*No bonds formed yet.*"

        embed = discord.Embed(title=f"💕 Profile — {interaction.user.display_name}", color=PINK)
        embed.add_field(name="💖 Status", value=status, inline=False)
        embed.add_field(name="🔗 Bonds", value=bond_str, inline=False)
        embed.add_field(name="💉 Obsession", value=f"`{obsession}/100`", inline=True)
        embed.add_field(name="🩸 Sanity", value=f"`{sanity}/100`", inline=True)
        embed.set_footer(text="Love is eternal. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="jealous", description="Show jealousy toward someone. 🔪")
    @app_commands.describe(user="The one making you jealous")
    async def jealous(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        profile = data.get_user(uid)
        new_sanity = max(0, profile["sanity"] - 5)
        data.set_user(uid, sanity=new_sanity)
        obsession = data.get_obsession(interaction.user.id)
        if obsession >= 80:
            responses = [
                f"*{interaction.user.mention}'s expression goes completely blank.* 🔪\n*\"Step. Away. From. Them. I'm still smiling. See? Still smiling.\"*",
                f"*{interaction.user.mention} grips the edge of the table.* 🩸\n*\"You don't understand what you're doing. Going near them. Smiling at them. You have no idea. 🔪\"*",
            ]
        elif obsession >= 50:
            responses = [
                f"*{interaction.user.mention} stares at {user.mention} with a warm, fixed smile.* 🌸\n*\"Stay away from them. I mean it. 💕\"*",
                f"*{interaction.user.mention}'s hands tighten.* 🔪\n*\"Talking to them again. I noticed. I always notice.\"*",
            ]
        else:
            responses = [
                f"*{interaction.user.mention} tilts their head at {user.mention}.*\n*\"You're not a threat. You're just... in the way. 🌸\"*",
                f"*{interaction.user.mention} watches {user.mention} carefully.*\n*\"I'm keeping an eye on you. Just in case. 💕\"*",
            ]
        embed = discord.Embed(description=random.choice(responses), color=RED if obsession >= 70 else PINK)
        embed.set_footer(text="Jealousy is just love with nowhere to go. 💕")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="devotion", description="Show your devotion level. 💕")
    @app_commands.describe(user="Who you're devoted to")
    async def devotion(self, interaction: discord.Interaction, user: discord.Member):
        love = data.get_love(interaction.user.id)
        obsession = data.get_obsession(interaction.user.id)
        combined = min(100, (love + obsession) // 2)
        if combined >= 85:
            desc = "🔪 *Absolute. Permanent. Beyond reason.*"
        elif combined >= 65:
            desc = "🌸 *Deep, unwavering, and slightly terrifying.*"
        else:
            desc = "💕 *Strong and growing. Always growing.*"
        embed = discord.Embed(
            title="💕 Devotion Level",
            description=f"*{interaction.user.mention} → {user.mention}*\n\n**{combined}%** {desc}",
            color=_obsession_color(combined)
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="attention", description="Beg for attention. 🌸")
    @app_commands.describe(user="Who you want attention from")
    @app_commands.checks.cooldown(1, 30.0)
    async def attention(self, interaction: discord.Interaction, user: discord.Member):
        sanity = data.get_sanity(interaction.user.id)
        if sanity <= 30:
            msg = f"*{interaction.user.mention} appears suddenly, eyes wide.* 🩸\n*\"Look at me. LOOK AT ME. You haven't talked to me in hours. Do you understand what that does to me? 🔪\"*"
        elif sanity <= 60:
            msg = f"*{interaction.user.mention} tugs on {user.mention}'s sleeve, a little too hard.* 🌸\n*\"Please. Just... look at me. Say something. Please. 💕\"*"
        else:
            msg = f"*{interaction.user.mention} tugs on {user.mention}'s sleeve.* 🌸\n*\"Look at me. Please. Just for a second. 💕\"*"
        embed = discord.Embed(description=msg, color=PINK if sanity > 60 else RED)
        embed.set_footer(text="Notice me. 🌸")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="obsession", description="Check obsession level. 💉")
    @app_commands.describe(user="Who you're obsessed with")
    async def obsession(self, interaction: discord.Interaction, user: discord.Member):
        level = data.get_obsession(interaction.user.id)
        bar = data.love_bar(level)
        desc = _obsess_msg(level)
        embed = discord.Embed(
            title=f"💉 Obsession — {user.display_name}",
            description=f"{bar}\n**{level}/100**\n\n{desc}",
            color=_obsession_color(level)
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="obsess", description="Feed the obsession. 💉")
    @app_commands.checks.cooldown(1, 20.0)
    async def obsess(self, interaction: discord.Interaction):
        uid = interaction.user.id
        profile = data.get_user(uid)
        bump = random.randint(5, 15)
        new_obs = min(100, profile["obsession_level"] + bump)
        new_sanity = max(0, profile["sanity"] - random.randint(1, 4))
        data.set_user(uid, obsession_level=new_obs, sanity=new_sanity)

        desc = _obsess_msg(new_obs)
        lu = data.gain_xp(uid, 20)
        embed = discord.Embed(
            description=f"💉 *The feeling grows...*\n\n**Obsession:** `{new_obs}/100` (+{bump})\n**Sanity:** `{new_sanity}/100`\n\n{desc}",
            color=_obsession_color(new_obs)
        )
        if lu:
            embed.add_field(
                name=f"🆙 LEVEL {lu['new_level']} REACHED",
                value=f"*{data.levelup_text(lu['new_level'])}*\n`XP: {lu['new_xp']}/100`",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="forget", description="Try to forget someone. 🖤")
    @app_commands.describe(user="Who to forget")
    @app_commands.checks.cooldown(1, 30.0)
    async def forget(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        profile = data.get_user(uid)
        current = profile["obsession_level"]
        drop = random.randint(5, 15) if current < 70 else random.randint(1, 5)
        new_obs = max(0, current - drop)
        data.set_user(uid, obsession_level=new_obs)

        desc = _forget_msg(current)
        embed = discord.Embed(
            description=f"🖤 *{interaction.user.mention} tries to forget {user.mention}...*\n\n**Obsession:** `{current}/100` → `{new_obs}/100`\n\n{desc}",
            color=BLACK
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remember", description="Let the obsession return. 💉")
    @app_commands.describe(user="Who to remember")
    @app_commands.checks.cooldown(1, 20.0)
    async def remember(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        profile = data.get_user(uid)
        bump = random.randint(15, 30)
        new_obs = min(100, profile["obsession_level"] + bump)
        new_sanity = max(0, profile["sanity"] - random.randint(2, 6))
        data.set_user(uid, obsession_level=new_obs, sanity=new_sanity)
        lu = data.gain_xp(uid, 10)
        embed = discord.Embed(
            description=f"💉 *{interaction.user.mention} remembers {user.mention}...*\n\n*Every detail. Every smile. Every word. It all floods back.*\n\n**Obsession:** `{new_obs}/100` 🌸",
            color=RED
        )
        if lu:
            embed.add_field(
                name=f"🆙 LEVEL {lu['new_level']} REACHED",
                value=f"*{data.levelup_text(lu['new_level'])}*\n`XP: {lu['new_xp']}/100`",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bond", description="Form an unbreakable bond. 🔗")
    @app_commands.describe(user="Who to bond with")
    @app_commands.checks.cooldown(1, 30.0)
    async def bond(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        profile = data.get_user(uid)
        bonds = profile["bonds"]
        uid_str = str(user.id)
        if uid_str in bonds:
            embed = discord.Embed(
                description=f"🔗 *The bond with {user.mention} already exists.*\n*You can't form what's already there. 🌸*",
                color=PINK
            )
        else:
            bonds.append(uid_str)
            data.set_user(uid, bonds=bonds)
            lu = data.gain_xp(uid, 20)
            embed = discord.Embed(
                title="🔗 BOND FORMED",
                description=f"*{interaction.user.mention} and {user.mention} are now bound together.*\n\n🌸 *This is permanent. I hope you understand that. 💕*",
                color=PINK
            )
            if lu:
                embed.add_field(
                    name=f"🆙 LEVEL {lu['new_level']} REACHED",
                    value=f"*{data.levelup_text(lu['new_level'])}*\n`XP: {lu['new_xp']}/100`",
                    inline=False
                )
        embed.set_footer(text="Bonds don't break. 🔪")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="breakbond", description="Sever the bond. If you dare. 🖤")
    @app_commands.describe(user="Who to break from")
    async def breakbond(self, interaction: discord.Interaction, user: discord.Member):
        uid = interaction.user.id
        profile = data.get_user(uid)
        bonds = profile["bonds"]
        uid_str = str(user.id)
        if uid_str in bonds:
            bonds.remove(uid_str)
            data.set_user(uid, bonds=bonds)
        embed = discord.Embed(
            description=f"🖤 *The bond between {interaction.user.mention} and {user.mention} has been severed.*\n\n*Something is bleeding. Not physically. But something. 🩸*",
            color=BLACK
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Relationship(bot))

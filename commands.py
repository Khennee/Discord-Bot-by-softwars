import random
import time
import discord
from discord.ext import commands
from database import Database
from helpers import check_and_reset_season

db = Database()

cooldowns = {}
COOLDOWN_SECONDS = 600  # 10 minutes


class TraydorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print(f"{self.bot.user} Online.")

    @discord.app_commands.command(name="hello", description="Test if the bot is alive")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Traydor")

    @discord.app_commands.command(
        name="addtraydor",
        description="Randomly add 1–5 Traydor points to a user (10min cooldown)"
    )
    async def addtraydor(self, interaction: discord.Interaction, member: discord.Member):
        try:
            await interaction.response.defer(thinking=True)  # ⏳ prevents timeout

            giver_id = interaction.user.id
            target_id = member.id
            key = (giver_id, target_id)
            now = time.time()

            if giver_id == target_id:
                await interaction.followup.send(
                    "❌ You can’t add Traydor points to yourself!",
                    ephemeral=True
                )
                return

            if key in cooldowns and now - cooldowns[key] < COOLDOWN_SECONDS:
                remaining = int(COOLDOWN_SECONDS - (now - cooldowns[key]))
                minutes = remaining // 60
                seconds = remaining % 60
                await interaction.followup.send(
                    f"⏳ You must wait `{minutes:02}:{seconds:02}` before adding points to {member.display_name} again.",
                    ephemeral=True
                )
                return

            points = random.randint(1, 5)
            total = db.add_points(str(member.id), member.display_name, points)
            cooldowns[key] = now

            await interaction.followup.send(
                f"✅ {interaction.user.display_name} gave **{points}** random Traydor points to {member.display_name}! 🎲\n"
                f"🏅 {member.display_name} now has **{total}** points."
            )

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error: {e}", ephemeral=True)

    @discord.app_commands.command(name="leaderboards", description="Show the top players for this season")
    async def leaderboards(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(thinking=True)

            season_number, days_left = check_and_reset_season()
            top = db.get_top(10)

            if not top:
                await interaction.followup.send(
                    f"📅 Season {season_number}\nNo players yet. Resets in {days_left} days."
                )
                return

            embed = discord.Embed(title=f"🏆 Season {season_number} Leaderboards 🏆")
            embed.set_footer(text=f"⏳ Resets in {days_left} days")

            for i, (username, score) in enumerate(top, start=1):
                name = f"{i}. {username}"
                value = f"{score} Traydor points"
                if i == 1:
                    embed.add_field(name=f"🔥 {name} (Top 1)", value=value, inline=False)
                    embed.color = discord.Color.red()
                elif i == 2:
                    embed.add_field(name=f"⚡ {name} (Top 2)", value=value, inline=False)
                    embed.color = discord.Color.orange()
                elif i == 3:
                    embed.add_field(name=f"⭐ {name} (Top 3)", value=value, inline=False)
                    embed.color = discord.Color.gold()
                else:
                    embed.add_field(name=name, value=value, inline=False)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error: {e}", ephemeral=True)

    @discord.app_commands.command(name="checktraydor", description="Check a user's Traydor points")
    async def checktraydor(self, interaction: discord.Interaction, member: discord.Member):
        season_number, days_left = check_and_reset_season()
        points = db.get_points(str(member.id))
        await interaction.response.send_message(
            f"{member.display_name} has `{points}` Traydor points in Season {season_number}.\n"
            f"⏳ Resets in {days_left} days."
        )

    @discord.app_commands.command(name="helpme", description="Show all available commands")
    async def helpme(self, interaction: discord.Interaction):
        help_text = (
            "**🤖 Traydor Bot Commands:**\n\n"
            "🔹 `/hello` → Test if the bot is alive\n"
            "🔹 `/addtraydor @user` → Randomly add 1–5 points (10min cooldown)\n"
            "🔹 `/checktraydor @user` → Check a user’s points\n"
            "🔹 `/leaderboards` → Show season leaderboards\n"
            "🔹 `/helpme` → Show this help message\n\n"
            "📅 Seasons reset **monthly** — all points go back to `0` at reset."
        )

        embed = discord.Embed(
            title="📖 Traydor Bot Help",
            description=help_text,
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(
        name="pingtraydors",
        description="Ping everyone and require them to press Join within 5 minutes or get points"
    )
    async def pingtraydors(self, interaction: discord.Interaction):
        try:
            OWNER_ID = 640054746560069634
            if interaction.user.id != OWNER_ID:
                await interaction.response.send_message(
                    "❌ You are not authorized to use this command.",
                    ephemeral=True
                )
                return

            await interaction.response.defer(thinking=True)

            guild = interaction.guild
            if guild is None:
                await interaction.followup.send("❌ This command can only be used in a server.")
                return

            members = [m for m in guild.members if not m.bot]  # exclude bots
            if not members:
                await interaction.followup.send("❌ No members found in this server.")
                return

            joined = set()

            class JoinView(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=300)  # 5 minutes

                @discord.ui.button(label="Join", style=discord.ButtonStyle.success)
                async def join_button(self, interaction_btn: discord.Interaction, button: discord.ui.Button):
                    user = interaction_btn.user
                    joined.add(user.id)
                    await interaction_btn.response.send_message(
                        f"✅ {user.display_name} joined in time!", ephemeral=True
                    )

            view = JoinView()

            # Send the message with @everyone ping
            await interaction.followup.send(
                content=(
                    f"🚨 **Attention @everyone!**\n"
                    f"You have **5 minutes** to press the **Join** button below "
                    f"or you will receive Traydor points! 👇"
                ),
                allowed_mentions=discord.AllowedMentions(everyone=True),
                view=view
            )

            # Wait until the 5-minute window expires
            await view.wait()

            # Process members who failed to join
            failed = [m for m in members if m.id not in joined]

            if not failed:
                await interaction.followup.send("🎉 Everyone pressed **Join** in time! No Traydor points given.")
                return

            results = []
            for member in failed:
                points = random.randint(1, 5)
                total = db.add_points(str(member.id), member.display_name, points)
                results.append(f"❌ {member.display_name} failed and got **{points}** points (now {total}).")

            await interaction.followup.send("\n".join(results))

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error: {e}", ephemeral=True)

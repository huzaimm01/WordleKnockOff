import discord
from discord import app_commands
from discord.ext import commands
from core.data import load_json

class Board(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leaderboard", description="View the leaderboard.")
    async def leaderboard(self, interaction: discord.Interaction):
        scores = load_json("data/scores.json")
        tally = []

        for uid, results in scores.items():
            user = await self.bot.fetch_user(int(uid))
            tally.append((user.name, len(results)))

        tally.sort(key=lambda x: x[1], reverse=True)
        msg = "\n".join([f"{i+1}. {name} — {score}" for i, (name, score) in enumerate(tally[:10])])
        await interaction.response.send_message(f"🏆 Leaderboard:\n{msg}")

async def setup(bot):
    await bot.add_cog(Board(bot))

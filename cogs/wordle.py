import discord
from discord import app_commands
from discord.ext import commands
from core.daily_game import get_daily_words
from core.engine import evaluate_guess
from core.data import load_json, save_json

class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    @app_commands.command(name="play", description="Start the daily Wordle puzzles.")
    async def play(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        daily = get_daily_words()
        scores = load_json("data/scores.json")

        if user_id not in scores:
            scores[user_id] = []

        self.active_games[user_id] = {
            "answers": daily,
            "current_index": 0,
            "guesses": []
        }

        await interaction.response.send_message(f"Puzzle 1/{len(daily)} — Guess a {len(daily[0])}-letter word.")

    @app_commands.command(name="guess", description="Make a guess.")
    @app_commands.describe(word="Your guessed word.")
    async def guess(self, interaction: discord.Interaction, word: str):
        user_id = str(interaction.user.id)
        game = self.active_games.get(user_id)

        if not game:
            await interaction.response.send_message("Start a game first using /play.")
            return

        answer = game["answers"][game["current_index"]]
        result = evaluate_guess(word.lower(), answer.lower())
        game["guesses"].append((word, result))

        output = ""
        for guess, res in game["guesses"]:
            display = ""
            for i in range(len(guess)):
                color = res[i]
                letter = guess[i]
                emoji = {
                    "green": "🟩",
                    "yellow": "🟨",
                    "gray": "⬜"
                }.get(color, "⬜")
                display += emoji
            output += f"`{guess}` {display}\n"

        if word.lower() == answer.lower():
            game["current_index"] += 1
            game["guesses"] = []
            if game["current_index"] >= len(game["answers"]):
                scores = load_json("data/scores.json")
                if user_id not in scores:
                    scores[user_id] = []
                scores[user_id].append("✅")
                save_json("data/scores.json", scores)
                self.active_games.pop(user_id)
                await interaction.response.send_message(output + "\nAll puzzles complete!")
            else:
                await interaction.response.send_message(output + f"\nCorrect! Next puzzle: {len(answer)} letters.")
        else:
            await interaction.response.send_message(output)

async def setup(bot):
    await bot.add_cog(Wordle(bot))

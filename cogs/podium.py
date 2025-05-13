import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from core.data import load_json

class Podium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="podium", description="Generate the podium graphic.")
    async def podium(self, interaction: discord.Interaction):
        scores = load_json("data/scores.json")
        top = sorted(scores.items(), key=lambda x: len(x[1]), reverse=True)[:3]

        base = Image.open("assets/podium.png")
        draw = ImageDraw.Draw(base)
        font = ImageFont.truetype("arial.ttf", 32)

        positions = [(150, 250), (400, 200), (650, 275)]

        for i, (uid, _) in enumerate(top):
            user = await self.bot.fetch_user(int(uid))
            name = user.name
            draw.text(positions[i], name, fill="black", font=font)

        base.save("assets/generated_podium.png")
        file = discord.File("assets/generated_podium.png", filename="podium.png")
        await interaction.response.send_message("🏁 Podium:", file=file)

async def setup(bot):
    await bot.add_cog(Podium(bot))

import discord
from discord.ext import commands
from commands import TraydorCommands
import os
from dotenv import load_dotenv  

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    await bot.add_cog(TraydorCommands(bot))
    await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from core.generate import summarise
from core.scrape import scrape_articles
from core.supabase import upload
from datetime import date
import asyncio

load_dotenv()

# Discord Bot setup
bot_token = os.environ.get("DISCORD_BOT_TOKEN")
channel_id = os.environ.get("DISCORD_CHANNEL_ID")

# Create and set up intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def send_to_discord(content):

    channel = bot.get_channel(int(channel_id))

    if channel:
        for article in content["articles"]:
            embed = discord.Embed(title=article['revised_title'], description=article['Summary'], color=0x00ff00)
            await channel.send(embed=embed)
    else:
        print(f"Channel with ID {channel_id} not found.")

async def process(date_input):
    content = await asyncio.to_thread(scrape_articles, date_input)
    summarised_content = await asyncio.to_thread(summarise, content)
    return summarised_content

async def job():
    date_input = str(date.today())

    print(f"Job started at {date_input}")

    try:
        content = await process(date_input)

        print("Content Summarisation Completed")

        await asyncio.gather(
            asyncio.to_thread(upload, content, date_input),
            send_to_discord(content)
        )

        print(f"Job completed at {date_input}")
    except Exception as e:
        print(f"An error occurred x: : {e}")

    print("Scheduling next job in 1 hour...")
    await asyncio.sleep(3600)
    asyncio.ensure_future(job())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    
    # Schedule initial job
    asyncio.ensure_future(job())

# Start the bot
bot.run(bot_token)

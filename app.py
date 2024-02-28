import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from core.generate import summarise
from core.scrape import scrape_articles
from core.supabase import upload
from datetime import date
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Discord Bot setup
bot_token = os.environ.get("DISCORD_BOT_TOKEN")
channel_id = os.environ.get("DISCORD_CHANNEL_ID")

# Create and set up intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def send_to_discord(content):
    channel_iid = int(channel_id)
    channel = bot.get_channel(channel_iid)
    if channel:
        for article in content["articles"]:
            embed = discord.Embed(
                title=article['revised_title'],
                description=article['Summary'],
                color=0x00ff00
            )
            embed.set_image(url=article['image_links'][0])  # Set the image with the first image link
            embed.add_field(name="Article Link", value=article['link'], inline=False)
            await channel.send(embed=embed)
    else:
        logger.error(f"Channel with ID {channel_id} not found.")

async def process(date_input):
    content = await asyncio.to_thread(scrape_articles, date_input)
    summarised_content = await asyncio.to_thread(summarise, content)
    return summarised_content

async def job():
    date_input = str(date.today())
    
    try:
        content = await process(date_input)

        logger.info("1/3 : Content Summarisation Completed")

        await send_to_discord(content)
        logger.info("2/3 : Message sent to Discord")

        await asyncio.to_thread(upload, content, date_input)
        logger.info("3/3: JSON File uploaded")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        logger.error("Job Stopped!")

    for _ in range(6):  # Run this loop 6 times (every 10 minutes for 1 hour)
        logger.info(f"Time remaining for the next job: {10 * (_ + 1)} minutes")
        await asyncio.sleep(600)  # Sleep for 10 minutes

    logger.info("Scheduling next job in 1 hour...")
    asyncio.ensure_future(job())

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    
    # Schedule initial job
    asyncio.ensure_future(job())

# Start the bot
bot.run(bot_token)
import asyncio
import io
import logging
import os
from datetime import datetime

import aiohttp
import discord
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

logging.basicConfig(level=logging.INFO)

DISCORD_TOKEN = os.getenv("DISCORD_API_KEY")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Image resize dimensions
MAX_WIDTH = 400
MAX_HEIGHT = 300

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
client = discord.Client(intents=intents)

async def download_image(session, url):
    """Downloads an image from the given URL."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                logging.warning(f"Failed to download image from {url}. Status: {response.status}")
                return None
    except aiohttp.ClientError as e:
        logging.error(f"Error downloading image from {url}: {e}")
        return None

def resize_image(image_data):
    """Resizes an image to the specified dimensions."""
    try:
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((MAX_WIDTH, MAX_HEIGHT))
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        buffered.seek(0)
        return buffered
    except Exception as e:
        logging.error(f"Error resizing image: {e}")
        return None

def create_news_embed(article):
    """Creates a Discord embed for a news article."""
    try:
        embed = discord.Embed(
            title=article.get('revised_title', 'No Title'),
            description=article.get('Summary', 'No summary available.'),
            color=0x00AAFF,  
            url=article.get('link', 'https://techcrunch.com')
        )

        if article.get('image_links'):
            embed.set_thumbnail(url=article['image_links'])
            
        embed.set_footer(text="Powered by MassCoders | News Agent \t\t\t\t\t TechCrunch")

        return embed
    except Exception as e:
        logging.error(f"Error creating news embed: {e}")
        return None

async def send_technews(articles):
    """Sends tech news to the Discord channel."""
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        logging.error(f"Channel with ID {CHANNEL_ID} not found.")
        return

    async with aiohttp.ClientSession() as session:
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            header = f"## NewsAgent Daily Digest - {today}\n"
            await channel.send(header)

            for index, article in enumerate(articles, 1):
                embed = create_news_embed(article)
                if embed:
                    await channel.send(embed=embed)
                else:
                    logging.warning(f"Skipping article due to error creating embed: {article}")
                if index < len(articles):
                    await channel.send("---")

            # await channel.send("🔔 Stay tuned for more tech insights tomorrow! 🌐")

        except Exception as e:
            logging.error(f"An error occurred while sending tech news: {e}")
        finally:
            await client.close()

def start_discord_bot(articles):
    @client.event
    async def on_ready():
        logging.info(f"{client.user.name} has connected to Discord!")
        await send_technews(articles)

    try:
        client.run(DISCORD_TOKEN)
    except discord.LoginFailure as e:
        logging.critical(f"Failed to log in to Discord: {e}")
import discord
import logging
import os
import asyncio
from dotenv import load_dotenv
import aiohttp
import io
from PIL import Image
from datetime import datetime

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
    async with session.get(url) as response:
        if response.status == 200:
            return await response.read()
        else:
            logging.warning(f"Failed to download image from {url}. Status: {response.status}")
            return None

def resize_image(image_data):
    """Resizes an image to the specified dimensions."""
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail((MAX_WIDTH, MAX_HEIGHT))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    return buffered

def create_news_embed(article):
    """Creates a Discord embed for a news article."""
    embed = discord.Embed(
        title=article.get('revised_title', 'No Title'),
        description=article.get('Summary', 'No summary available.'),
        color=0x00AAFF,  
        url=article.get('link', 'https://techcrunch.com')
    )

    if article.get('image_links'):
        embed.set_thumbnail(url=article['image_links'])

    embed.add_field(name="Read Full Article", value=f"[Click here]({article.get('link', 'https://techcrunch.com')})", inline=True)
    embed.add_field(name="Source", value="TechCrunch", inline=True)
    embed.set_footer(text="Powered by MassCoders | News Agent")

    return embed

async def send_technews(articles):
    """Sends tech news to the Discord channel."""
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        logging.error(f"Channel with ID {CHANNEL_ID} not found.")
        return
    async with aiohttp.ClientSession() as session:
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            header = "## TechCrunch Daily Digest #001\n"
            header_1 = f"📅 Date: {today}\n"
            await channel.send(header)
            await channel.send(header_1)
            for index, article in enumerate(articles, 1):
                embed = create_news_embed(article)
                await channel.send(embed=embed)
                if index < len(articles):
                    await channel.send("---")
            await channel.send("🔔 Stay tuned for more tech insights tomorrow! 🌐")
        finally:
            await session.close()

def start_discord_bot(articles):
    @client.event
    async def on_ready():
        logging.info(f"{client.user.name} has connected to Discord!")
        await send_technews(articles)


    client.run(DISCORD_TOKEN)


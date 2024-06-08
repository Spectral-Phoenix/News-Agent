import discord
import logging
import json
import os
from dotenv import load_dotenv
import aiohttp
import io
from PIL import Image

load_dotenv()

logging.basicConfig(level=logging.INFO)

DISCORD_TOKEN = os.getenv("DISCORD_API_KEY")
CHANNEL_ID = 1199708239185588264

# Image resize dimensions
MAX_WIDTH = 400
MAX_HEIGHT = 300

intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def download_image(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.read()
        else:
            logging.warning(f"Failed to download image from {url}. Status: {response.status}")
            return None

def resize_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail((MAX_WIDTH, MAX_HEIGHT))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    return buffered

async def send_technews():
    try:
        with open('2024-06-07_technews.json', 'r') as f:
            data = json.load(f)
            articles = data.get("articles", [])

        # Fetch the channel object
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            logging.error(f"Channel with ID {CHANNEL_ID} not found.")
            return

        async with aiohttp.ClientSession() as session:
            try:
                for article in articles:
                    # Send article title
                    title_message = f"## {article.get('revised_title', 'No Title')}"
                    await channel.send(title_message)

                    # Send article image (if available)
                    if article.get('image_links'):
                        image_data = await download_image(session, article['image_links'])
                        if image_data:
                            resized_image = resize_image(image_data)
                            file = discord.File(resized_image, filename="article_image.png")
                            await channel.send(file=file)

                    # Send article link and summary
                    link_and_summary = f"<[Read full article]({article.get('link', 'No Link')})>\n"
                    link_and_summary += f"{article.get('Summary', 'No summary available.')}"
                    await channel.send(link_and_summary)

                    # Add a separator between articles for clarity
                    await channel.send("---")
            finally:
                await session.close()

    except FileNotFoundError:
        logging.error("The tech news JSON file was not found.")
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from the tech news file.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        await client.close()

@client.event
async def on_ready():
    logging.info(f"{client.user.name} has connected to Discord!")
    await send_technews()

# Run the bot
client.run(DISCORD_TOKEN)

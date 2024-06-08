import discord
import logging
import json
import os
from dotenv import load_dotenv
import aiohttp
import io
from PIL import Image
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.INFO)

DISCORD_TOKEN = os.getenv("DISCORD_API_KEY")
CHANNEL_ID = 1199708239185588264

# Image resize dimensions
MAX_WIDTH = 400
MAX_HEIGHT = 300

intents = discord.Intents.all()
client = discord.Client(intents=intents)

def send_technews():

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

    def create_news_embed(article):
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

        # You can add more fields here, like category, author, etc.
        # embed.add_field(name="Category", value=article.get('category', 'Tech'), inline=True)

        embed.set_footer(text="Powered by MassCoders | News Agent")

        return embed

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
                    # Generate a cool header for today's tech news
                    today = datetime.now().strftime("%Y-%m-%d")
                    header = "## TechCrunch Daily Digest #001\n"
                    header_1 = f"📅 Date: {today}\n"

                    await channel.send(header)
                    await channel.send(header_1)

                    for index, article in enumerate(articles, 1):
                        embed = create_news_embed(article)
                        await channel.send(embed=embed)

                        # Add a separator between articles for clarity (optional)
                        if index < len(articles):
                            await channel.send("---")

                    # Footer message
                    await channel.send("🔔 Stay tuned for more tech insights tomorrow! 🌐")
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

send_technews()
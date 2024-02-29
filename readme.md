## News Agent

This pipeline scrapes the TechCrunch website for the latest news articles on a given date, summarizes and revises their titles, and uploads the processed content to a Supabase storage bucket. A Discord bot is used to send the summarized articles to a specified channel.

## Usage

### Running the pipeline manually
From the command line, navigate to the directory containing the codebase and run the following command:
`python app.py`
This will trigger the pipeline to scrape, summarize, and upload the latest articles for the current date.
### Scheduling the pipeline to run daily
To schedule the pipeline to run daily at a specific time, you can use a task scheduler such as cron or Windows Task Scheduler.
Configure the scheduler to run the following command at the desired time:
`python app.py`

![news agent](https://github.com/Spectral-Phoenix/News-Agent/assets/140725262/d0cc6ecd-b258-4034-b808-8f76aa8af0b1)

## Configuration

GEMINI_API_KEY = Google Gemini API Key

SUPABASE_URL =  The URL of your Supabase project

SUPABASE_KEY = The API key for your Supabase project

DISCORD_BOT_TOKEN = The token for your Discord bot

DISCORD_CHANNEL_ID = The ID of the Discord channel where you want the articles to be sent

COHERE_API_KEY = Cohere Coral API Key

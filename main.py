import discord
import os
from dotenv import load_dotenv
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timezone, timedelta

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

event_schedule = [
    "Spider Swarm", "Unnatural Outcrop", "Stryke the Wyrm",
    "Demon Stragglers", "Butterfly Swarm", "King Black Dragon Rampage",
    "Forgotten Soldiers", "Surprising Seedlings", "Hellhound Pack",
    "Infernal Star", "Lost Souls", "Ramokee Incursion",
    "Displaced Energy", "Evil Bloodwood Tree"
]

rotation_start = datetime(2024, 2, 5, 7, 0, tzinfo=timezone.utc)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()

def get_next_event():
    now = datetime.now(timezone.utc)
    hours_since_start = round((now - rotation_start).total_seconds() / 3600)
    event_index = hours_since_start % len(event_schedule)
    return event_schedule[event_index]

async def send_event_alert():
    channel = await client.fetch_channel(CHANNEL_ID)
    event_name = get_next_event()

    async for message in channel.history(limit=10):
        if message.author == client.user:
            await message.delete()

    await channel.send(f"@everyone ⚠️ **Upcoming Event:** {event_name} in 5 minutes! ⚠️")


@client.event
async def on_ready():
    load_dotenv()

    print(f"Logged in as {client.user}")

    scheduler.add_job(send_event_alert, "cron", minute=55)
    scheduler.start()

client.run(TOKEN)

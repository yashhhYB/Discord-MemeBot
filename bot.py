import discord
import requests
import json
import os
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$meme'):
            await message.channel.send(get_meme())

client = MyClient()

@client.tree.command(name="meme", description="Get random memes (max 4)")
@app_commands.describe(amount="Number of memes (1-4)")
async def meme(interaction: discord.Interaction, amount: int = 1):
    amount = min(max(amount, 1), 4)  
    memes = [get_meme() for _ in range(amount)]
    await interaction.response.send_message("\n".join(memes))

def get_meme():
    try:
        response = requests.get('https://meme-api.com/gimme')
        response.raise_for_status()
        json_data = response.json()
        return json_data['url']
    except Exception as e:
        print(f"Error fetching meme: {e}")
        return "Couldn't fetch a meme at this time."

client.run(TOKEN)

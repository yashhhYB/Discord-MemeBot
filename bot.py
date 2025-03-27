import discord
import requests
import json


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        print("Received message:", message.content)  # Debugging log
        if message.content.startswith('$meme'):
            print("Processing $meme command")  # Debugging log

            await message.channel.send(get_meme())


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
def get_meme():
  try:
    response = requests.get('https://meme-api.com/gimme')
    response.raise_for_status()  # Raise an error for bad responses
    json_data = json.loads(response.text)
    return json_data['url']
  except Exception as e:
    print(f"Error fetching meme: {e}")
    return "Sorry, I couldn't fetch a meme at this time."

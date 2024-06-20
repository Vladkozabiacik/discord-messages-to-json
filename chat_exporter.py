import discord
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
channel_id = int(os.getenv('channel_id'))

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    id = 1
    print(f'Logged in as {client.user.name}')

    channel = client.get_channel(channel_id)
    if channel is None:
        print('Invalid channel ID')
        return

    main_dir = 'User_Folders'
    os.makedirs(main_dir, exist_ok=True)

    messages = []
    ids = []
    user_folders = {}

    async for message in channel.history(limit=None):
        construct = []
        if message.author.bot:
            continue
        ids.append(id)
        construct.append(f'{id}, {message.author.name}, {message.clean_content}')
        messages.append(f'{construct}')
        id = id + 1

        if message.author.name not in user_folders:
            user_folder_name = os.path.join(main_dir, message.author.name.replace(" ", "_"))
            user_folders[message.author.name] = user_folder_name
            os.makedirs(user_folder_name, exist_ok=True)

        user_folder = user_folders[message.author.name]

        message_text_path = os.path.join(user_folder, 'message.txt')
        with open(message_text_path, 'a', encoding='utf-8') as text_file:
            text_file.write(f'{id}, {message.clean_content}\n')

        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                file_extension = os.path.splitext(attachment.filename)[1]
                file_path = os.path.join(user_folder, f'{id}{file_extension}')
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            with open(file_path, 'wb') as f:
                                f.write(await resp.read())
    
    messages.reverse()
    document = "\n".join(messages)

    with open('vycuc.txt', 'w', encoding='utf-8') as file:
        file.write(document)
    await client.close()

client.run(API_TOKEN)

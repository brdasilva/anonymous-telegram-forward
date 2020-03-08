import configparser

from telethon import TelegramClient, utils
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import (
    PeerChannel
)

# Reading Configs
config = configparser.RawConfigParser()
config.read("config.ini")

# Setting Telegram configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']
channel_to_forward_from = config['Telegram']['source_channel_id']
destination_channel_id = config['Telegram']['destination_channel_id']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")


async def authorize_client():
    # Ensure you're authorized
    isAuthorized = await client.is_user_authorized()
    if not isAuthorized:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    if channel_to_forward_from.isdigit():
        entity = PeerChannel(int(channel_to_forward_from))
        destination_entity = PeerChannel(int(destination_channel_id))
    else:
        entity = channel_to_forward_from
        destination_entity = destination_channel_id

    source_channel = await client.get_entity(entity)
    destination_channel = await client.get_input_entity(destination_entity)
    print(utils.get_display_name(source_channel))

    return source_channel, destination_channel


async def main():
    source_channel, destination_channel = await authorize_client()
    offset_id = 0

    while True:
        async for message in client.iter_messages(destination_channel, reverse=True, wait_time=5, min_id=offset_id):
            try:
                # await client.delete_messages(destination_channel, message.id, revoke=True)
                await client.send_message(destination_channel, message)
            except Exception:
                pass
            offset_id = message.id
        config.set("Telegram", "offset_id", str(offset_id))
        with open('config.ini', 'w') as configFile:
            config.write(configFile)


with client:
    client.loop.run_until_complete(main())

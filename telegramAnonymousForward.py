import configparser
import json

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting Telegram configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']
channel_to_forward_from = config['Telegram']['source_channel_id']
destination_channel = config['Telegram']['destination_channel_id']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")

# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))


if channel_to_forward_from.isdigit():
    entity = PeerChannel(int(channel_to_forward_from))
else:
    entity = channel_to_forward_from

source_channel = client.get_entity(entity)

offset_id = 0
limit = 100
all_messages = []
total_messages = 0
total_count_limit = 0

while True:
    print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
    history = client(GetHistoryRequest(
        peer=source_channel,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0
    ))
    if not history.messages:
        break
    messages = history.messages
    for message in messages:
        #all_messages.append(message.to_dict())
        print("Actual message: ", message.to_dict())
    offset_id = messages[len(messages) - 1].id
    total_messages = len(all_messages)
    #if total_count_limit != 0 and total_messages >= total_count_limit:
    #    break







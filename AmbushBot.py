from os import environ
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser
from telethon.tl.functions.messages import SendMessageRequest
from alchemysession import AlchemySessionContainer

import asyncio

import logging
import configparser
import datetime
import time
import random
import sys
import json
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

container = AlchemySessionContainer(environ['DATABASE_URL'])
session_name = environ.get('TG_SESSION', 'session')
container.core_mode = True 
session = container.new_session(session_name)

botToken = environ['TG_BOT_TOKEN']
client = TelegramClient(
    session, int(environ['TG_API_ID']), environ['TG_API_HASH'])

admonid = 323232619 
ambushChannelID = "-1001193142189"
website = "https://api.telegram.org/bot"+botToken
cwBotChat = 'chtwrsbot'
semaphore = 1
semaphore2 = 1

client.start(bot_token = botToken)

@client.on(events.ChatAction)
async def validateJoin(event):
    if event.user_added:
        user = await event.get_added_by()
        userID = user.id
        
        chat = await event.get_chat()
        chatID = chat.id
        chatTitle = chat.title
        
        print("Bot has been added to a new group by " + userID + "to group named: " + chatTitle)
        
        if user.id != admonid:
            await client.delete_dialog(chatID)


client.run_until_disconnected()







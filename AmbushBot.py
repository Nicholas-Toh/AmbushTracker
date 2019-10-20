from os import environ
from telethon import TelegramClient, events, Button
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
ambushChannelID = -1001193142189
website = "https://api.telegram.org/bot"+botToken
cwBotChat = 'chtwrsbot'
cwBotID = 408101137
semaphore = 1
semaphore2 = 1

client.start(bot_token = botToken)

@client.on(events.ChatAction)
async def validateJoin(event):
    if event.user_added:
        user = await event.get_added_by()
        userName = user.username
        userID = user.id
        
        chat = await event.get_chat()
        chatID = chat.id
        chatTitle = chat.title
        
        print("Bot has been added by @" + userName + " (" + str(userID) + ") " + "to a group named: " + chatTitle)
        
        if userID != admonid:
            await client.delete_dialog(chatID)

fightMessageRegex = re.compile(r"\w+/fight_\w+")
@client.on(events.NewMessage)
async def getMonsterMessage(event):
    print("Received message")
    if (event.message.fwd_from):
        fromChatID = event.message.fwd_from.from_id
        print(fromChatID)
        if fromChatID == cwBotID:
            print("from Chat Wars")
            if "ambush" in event.message.message:
                print("and has ambush")
                markup = setJoinButton("Join Fight")
                fightMessage = event.message.message + "\n\nPlayers who have joined the fight: "
                await sendMonsterTarget(ambushChannelID, fightMessage, markup)

async def sendMonsterTarget(target, message, markup=None):
    await client.send_message(target, message, buttons=markup)
    print ("Sending monster ambush message")

def setJoinButton(message):
    markup = client.build_reply_markup(Button.inline(message))
    return markup

@client.on(events.CallbackQuery(chats=ambushChannelID))
async def updateJoinedPlayers(event):
    fightMessage = event.get_message()
    clickedUserFirstName = event.get_sender().first_name
    if !clickedUserFirstName:
        clickedUserFirstName = ""

    clickedUserLastName = event.get_sender().last_name
    if !clickedUserLastName:
        clickedUserLastName = ""

    clickedUserFullName = clickedUserFirstName + clickedUserLastName
    fightMessage += ("\n" +clickedUserFullName)
    event.edit(fightMessage)

    
client.run_until_disconnected()







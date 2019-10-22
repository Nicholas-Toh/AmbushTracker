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
testChannelID = -1001278139694
controlCenterID = -1001456217101
website = "https://api.telegram.org/bot"+botToken
cwBotChat = 'chtwrsbot'
cwBotID = 408101137
semaphore = 1
semaphore2 = 1

client.start(bot_token = botToken)

##class Queue:
##    def __init__(self, size, capacity):
##        self.arr = [0 for i in range(capacity)]
##        self.front = 0
##        self.end = -1
##        self.size = size
##        self.numItems = 0
##
##    def extend(self, extension):
##        if self.size + extension <= self.capacity:
##            self.size += extension
##        else:
##            raise Exception("Size exceeded capacity of queue")
##
##    def reduce(self, reduction):
##        if self.size - reduction >= 0:
##            self.size -= reduction
##        else:
##            raise Exception("Size of queue cannot be reduced beyond 0")
##        
##    def enqueue(self, value):
##        if self.numItems + 1 > self.size:
##            raise Exception("Cannot enqueue: queue is full")
##            
##        self.end = (self.end + 1) % self.size
##        self.arr[self.end] = value
##        self.numItems += 1
##
##    def dequeue(self):
##        if self.numItems <= 0:
##            raise Exception("Cannot dequeue: queue is empty")
##        val = self.arr[self.front]
##        self.front = (self.front + 1) % self.size
##        self.numItems -= 1
##        return val
##
##FIGHT_TIME = 3 ##Minutes
##MAX_FIGHTERS = 4
##class Ambush:
##    def __init__(self, message, startTime):
##        self.sender = {} ##Dictionary mapping id(int) to username(string)
##        self.message = message
##        self.fightTime = FIGHT_TIME
##        self.endTime = startTime + datetime.timedelta(minutes=FIGHT_TIME)
##        self.maxFighters = MAX_FIGHTERS
##
##    def check_ended(self):
##        now = datetime.datetime.now()
##        if now >= self.endTime:
##            return True
##        else:
##            return False
##
##    def add_sender(self, userID, userFullName):
##        if self.key_exists(userID):
##            return False
##        else:
##            self.sender[userID] = userFullName
##            return True
##
##    def key_exists(self, key):
##        if key in self.sender.keys(): 
##            return True
##        else: 
##            return False
##            
##    def get_user_full_name(self, userID):
##        return self.sender[userID]
##
##    def get_name_list(self):
##        keys = list(self.sender.keys())
##        names = []
##        for key in keys:
##            names.append(self.sender[key])
##
##        return names
##    
##class AmbushFightController:
##    def __init__(self, queueSize, capacity):
##        self.capacity = capacity
##        self.queueSize = queueSize
##        self.queue = Queue(self.queueSize, self.capacity)
##        self.ambushes = []
##
##    def add_ambush(event):
##        self.ambushes.append(Ambush(event.message.message, event.message.date))

ambushes = {}

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


@client.on(events.NewMessage(chats=controlCenterID))
async def getMonsterMessageTest(event):
    print("Received message from control center")
    print("Received message")
    if (event.message.fwd_from):
        fromChatID = event.message.fwd_from.from_id
        if fromChatID == cwBotID:
            print("from Chat Wars")
            if "ambush" in event.message.message:
                print("and has ambush")
                ambushes[event.message.id] = {}
                markup = setJoinButton("Join Fight")
                fightMessage = event.message.message + "\nPlayers who have joined the fight: "
                await sendMessage(ambushChannelID, fightMessage, markup)
                
    raise events.StopPropagation
    
fightMessageRegex = re.compile("/fight_(\w+)")
@client.on(events.NewMessage)
async def getMonsterMessage(event):
    print("Received message")
    if (event.message.fwd_from):
        fromChatID = event.message.fwd_from.from_id
        if fromChatID == cwBotID:
            print("from Chat Wars")
            if "ambush" in event.message.message:
                print("and has ambush")
                markup = setJoinButton("Join Fight")
                fightMessage = event.message.message + "\nPlayers who have joined the fight: "
                await sendMessage(testChannelID, fightMessage, markup)

async def sendMessage(target, message, markup=None):
    await client.send_message(target, message, buttons=markup)
    print ("Sending monster ambush message")

def setJoinButton(message):
    markup = client.build_reply_markup(Button.inline(message))
    return markup

@client.on(events.CallbackQuery(chats=ambushChannelID))
async def updateJoinedPlayers(event):
    originalMessage = await event.get_message()
    fightMessage = originalMessage.message
    clickedUser = await event.get_sender()
    clickedUserFirstName = clickedUser.first_name
    if not clickedUserFirstName:
        clickedUserFirstName = ""

    clickedUserLastName = clickedUser.last_name
    if not clickedUserLastName:
        clickedUserLastName = ""

    clickedUserFullName = clickedUserFirstName + clickedUserLastName
    fightMessage += ("\n" +clickedUserFullName)
    markup = setJoinButton("Join Fight")
    await event.edit(fightMessage, buttons=markup)

    
client.run_until_disconnected()







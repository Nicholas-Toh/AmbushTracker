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

DATABASE_URL = "DATABASE_URL"
TG_API_HASH =  "TG_API_HASH"
TG_API_ID= "TG_API_ID"
TG_BOT_TOKEN = "TG_BOT_TOKEN"
TG_SESSION = "TG_SESSION"

container = AlchemySessionContainer(DATABASE_URL)
session_name = TG_SESSION
container.core_mode = True 
session = container.new_session(session_name)

botToken = TG_BOT_TOKEN
client = TelegramClient(
    session, int(TG_API_ID), TG_API_HASH)

admonid = ADMONID 
ambushChannelID = AMBUSHCHANNELID
controlCenterID = CONTROLCENTERID
website = "https://api.telegram.org/bot"+botToken
cwBotChat = 'chtwrsbot'
cwBotID = 408101137
semaphore = 1
semaphore2 = 1

client.start(bot_token = botToken)


FIGHT_TIME = 3 ##Minutes
MAX_FIGHTERS = 4
class Ambush:
    def __init__(self, message, startTime):
        self.sender = {} ##Dictionary mapping id(int) to username(string)
        self.message = message
        self.fightTime = FIGHT_TIME
        self.endTime = startTime + datetime.timedelta(minutes=FIGHT_TIME)
        self.maxFighters = MAX_FIGHTERS
        self.ended = False

    def check_ended(self):
        unawareNow = datetime.datetime.now()
        now = unawareNow.replace(tzinfo=datetime.timezone.utc)
        if now >= self.endTime:
            return True
        else:
            return False

    def add_sender(self, userID, userFullName):
        if self.key_exists(userID):
            logger.error(f'User ID ({userID}) already exists')
            return False

        elif len(self.sender) == MAX_FIGHTERS:
            logger.error(f'Ambush participants already reached {MAX_FIGHTERS}')
            return False
        
        else:
            self.sender[userID] = userFullName
            return True

    def delete_sender(self, userID):
        if self.key_exists(userID):
            del self.sender[userID]
            return True

        else:
            logger.error(f'User ID ({userID}) does not exist')
            return False
            
    def key_exists(self, key):
        if key in self.sender.keys():
            return True
        else: 
            return False
            
    def get_user_full_name(self, userID):
        return self.sender[userID]

    def get_name_list(self):
        keys = list(self.sender.keys())
        names = []
        for key in keys:
            names.append(self.sender[key])

        return names
    
class AmbushFightController:
    def __init__(self, queueSize, capacity):
        self.capacity = capacity
        self.queueSize = queueSize
        #self.queue = Queue(self.queueSize, self.capacity)
        self.ambushes = {} ## date ---> ambush
        self.messageDateIDMap = {} ## id ---> date

    def add_ambush(self, dateID, message, messageDate):
        if dateID not in self.ambushes.keys():
            self.ambushes[dateID] = Ambush(message, messageDate)
            return True
        else:
            return False

    def delete_ambush(self, dateID):
        try:
            del self.ambushes[dateID]
        except KeyError as error:
            raise RuntimeError("Failed to delete ambush") from error

    def add_sender(self, dateID, userID, userName):
        if not self.ambushes[dateID].add_sender(userID, userName):
            logger.error(f'Failed to add user with id ({userID}) to ambush id ({dateID})')
            return False
        else:
            return True

    def delete_sender(self, dateID, userID):
        if not self.ambushes[dateID].delete_sender(userID):
            logger.error(f'Failed to delete user with id ({userID}) to ambush id ({dateID}) - ID does not exist')
            return False
        else:
            return True
        
    def key_exists(self, key):
        if key in self.ambushes.keys():
            return True
        else: 
            return False
        
    def get_ambush(self, ambushID):
        if self.key_exists(ambushID):
            return self.ambushes[ambushID]
        else:
            logger.error(f'Failed to get ambush ({ambushID})')

    def map_message_date_id(self, messageID, dateID):
        self.messageDateIDMap[messageID] = dateID

    def get_ambushID(self, messageID): 
        if messageID in self.messageDateIDMap.keys():
            return self.messageDateIDMap[messageID]
        else:
             logger.error(f'Failed to get ambushID using message ID ({messageID})')

ambushFightController = AmbushFightController(900, 200)

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


@client.on(events.NewMessage)
async def getMonsterMessage(event):
    print("Received message")
    if (event.message.fwd_from):
        fromChatID = event.message.fwd_from.from_id
        if fromChatID == cwBotID:
            print("from Chat Wars")
            if "ambush" in event.message.message:
                print("and has ambush")
                message = event.message.message
                date = event.message.fwd_from.date
                if ambushFightController.add_ambush(date, message, date):
                    markup = setJoinButton("Join Fight")
                    fightMessage = message + "\nPlayers who have joined the fight: "

                    result = await sendMessage(ambushChannelID, fightMessage, markup)

                    ambushFightController.map_message_date_id(result.id, date)
                    print(date)
                    
                    now = event.message.date
                    
                    await asyncio.sleep((ambushFightController.get_ambush(date).endTime-now).total_seconds())
                    ambush = ambushFightController.get_ambush(date)
                    print(f'Fight at {ambush.endTime} ended')
                    ambush.ended = True
                    fightMessage = ambush.message+ "\nPlayers who have joined the fight: "
                    for name in ambush.get_name_list():
                        fightMessage += ("\n" + name)
                    await editMessage(ambushChannelID, result.id, fightMessage+"\n\nFight is over!")
                    ##ambushFightController.delete_ambush(date)
                    
                else:
                    logger.info(f'Ambush {event.message.id} already exists')
                
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
    return await client.send_message(target, message, buttons=markup)
    print ("Sending monster ambush message")

async def editMessage(target, messageid, message, markup=None):
    return await client.edit_message(target, messageid, message, buttons=markup)
    print ("Editing monster ambush message")



def setJoinButton(message):
    markup = client.build_reply_markup(Button.inline(message))
    return markup

@client.on(events.CallbackQuery(chats=ambushChannelID))
async def updateJoinedPlayers(event):
    logger.warning("Received button click")
    originalMessage = await event.get_message()
    clickedUser = await event.get_sender()
    clickedUserFirstName = clickedUser.first_name
    if not clickedUserFirstName:
        clickedUserFirstName = ""

    clickedUserLastName = clickedUser.last_name
    if not clickedUserLastName:
        clickedUserLastName = ""

    clickedUserFullName = clickedUserFirstName + " " + clickedUserLastName
    date = ambushFightController.get_ambushID(originalMessage.id)
    ambush = ambushFightController.get_ambush(date)
    
    if ambush.key_exists(clickedUser.id):
        ambushFightController.delete_sender(date, clickedUser.id)
    
    else: 
        ambushFightController.add_sender(date, clickedUser.id, clickedUserFullName)

    fightMessage = ambush.message+ "\nPlayers who have joined the fight: "

    for name in ambush.get_name_list():
        fightMessage += ("\n" + name)
        
    markup = None
    if not ambush.ended:
        markup = setJoinButton("Join Fight")

    await event.edit(fightMessage, buttons=markup)
        
    logger.warning("Finished processing button click")
        
        

    
client.run_until_disconnected()







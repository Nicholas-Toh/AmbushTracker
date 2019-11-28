#!/usr/bin/env python3
from os import environ
from multiprocessing import Process
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
#telethon==0.19.1.6
#git+https://github.com/BlaQPhoeniX/telethon-session-sqlalchemy.git@postgres-fix
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

#Set up session and connect to Tg
proxy_chan_id = 1151984662

container = AlchemySessionContainer(environ['DATABASE_URL'])
session_name = environ.get('TG_SESSION', 'session')
container.core_mode = True 
session = container.new_session(session_name)

user_phone = environ['TG_PHONE']
client = TelegramClient(
    session, int(environ['TG_API_ID']), environ['TG_API_HASH'])

def code_cb():
    return 42385




cwBotChat = 'chtwrsbot'
go2ChatID = -1001288184462
#await go2Chat = client.get_entity(go2ChatID)
chihan = "MeatSchtick"
chatWarsAuction = "ChatWarsAuction"
aucMsg = ""
#await chihanChat = client.get_entity(chihan)
#staminaTime = 0
semaphore = 1
semaphore2 = 1
arenaSemaphore = 1

items = [("Order Armor +", 2), ("Trident +", 5), ("Hunter Armor +", 2), ("Hunter Bow +", 5), ("Composite Bow +", 8), ("Imperial Axe +", 8), ("Guard's Spear +", 8), ("War hammer +", 5), ("Royal Armor +", 4), ("Crusader Armor +", 4), ("Meteor Bow +", 10), ("Hailstorm Bow +", 8), ("Thundersoul Sword +", 8), ("King's Defender +", 8), ("Raging Lance +", 8), ("Skull Crusher +", 8), ("Dragon Mace +", 8), ("Heavy Fauchard +", 10), ("Black Morningstar +", 10)]

@client.on(events.NewMessage(chats=chatWarsAuction))
async def snipeAuctio(event):
    for item in items:
        if item[0] in event.message.message:
            try:
                betMessage = (re.search("/bet_(\w+)", event.message.message)).group(0)
                betMessage += "_" + str(item[1])
                await client.send_message(cwBotChat, betMessage)
                #await asyncio.sleep(random.randint(1, 3))
                unawareNow = datetime.datetime.now()
                now = unawareNow.replace(tzinfo = datetime.timezone.utc)
                handlingTime = (now - event.message.date).total_seconds()
                print(f"Time taken to handle auction: {handlingTime}")
                print("Betting on " + item[0][:-2] + " with " + str(item[1]) + " pouches.")
            except:
                print("Bet failed")
                
@client.on(events.NewMessage(from_users=cwBotChat))
async def stopForay(event):
    #print("Foray spotted")
    if '/go' in event.message.message:
        await asyncio.sleep(random.randint(1,5))
        await client.send_message(cwBotChat, '/go')
        #await setDef()
        print("Stopping Foray...")

@client.on(events.NewMessage(from_users=cwBotChat))
async def fightMonsters(event):
    if '/fight' in event.message.message:
        try:
            go2Chat = await client.get_entity(go2ChatID)
            await sendMonsterTarget(go2Chat, event.message)
            matches = re.findall("lvl.(\w+)", event.message.message)
            await asyncio.sleep(random.randint(1, 5))
            if len(matches) == 1:
                fightMessage = re.search("/fight_(\w+)", event.message.message)
                await client.send_message(cwBotChat, fightMessage)
                print ("Fighting monsters")
        except:
                print ("Fighting failed for some reason...")

##@client.on(events.NewMessage(from_users=chihan))
##async def fightMonsters2(event):
##    if '/fight' in event.message.message:
##        try:
##            await sendMonsterTarget(chihan, event.message)
##            await asyncio.sleep(random.randint(1, 5))
##            fightMessage = (re.search("/fight_(\w+)", event.message.message)).group(0)
##            await client.send_message(cwBotChat, fightMessage)
##            print ("Fighting monsters")
##        except:
##                print ("Fighting failed for some reason...")

#@client.on(events.NewMessage(from_users=cwBotChat, pattern=r"/f_report"))

                
async def sendMonsterTarget(target, message):
    await asyncio.sleep(random.randint(1, 5))
    await client.forward_messages(target, message)
    print ("Sending monster fight message")

async def setDef():
    await asyncio.sleep(random.randint(1,5))
    await client.send_message(cwBotChat, '\U0001F6E1'+'Defend')
    print("Setting defence")

async def setDefScheduler():
    endTime = datetime.datetime.now()
    if endTime.hour == 22 and endTime.minute == 59:
        await setDef()
        await asyncio.sleep(60)
    elif endTime.hour == 6 and endTime.minute == 59:
        await setDef()
        await asyncio.sleep(60)
    elif endTime.hour == 14 and endTime.minute == 59:
        await setDef()
        await asyncio.sleep(60)

async def signal():
    global semaphore
    semaphore += 1

async def wait():
    global semaphore
    semaphore -= 1
    
async def goSwamp():
    await asyncio.sleep(random.randint(1,10))
    await client.send_message(cwBotChat, '\U0001F5FA'+'Quests')
    await asyncio.sleep(1)
    questText = await client.get_messages(cwBotChat, limit=1)
    await asyncio.sleep(random.randint(1,10))
    print ("Going to the swamp")
    await questText[0].click(text= '\U0001F344'+'Swamp')
    #await client.send_message(cwBotChat, '\U0001F344'+'Swamp')

async def brewExp():
    #asyncio.sleep(random.randint(1,10))
    print ("Brewing")
    await client.send_message(cwBotChat, '/craft_23')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/craft_22')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/craft_22')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/craft_22')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/craft_22')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/craft_22')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/brew_507')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/brew_507')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/brew_507')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/brew_507')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/brew_509')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/use_507')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/use_507')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/use_507')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/use_507')
    await asyncio.sleep(random.randint(1,3))
    await client.send_message(cwBotChat, '/use_509')

async def buyResource(code, amount):
    asyncio.sleep(random.randint(1,5))
    print ("Buying item code" + code)
    buyOrder = '/wtb_' + code + '_' + str(amount)
    await client.send_message(cwBotChat, buyOrder)
    
async def goSwampScheduler():
    global semaphore
    #print(semaphore)
    if semaphore > 0:
        semaphore -= 1
        #evening swamp
        endTime = datetime.datetime.now()
        if endTime.hour == 19 and endTime.minute == 5:
            await goSwamp()
            await asyncio.sleep (13*30)
        elif endTime.hour == 19 and endTime.minute == 12:
            await goSwamp()
            await asyncio.sleep (13*30)            
        elif endTime.hour == 19 and endTime.minute == 19:
            await goSwamp()
            await asyncio.sleep (13*30)               
        elif endTime.hour == 19 and endTime.minute == 26:
            await goSwamp()
            await asyncio.sleep (13*30)
        elif endTime.hour == 19 and endTime.minute == 33:
            await goSwamp()
            await asyncio.sleep (13*30)
        elif endTime.hour == 19 and endTime.minute == 40:
            await goSwamp()
            await asyncio.sleep (13*30)
        elif endTime.hour == 20 and endTime.minute == 5:
            await goSwamp()
            await asyncio.sleep (13*30)            
        elif endTime.hour == 20 and endTime.minute == 12:
            await goSwamp()
            await asyncio.sleep (13*30)            
        elif endTime.hour == 20 and endTime.minute == 19:
            await goSwamp()
            await asyncio.sleep (13*30)               
        elif endTime.hour == 20 and endTime.minute == 26:
            await goSwamp()
            await asyncio.sleep (13*30)
        elif endTime.hour == 20 and endTime.minute == 33:
            await goSwamp()
            await asyncio.sleep (13*30)
        elif endTime.hour == 20 and endTime.minute == 40:
            await goSwamp()
            await asyncio.sleep (13*30)

        #night swamp

        if endTime.hour == 21 and endTime.minute == 5:
            await goSwamp()
            await asyncio.sleep (17*30)
        elif endTime.hour == 21 and endTime.minute == 14:
            await goSwamp()
            await asyncio.sleep (17*30)            
        elif endTime.hour == 21 and endTime.minute == 23:
            await goSwamp()
            await asyncio.sleep (17*30)               
        elif endTime.hour == 21 and endTime.minute == 32:
            await goSwamp()
            await asyncio.sleep (17*30)
        elif endTime.hour == 21 and endTime.minute == 41:
            await goSwamp()
            await asyncio.sleep (17*30)
        elif endTime.hour == 21 and endTime.minute == 50:
            await goSwamp()
            await asyncio.sleep (17*30)
        elif endTime.hour == 21 and endTime.minute == 59:
            await goSwamp()
            await asyncio.sleep (17*30)
            #engageOffset = 0
            
        elif endTime.hour == 22 and endTime.minute == 8:
            await goSwamp()
            await asyncio.sleep (17*30)
        elif endTime.hour == 22 and endTime.minute == 17:
            await goSwamp()
            await asyncio.sleep (17*30)            
        elif endTime.hour == 22 and endTime.minute == 26:
            await goSwamp()
            await asyncio.sleep (17*30)               
        elif endTime.hour == 22 and endTime.minute == 35:
            await goSwamp()
            await asyncio.sleep (17*30)
        if endTime.hour == 22 and endTime.minute == 44:
            ##await buyResource('02', 15)
            ##await brewExp()
            await goSwamp()
            await asyncio.sleep (17*30)
            
        
        semaphore += 1
        #return stamina

    else:
        return
                    
async def checkStamina():
    await client.send_message(cwBotChat, '\U0001F3C5'+'Me')

async def goArena():
    await asyncio.sleep(random.randint(1,10))
    print ("Going to the Arena")
    await client.send_message(cwBotChat, '▶️Fast fight')
    
async def equipArenaWeapons():
    await asyncio.sleep(random.randint(1,10))
    print ("Equipping Arena weapons")
    await client.send_message(cwBotChat, '/on_u120')
    await asyncio.sleep(random.randint(1,10))
    await client.send_message(cwBotChat, '/on_508')

async def equipDefWeapons():
    await asyncio.sleep(random.randint(1,10))
    print ("Equipping Defend weapons")
    await client.send_message(cwBotChat, '/on_u124')
    await asyncio.sleep(random.randint(1,10))
    await client.send_message(cwBotChat, '/on_506')

async def goArenaScheduler():
    global arenaSemaphore
    #print(semaphore)
    if arenaSemaphore > 0:
        arenaSemaphore -= 1
        #evening swamp
        endTime = datetime.datetime.now()
        if endTime.hour == 9 and endTime.minute == 15:
            await equipArenaWeapons()
            await goArena()
            await asyncio.sleep(120)
        elif endTime.hour == 11 and endTime.minute == 30:
            #await equipArenaWeapons()
            await goArena()
            await asyncio.sleep(120)
        
        arenaSemaphore += 1
    else:
        return

@client.on(events.NewMessage(from_users=cwBotChat))
async def goToArena(event):
    if 'find an opponent.' in event.message.message or '/top5' in event.message.message:
        await asyncio.sleep(random.randint(1,10))
        await goArena()

@client.on(events.NewMessage(from_users=cwBotChat))
async def afterArenaChangeWeapons(event):
    if 'heal your wounds' in event.message.message:
        await asyncio.sleep(random.randint(1,10))
        #await equipDefWeapons()

##@client.on(events.NewMessage(from_users=cwBotChat))
##async def getStamina(event):
##    global semaphore2
##    print("begin of getStamina: " + str(semaphore2))
##    if semaphore2 > 0:
##        endTime = datetime.datetime.now()
##        try:
##            #global staminaTime
##            staminaTime = int(re.search("(\d+)min", event.message.message).group(1))
##            #print(staminaTime)
##            #print(endTime.hour == 8 and endTime.minute == 25 and staminaTime > 7)
##            if endTime.hour == 18 or endTime.hour == 17 and staminaTime > 7: 
##                await goSwamp()
##                semaphore2 -= 1
##                print("end of getStamina: " + str(semaphore2))
##                await asyncio.sleep (13*30)
##                semaphore2 += 1
##            elif endTime.hour == 18 or endTime.hour == 17 and staminaTime <= 7:
##                semaphore2 -= 1
##                print("end of getStamina: " + str(semaphore2))
##                await asyncio.sleep (staminaTime*60)
##                semaphore2 += 1
##            elif endTime.hour == 21 and staminaTime > 9:
##                await goSwamp()
##                semaphore2 -= 1
##                print("end of getStamina: " + str(semaphore2))
##                await asyncio.sleep (17*30)
##                semaphore2 += 1
##
##            elif endTime.hour == 21 and staminaTime <= 9:
##                semaphore2 -= 1
##                print("end of getStamina: " + str(semaphore2))
##                await asyncio.sleep (staminaTime*60)
##                semaphore2 += 1
##                
##        except:
##            return
##        
##    else:
##        return
 

async def wait_for(dt):
    # sleep until the specified datetime
    while True:
        now = datetime.datetime.now()
        remaining = (dt - now).total_seconds()
        if remaining < 86400:
            break
        # asyncio.sleep doesn't like long sleeps, so don't sleep more
        # than a day at a time
        await asyncio.sleep(86400)
    await asyncio.sleep(remaining)

async def run_at(dt, coro):
    await wait_for(dt)
    return await coro

async def getAuction():
    global aucMsg
    newAucMsg = await client.get_messages(chatWarsAuction)
    if newAucMsg != aucMsg:
        print("Received new auction via get messages")
    else:
        aucMsg = newAucMsg
    await asyncio.sleep(0.5)
    

#await checkStamina()
client.start(phone=user_phone, code_callback=code_cb)
async def main(delay):
    currentTime = datetime.datetime.now()
    startTime = 0
    timeOffset = 0
    sleepTime = 0
    while True: #start == True:
        endTime = datetime.datetime.now()
        #print (str(endTime.second) + str(startTime))
        if startTime != 0:
            if endTime.second - startTime > delay:
                timeOffset = 1
            else:
                timeOffset = 0
        startTime = endTime.second
        #print (str(endTime.hour) +" : " + str(endTime.minute) + " : " + str(endTime.second) +"."+str(endTime.microsecond))
        await setDefScheduler()
        asyncio.ensure_future(goSwampScheduler())
        asyncio.ensure_future(goArenaScheduler())
        endProcessTime = datetime.datetime.now()
        sleepTime = delay - (endProcessTime.second-startTime) - timeOffset
        if sleepTime < 0:
            sleepTime = 0
        await asyncio.sleep(sleepTime)
##    while True:
##        #print(loop.time())
##        await setDefScheduler()
##        asyncio.ensure_future(goSwampScheduler())
##        await asyncio.sleep(delay)

loop = asyncio.get_event_loop()    
loop.create_task(main(3))
loop.create_task(getAuction())
#loop.create_task(goSwampScheduler())
        
                             

loop.run_forever()
print (loop.is_running())


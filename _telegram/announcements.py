import os
import yaml
import telebot
from decouple import config
from datetime import datetime as DT
import pytz
import time
import json


global bot
global TOKEN

TOKEN = config('BOT_TOKEN')
# CHAT_ID = config('CHAT_ID')
CHAT_ID_json = os.getenv("CHAT_ID")
print(CHAT_ID_json)
CHAT_ID = json.loads(CHAT_ID_json)
ANNOUNCEMENTS = '_telegram/announcements.yaml'
ANNOUNCE_EVERY = 15 #minutes

with open(ANNOUNCEMENTS, 'r') as stream:
    try:
        parsed_announcements=yaml.safe_load(stream)
        # print(parsed_announcements)
    except yaml.YAMLError as exc:
        print(exc)
        raise SystemExit
bot = telebot.TeleBot(TOKEN, parse_mode=None)

NOW = DT.now(pytz.timezone('Europe/Athens')).replace(tzinfo=None)
print('Now in Athens/GR: ', NOW)

for dt, channels in parsed_announcements.items():
    ann_time = DT.strptime(dt, '%d/%m/%Y %H:%M:%S')
    # print('Announcement time:', ann_time)
    diff = (ann_time - NOW)
    # print ('Diff DAYS:', diff_sec.days )
    # print ('Diff SEC :', diff_sec.seconds )
    if diff.days != 0:
        print('Skip: ', ann_time, '> DAY ', diff)
        continue
    if diff.seconds/60 > ANNOUNCE_EVERY :
        print('Skip: ', ann_time, '> ',ANNOUNCE_EVERY, ' MINUTES ', diff)
        continue
    print('Announce: ', ann_time)
    for channel in channels:
        if channel in CHAT_ID:
            for txt in parsed_announcements[dt][channel]:
                print('Coming up at #wmceem2025 \n\n🕰️ '+(ann_time.strftime('%H:%M %Y-%m-%d'))+' \n'+txt)
                bot.send_message(chat_id=CHAT_ID[channel], text=('Coming up at Wikimedia CEE Meeting 2025 \n\n🕰️'+(ann_time.strftime('%H:%M %Y-%m-%d'))+' \n'+txt))
                time.sleep(1)
        else:
            print('No channel:', channel)
            continue
            
import os
import yaml
import telebot
from decouple import config
from datetime import datetime as DT
import pytz
import time

global bot
global TOKEN

TOKEN = config('BOT_TOKEN')
CHAT_ID = config('CHAT_ID')
# ANNOUNCEMENTS = config('ANNOUNCEMENTS')
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

for dt, arr in parsed_announcements.items():
    ann_time = DT.strptime(dt, '%d/%m/%Y %H:%M:%S')
    print(ann_time)
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
    for txt in arr:
        # bot.send_message(chat_id=CHAT_ID, text=('Coming up at #wmcee #wmcee2025 \n🕰️'+(ann_time.strftime('%H:%M'))+' \n\n'+txt))
        bot.send_message(chat_id=CHAT_ID, text=('Coming up at Wikimedia CEE Meeting 2025 \n🕰️'+(ann_time.strftime('%H:%M'))+' \n\n'+txt))
        time.sleep(1)

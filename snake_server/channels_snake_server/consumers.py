# In consumers.py
import json
import random

import redis
from channels import Group

# Connected to websocket.connect
from django.shortcuts import render_to_response

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def ws_add(message):
    Group("snake").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
    selected = message.content['text']
    r.setex(message.reply_channel.name, 1, message.content['text'])

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("snake").discard(message.reply_channel)

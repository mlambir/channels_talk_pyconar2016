import json
import random

import time

import redis
from channels import Group
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'sends controller status'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        # c = Channel('snake', channel_layer=channel_layers['default'])

        while 1:
            vals = {
                "up": 0,
                "down": 0,
                "left": 0,
                "right": 0,
                "connected": 0,
                "selected": ""
            }
            keys = r.keys("websocket.send*")

            for k in keys:
                val = r.get(k)
                if val:
                    vals[val.decode("utf-8")] += 1

            items = [(k, v) for k, v in vals.items() if k in ["up", "down", "left", "right"]]

            items.sort(key=lambda x: x[1])

            if items[-1][1]:
                vals["selected"] = items[-1][0]

            Group('snake').send({
                'text': json.dumps(vals)
            })
            time.sleep(.1)

"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.

Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from corenetwork.cli.cli_base import CommandLineBase
from datetime import datetime, timedelta
from django.db.models import Q
from corenetwork.hook_interface import HookInterface
from corenetwork.models.message import Message
from corenetwork.models.tag import Tag
import re
import time


class Cmd(CommandLineBase):
    actions = {
        'last': {
            'help': 'Show logs from defined period of time',
            'params': {
                'period': {
                    'help': 'Specifies period in minutes, hours or days, by suffix m, h, d. For example: 2h specifies two hours.'
                },
                'tags': {
                    'help': 'Comma-separated list of tags'
                }
            }
        },
        'all': {
            'help': 'Show all logs',
            'params': {
                'tags': {
                    'help': 'Comma-separated list of tags'
                }
            }
        },
        'watch': {
            'help': 'Wait for new messages in logs and pring them',
            'params': {
                'tags': {
                    'help': 'Comma-separated list of tags'
                }
            }
        },
        'clear': {
            'help': 'Remove all logs'
        }
    }

    def _print(self, message_set):
        for msg in message_set.order_by('date').all():
            print(str(msg))

    def _query(self, tags):
        if tags != '' and tags is not None:
            tag_list = Tag.objects.filter(name__in=tags.split(',')).all()
            if len(tag_list) == 0:
                print('Tag not found')
                return

            q = tag_list[0].message_set.all()
            for tag in tag_list[1:]:
                q = q & tag.message_set.all()
        else:
            q = Message.objects

        return q

    def all(self, tags=''):
        q = self._query(tags)
        self._print(q)

    def last(self, interval, tags=''):
        q = self._query(tags)

        digits = int(re.findall('\d+', interval)[0])
        if interval[-1] in ['m', 'min', 'minute', 'minutes']:
            q = q.filter(date__range=(datetime.now() - timedelta(minutes=digits), datetime.now()))
        elif interval[-1] in ['h', 'H', 'hour', 'hours']:
            q = q.filter(date__range=(datetime.now() - timedelta(hours=digits), datetime.now()))
        elif interval[-1] in ['d', 'D', 'day', 'days']:
            q = q.filter(date__range=(datetime.now() - timedelta(days=digits), datetime.now()))
        elif interval[-1] in ['w', 'W', 'week', 'weeks']:
            q = q.filter(date__range=(datetime.now() - timedelta(weeks=digits), datetime.now()))

        self._print(q)

    def watch(self, tags=''):
        last_d = None
        while True:
            q = self._query(tags)
            q = q.order_by('date')

            if last_id is not None:
                result = q.filter(id__gt=last_id).all()
                for msg in result:
                    print(str(msg))
                    last_id = msg.id
            else:
                last_id = q.last().id
            time.sleep(0.5)


    def clear(self):
        Message.objects.all().delete()
        print('Deleted all logs')

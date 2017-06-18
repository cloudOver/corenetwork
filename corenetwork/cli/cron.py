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
from corenetwork.hook_interface import HookInterface
from corenetwork.os_mixin import OsMixin


class Cmd(CommandLineBase):
    actions = {
        'minute': {
            'help': 'Execute minute actions',
        },
        'hourly': {
            'help': 'Execute hourly actions',
        },
        'daily': {
            'help': 'Execute daily actions',
        },
        'weekly': {
            'help': 'Execute weekly actions',
        },
        'monthly': {
            'help': 'Execute monthly actions',
        },
    }

    def execute(self, interval):
        osm = OsMixin()
        osm._become_cloudover()

        hooks = []
        if interval == 'minute':
            hooks = HookInterface.get_hooks('cron.minute')
        elif interval == 'hourly':
            hooks = HookInterface.get_hooks('cron.hourly')
        elif interval == 'daily':
            hooks = HookInterface.get_hooks('cron.daily')
        elif interval == 'weekly':
            hooks = HookInterface.get_hooks('cron.weekly')
        elif interval == 'monthly':
            hooks = HookInterface.get_hooks('cron.monthly')
        else:
            print 'Unknown interval'

        for hook in hooks:
            if hasattr(hook, 'cron'):
                hook.cron(interval)

    def minute(self):
        self.execute('minute')

    def hourly(self):
        self.execute('hourly')

    def daily(self):
        self.execute('daily')

    def weekly(self):
        self.execute('weekly')

    def monthly(self):
        self.execute('monthly')
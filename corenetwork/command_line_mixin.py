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

from corenetwork.utils import system
from corenetwork.utils import config
from corenetwork.utils.logger import log
import importlib


class CommandLineMixin():
    def _get_commands(self):
        """
        Get list with all enabled commands
        :param action: Name of action which is triggering hook call
        :param pipeline: Deprecated.
        :return:
        """
        commands = {}
        from corenetwork.utils.config import settings

        for app_name in settings.APPS:
            app = importlib.import_module(app_name).MODULE
            if 'cli' in app:
                for module in app['cli'].keys():
                    try:
                        cli_handler = importlib.import_module(app['cli'][module])
                        commands[module] = cli_handler.Cmd()
                    except Exception as e:
                        log(msg='Failed to import hook: %s' % app['cli'][module], exception=e, tags=('hook', 'fatal', 'error'))
        return commands

    def cli_handle(self, params):
        cmds = self._get_commands()
        if params[1] not in cmds and params[1] != 'help':
            print('Command not supported')
        elif params[1] == 'help':
            cmds[params[2]].help()
        else:
            cmds[params[1]].call(params[2], params[3:])

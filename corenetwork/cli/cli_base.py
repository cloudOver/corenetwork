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

class CommandLineBase:
    """
    Command Line base class. Override it with own class to provide command line tool. Each tool should be listed in
    app.py file in cli section. See corecluster.app for details. Each derived class should be called Cmd to provide
    proper import of module by CLI driver
    """

    actions = {
        'test_action': {
            'help': 'Help text',
            'params': {
                'first_parameter': {
                    'help': 'Description for parameter',
                },
                'second_parameter': {
                    'help': 'Description for parameter',
                },
            },
        }
    }

    # Example:
    # def test_action(self, first_parameter, second_parameter):
    #     pass

    def call(self, action, params):
        if action in self.actions.keys():
            a = getattr(self, action)
            a(*params)
        else:
            print('Command not found')

    def help(self, command=None):
        if command is None:
            for action in self.actions:
                if 'help' in self.actions[action]:
                    print('cc-manage ' + action + ': ' + self.actions[action]['help'])
                else:
                    print('cc-manage ' + action + ': ' + 'No help available')

                if 'params' in self.actions[action]:
                    print('Parameters:')
                    for param in self.actions[action]['params'].keys():
                        if 'help' in self.actions[action]['params'][param]:
                            print('\t- ' + param + '\t' + self.actions[action]['params'][param]['help'])
                        else:
                            print('\t- ' + param)
                print('')

        elif command in self.actions.keys():
            if 'help' in self.actions[command]:
                print(self.actions[command]['help'])
            else:
                print('No help available')

            if 'params' in self.actions[command]:
                for param in self.actions[command]['params'].keys():
                    if 'help' in self.actions[command]['params'][param]:
                        print(' - ' + param + ': ' + self.actions[command]['params'][param]['help'])
                    else:
                        print(' - ' + param)
            print('')
        else:
            print('Command not found in this module')

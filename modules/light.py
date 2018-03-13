#!/usr/bin/env python3

import sys
from subprocess import check_output
from notification import Notification


class Light():
    @staticmethod
    def arguments_parser(parser):
        sp = parser.add_parser('light')

        subs = sp.add_subparsers(dest='lightcommand')

        increase = subs.add_parser('inc', help='Increase value')
        increase.add_argument('value', type=int, help='Step to increase')

        decrease = subs.add_parser('dec', help='Decrease value')
        decrease.add_argument('value', type=int, help='Step to decrease')

        set = subs.add_parser('set', help='Set value')
        set.add_argument('value', type=int, help='Set brightness to')

        return sp

    def __init__(self, parser, logger, config, args):
        self.logger = logger
        self.args = args
        self.parser = parser
        self.config = config

        self.values = {
            'increase_cmd': 'xbacklight -inc %d',
            'decrease_cmd': 'xbacklight -dec %d',
            'set_cmd': 'xbacklight -set %d',
            'get_cmd': 'xbacklight -get',
            'icon-low': 'notification-display-brightness-low',
            'icon-medium': 'notification-display-brightness-medium',
            'icon-high': 'notification-display-brightness-high',
            'icon-full': 'notification-display-brightness-full',
        }

        for k, v in self.config.items():
            if k in self.values:
                self.values[k] = v

    def run(self):
        if not self.args.lightcommand:
            self.parser.print_help(sys.stderr)
            return
        if self.args.lightcommand == 'inc':
            self.logger.info('Increase brightness of %d%%' % self.args.value)
            check_output(self.values['increase_cmd'] % (self.args.value), shell=True)
        elif self.args.lightcommand == 'dec':
            self.logger.info('Decrease brightness of %d%%' % self.args.value)
            check_output(self.values['decrease_cmd'] % (self.args.value), shell=True)
        else:
            self.logger.info('Set brightness to %d%%' % self.args.value)
            check_output(self.values['set_cmd'] % (self.args.value), shell=True)

        current_value = int(float(check_output(self.values['get_cmd'], shell=True)))
        if current_value < 50:
            icon = self.values['icon-low']
        elif current_value < 75:
            icon = self.values['icon-medium']
        elif current_value < 100:
            icon = self.values['icon-high']
        else:
            icon = self.values['icon-full']
        Notification.sendNotification("Brightness", icon, current_value)

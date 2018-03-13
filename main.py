#!/usr/bin/env python3

import os
import sys
import glob
import logging
import argparse
import importlib
import configparser

sys.path.append(os.path.realpath('.'))

parser = argparse.ArgumentParser()

parser.add_argument('--settings-file', default='~/.config/i3_tools.ini')
parser.add_argument('--log-verbosity', type=str, default="DEBUG",
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])

subs = parser.add_subparsers(dest='command')

modules = {}

def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalpha())
    return output

modules_path = os.path.abspath(os.path.join(__file__, '../', 'modules'))
for module in glob.glob(os.path.join(modules_path, '*.py')):
    module_name = module.split(os.path.sep)[-1].split('.')[0]
    m = importlib.import_module('modules.' + module_name, package=None)
    m_class = getattr(m, camelCase(module_name))
    try:
        args_method = getattr(m_class, "arguments_parser")
    except:
        continue
    if callable(args_method):
        modules[module_name] = (m_class, args_method(subs))

args = parser.parse_args()

logger = logging.getLogger("i3_tools")
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)s -- %(levelname)s -- %(message)s")
handler.setFormatter(formatter)

logger.setLevel(getattr(logging, args.log_verbosity))
logger.addHandler(handler)

config = configparser.RawConfigParser()
settings = config.read(args.settings_file)

if args.command is None:
    parser.print_help(sys.stderr)
else:
    module, parser = modules[args.command]
    cmd = module(parser, logger, config[args.command] if args.command in config else {}, args)
    cmd.run()

#!/usr/local/bin/python3
""" Entrypoint to Simdem """
import configparser
import logging
import argparse
import os

from simdem.executor import bash
from simdem.parser import ast, simdem1
from simdem.mode import demo, dump


def main():
    """ Main execution function """
    argp = argparse.ArgumentParser()
    argp.add_argument('file', metavar='file',
                      help='file to process')
    argp.add_argument('--debug', '-d', action="store_true",
                      help="Turn on logging to console")
    argp.add_argument('--config-file', '-c', default="content/config/demo.ini",
                      help="Config file to use")
    argp.add_argument('--renderer', '-r', default="demo",
                      help="Render class to use", choices=['demo'])
    argp.add_argument('--mode', '-m', default="demo",
                      help="Mode to use", choices=['demo', 'dump'])
    argp.add_argument('--parser', '-p', default="simdem1",
                      help="Parser class to use", choices=['simdem1', 'ast'])
    argp.add_argument('--executor', '-e', default="bash",
                      help="Executor class to use", choices=['bash'])
    options = argp.parse_args()

    file_path = options.file
    validate_error = validate(options, file_path)
    if validate_error:
        print(validate_error)
        exit(1)

    config = configparser.ConfigParser()
    config.read(options.config_file)

    setup_logging(config, options)

    mode = get_mode(options, config)
    mode.process_file(file_path)

def validate(options, file_path):
    """ validate all passed in arguments """
    if not os.path.isfile(file_path):
        return "Unable to find file: " + file_path

    if not os.path.isfile(options.config_file):
        return "Unable to find config file: " + options.config_file

def get_mode(options, config):
    """ Returns correct renderer object """
    if options.mode == 'demo':
        return demo.DemoMode(config, get_parser(options), get_executor(options))

    if options.mode == 'dump':
        return dump.DumpMode(config, get_parser(options))

def get_parser(options):
    """ Returns correct parser object """
    if options.parser == 'ast':
        return ast.AstParser()
    elif options.parser == 'simdem1':
        return simdem1.SimDem1Parser()

def get_executor(options):
    """ Returns correct executor object """
    if options.executor == 'bash':
        return bash.BashExecutor()

def setup_logging(config, options):
    """ Establishes logging level and format """
    log_formatter = logging.Formatter(config.get('LOG', 'FORMAT', raw=True))
    root_logger = logging.getLogger()
    root_logger.setLevel(config.get('LOG', 'LEVEL'))

    file_handler = logging.FileHandler(config.get('LOG', 'FILE'))
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    if options.debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

main()

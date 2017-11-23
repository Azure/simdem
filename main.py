#!/usr/local/bin/python3
from simdem import core
from simdem.render import demo
import os
import sys
import mistune
import logging
import optparse
import configparser

def main():
    p = optparse.OptionParser("%prog <options> file", version="%prog 1.0")
    p.add_option('--debug', '-d', action="store_true",
                 help="Turn on logging to console")
    p.add_option('--config-file', '-f', default="content/config/demo.ini",
                 help="Config file to use")
    p.add_option('--render', '-r', default="demo",
                 help="Render class to use")
    p.add_option('--lexer', '-l', default="mistune.BlockLexer",
                 help="Lexer class to use")
    options, arguments = p.parse_args()

    validate_error = validate(options, arguments)
    if validate_error:
        print(validate_error)
        exit(1)

    config = configparser.ConfigParser()
    config.read(options.config_file)

    setup_logging(config, options)

    simdem = core.Core(config, get_render(options), get_lexer(options))

    file_path = arguments[0]
    simdem.process_file(file_path)

def validate(options, arguments):
    if len(arguments) != 1:
        return "Must provide one and only one argument: " + str(arguments)

    file_path = arguments[0]
    if not os.path.isfile(file_path):
        return "Unable to find file: " + file_path

    if not os.path.isfile(options.config_file):
        return "Unable to find config file: " + options.config_file

    if options.render not in ['demo']:
        return "Unknown Render: " + options.render
    
    if options.lexer not in ['mistune.BlockLexer']:
        return "Unknown Lexer: " + options.lexer

def get_render(options):
    if options.render == 'demo':
        return demo.Demo()

def get_lexer(options):
    if options.lexer == 'mistune.BlockLexer':
        return mistune.BlockLexer()

def setup_logging(config, options):
    logFormatter = logging.Formatter(config.get('LOG', 'FORMAT', raw=True))
    rootLogger = logging.getLogger()
    rootLogger.setLevel(config.get('LOG', 'LEVEL'))

    fileHandler = logging.FileHandler(config.get('LOG', 'FILE'))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    if options.debug:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

main()
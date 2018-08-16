#!/usr/local/bin/python3
""" Entrypoint to Simdem """
import configparser
import logging
import argparse
import os
import pkg_resources

from simdem.executor import bash
from simdem.parser import ast, simdem1
from simdem.mode import demo, dump, test, tutorial, cleanup
from simdem.ui import basic, color

def main():
    """ Main execution function """
    argp = argparse.ArgumentParser(prog='simdem')
    argp.add_argument('file', metavar='file',
                      help='file to process')
    argp.add_argument('--debug', '-d', action="store_true",
                      help="Turn on logging to console")
    argp.add_argument('--config-file', '-c',
                      help="Config file to use")
    argp.add_argument('--mode', '-m', default="tutorial",
                      help="Mode to use", choices=['demo', 'dump', 'test', 'tutorial', 'cleanup'])
    argp.add_argument('--parser', '-p', default="simdem1",
                      help="Parser class to use", choices=['simdem1', 'ast'])
    argp.add_argument('--shell', '-s', default="bash",
                      help="Shell class to use", choices=['bash'])
    argp.add_argument('--environment', '-e', default='',
                      help="Environment variables to inject (Example: -e FOO=foo1,BAR=bar1)")
    argp.add_argument('--boot-strap', '-b', default=None,
                      help="Boot strap script to execute")
    argp.add_argument('--ui', '-u', default='color',
                      help="UI class to use", choices=['basic', 'color'])
    argp.add_argument('--override-config', metavar='override',
                      help="Override setting in config file")
    version = pkg_resources.require("simdem")[0].version
    argp.add_argument('--version', action='version', version='%(prog)s ' + version,
                      help="Display SimDem's version number")
    options = argp.parse_args()

    file_path = options.file
    config_file_path = get_config_file_path(options)
    validate(file_path, config_file_path)

    config = configparser.ConfigParser()
    config.read(config_file_path)
    inject_config_options(options, config)

    setup_logging(config, options)

    mode = get_mode(options, config)

    # Add user's home directory to path
    mode.process_command("export HOME=" + os.path.expanduser("~"))

    if options.environment:
        commands = options.environment.split(',')
        mode.process_commands(commands)

    if options.boot_strap:
        mode.run_setup_script(options.setup_script)

    mode.process_file(file_path)

def get_config_file_path(options):
    """ Returns the found config file path """
    options_config_file = options.config_file
    if options_config_file:
        return options_config_file
    file_path = pkg_resources.resource_filename(__name__, 'simdem.ini')
    return file_path

def inject_config_options(options, config):
    """ Injects CLI arguments into config settings """
    if options.override_config:
        [key, value] = options.override_config.split('=')
        [section, option] = key.split('.')
        config.set(section, option, value)

def validate(file_path, config_file_path):
    """ validate all passed in arguments """
    if not os.path.isfile(file_path):
        raise FileNotFoundError('Unable to find file: ' + file_path)

    if not os.path.isfile(config_file_path):
        raise FileNotFoundError('Unable to find config file: ' + config_file_path)

def get_mode(options, config):
    """ Returns correct renderer object """

    parser = get_parser(options)
    shell = get_shell(options)
    ui = get_ui(options, config)

    if options.mode == 'demo':
        return demo.DemoMode(config, parser, shell, ui)

    if options.mode == 'dump':
        return dump.DumpMode(config, parser, shell, ui)

    if options.mode == 'cleanup':
        return cleanup.CleanupMode(config, parser, shell, ui)

    if options.mode == 'test':
        return test.TestMode(config, parser, shell, ui)

    if options.mode == 'tutorial':
        return tutorial.TutorialMode(config, parser, shell, ui)

def get_ui(options, config):
    """ return UI object """
    if options.ui == 'basic':
        return basic.BasicUI(config)
    elif options.ui == 'color':
        return color.ColorUI(config)

def get_parser(options):
    """ Returns correct parser object """
    if options.parser == 'ast':
        return ast.AstParser()
    elif options.parser == 'simdem1':
        return simdem1.SimDem1Parser()

def get_shell(options):
    """ Returns correct shell object """
    if options.shell == 'bash':
        return bash.BashExecutor()

def setup_logging(config, options):
    """ Establishes logging level and format """
    log_formatter = logging.Formatter(config.get('log', 'format', raw=True))
    root_logger = logging.getLogger()
    root_logger.setLevel(config.get('log', 'level'))

    file_handler = logging.FileHandler(config.get('log', 'file'))
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    if options.debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

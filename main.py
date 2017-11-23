from simdem import core
import os
import sys
import logging
import optparse
import configparser

def main():
    p = optparse.OptionParser("%prog <options> file", version="%prog 1.0")
    p.add_option('--debug', '-d', action="store_true",
                 help="Turn on logging to console")
    p.add_option('--config-file', '-f', default="content/config/demo.ini",
                 help="Config file to use")
    options, arguments = p.parse_args()

    validate_error = validate(options, arguments)
    if validate_error:
        print(validate_error)
        exit(1)

    config = configparser.ConfigParser()
    config.read(options.config_file)

    setup_logging(config, options)

    simdem = core.Core()

    file_path = arguments[0]
    simdem.process_file(file_path)

def validate(options, arguments):
    if len(arguments) != 1:
        return "Must provide one and only one argument: " + str(arguments)

    file_path = arguments[0]
    if not os.path.isfile(file_path):
        return "Unable to find file " + file_path

    if not os.path.isfile(options.config_file):
        return "Unable to find config file " + options.config_file


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
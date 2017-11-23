from simdem import core,config
import os
import sys
import logging
import optparse

def main():
    p = optparse.OptionParser("%prog <options> file", version=config.SIMDEM_VERSION)
    p.add_option('--debug', '-d', action="store_true",
                 help="Turn on logging to console")
    options, arguments = p.parse_args()

    validate_error = validate(options, arguments)
    if validate_error:
        print(validate_error)
        exit(1)

    setup_logging(options)

    simdem = core.Core()

    file_path = arguments[0]
    simdem.process_file(file_path)

def validate(options, arguments):
    if len(arguments) != 1:
        return "Must provide one and only one argument: " + str(arguments)

    file_path = arguments[0]
    if not os.path.isfile(file_path):
        return "Unable to find file " + file_pathu

def setup_logging(options):
    logFormatter = logging.Formatter(config.LOG_FORMAT)
    rootLogger = logging.getLogger()
    rootLogger.setLevel(config.LOG_LEVEL)

    fileHandler = logging.FileHandler(config.LOG_FILE)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    if options.debug:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

main()
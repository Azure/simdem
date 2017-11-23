from simdem import core,config
import os
import logging
import optparse

def main():
    p = optparse.OptionParser("%prog <options> file", version=config.SIMDEM_VERSION)
    p.add_option('--debug', '-d', default="False",
                 help="Turn on debug logging by setting to True.")
    options, arguments = p.parse_args()

    validate_error = validate(options, arguments)
    if validate_error:
        print(validate_error)
        exit(1)

    logging.basicConfig(filename=config.LOG_FILE,level=config.LOG_LEVEL)

    simdem = core.Core()

    file_path = arguments[0]
    simdem.process_file(file_path)

def validate(options, arguments):
    if len(arguments) != 1:
        return "Must provide one and only one argument: " + str(arguments)

    file_path = arguments[0]
    if not os.path.isfile(file_path):
        return "Unable to find file " + file_path

main()
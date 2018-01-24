""" Debug renderer for SimDem"""

import logging
import json
import configparser
from simdem.mode.common import ModeCommon

class DumpMode(ModeCommon): # pylint: disable=R0903
    """ This class is used to pretty print a parsed file """

    def process_file(self, file_path, is_prereq=False):
        """ Parse the file and print it.  Not very exciting. """
        logging.debug("parse_file(file_path=" + file_path + ", is_prereq=" + str(is_prereq))
        steps = self.parser.parse_file(file_path)
        print(json.dumps(steps, indent=4, sort_keys=True))

    def print_config_data(self):
        """ Dead code for now, but useful for debugging config """
        print("Config=")
        for section in self.config.sections():
            for option in self.config.options(section):
                try:
                    print(section + '.' + option + '=' + str(self.config.get(section, option)))
                except configparser.InterpolationMissingOptionError:
                    pass
        print()

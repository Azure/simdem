""" Debug renderer for SimDem"""

import pprint
import logging
from simdem.mode.common import ModeCommon

class DumpMode(ModeCommon): # pylint: disable=R0903
    """ This class is used to pretty print a parsed file """

    def process_file(self, file_path, is_prereq=False):
        """ Parse the file and print it.  Not very exciting. """
        logging.debug("parse_file(file_path=" + file_path + ", is_prereq=" + str(is_prereq))
        steps = self.parser.parse_file(file_path)
        pprint.pprint(steps)

""" Debug renderer for SimDem"""

import pprint
from simdem.mode.common import ModeCommon

class DumpMode(ModeCommon): # pylint: disable=R0903
    """ This class is used to pretty print a parsed file """

    def process_file(self, file_path):
        """ Parse the file and print it.  Not very exciting. """
        steps = self.parser.parse_file(file_path)
        pprint.pprint(steps)

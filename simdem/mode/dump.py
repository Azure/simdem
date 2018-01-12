""" Debug renderer for SimDem"""

import pprint

class DumpMode(object): # pylint: disable=R0903
    """ This class is used to pretty print a parsed file """

    config = None
    parser = None

    def __init__(self, config, parser):
        self.config = config
        self.parser = parser

    def process_file(self, file_path):
        """ Parse the file and print it.  Not very exciting. """
        steps = self.parser.parse_file(file_path)
        pprint.pprint(steps)

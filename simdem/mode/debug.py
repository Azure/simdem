"""Demo (default) renderer for SimDem"""

import pprint

class DebugMode(object):
    """ This class is used to render the output of the commands into something
        that looks like you're typing
    """
    config = None
    parser = None

    def __init__(self, config, parser):
        self.config = config
        self.parser = parser

    def process_file(self, file_path):
        steps = self.parser.parse_file(file_path)
        pprint.pprint(steps)

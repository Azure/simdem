""" Common mode for SimDem mode """

class ModeCommon(object):
    """ This class is designed to hold any shared code across modes
    """
    config = None
    executor = None
    parser = None

    def __init__(self, config, parser, executor):
        self.config = config
        self.parser = parser
        self.executor = executor

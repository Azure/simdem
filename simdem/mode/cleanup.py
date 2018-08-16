""" Automated mode for SimDem """

import logging
from simdem.mode.common import ModeCommon

class CleanupMode(ModeCommon):
    """ This class is the SimDem Cleanup mode
    """

    def process(self, steps):
        """ I'd like to use a dispatcher for this; however, we need to exit processing
            if the validation fails. """
        logging.debug("process()")
        if 'cleanup' in steps:
            self.process_commands(steps['cleanup']['commands'])

    def process_next_steps(self, steps, start_path):
        """ No need to display next steps if in test mode """
        pass

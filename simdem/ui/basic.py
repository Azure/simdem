""" Basic Render Class """

import os
import sys
from simdem.misc.getch import Getch
from simdem.ui.common import CommonUI

class BasicUI(CommonUI):
    """ No frills, no thrills render object """

    def __init__(self, config):
        self.config = config

""" Basic Render Class """

import os
import sys
from simdem.misc.getch import Getch

class BasicUI(object):
    """ No frills, no thrills render object """

    def __init__(self, config):
        self.config = config

    @staticmethod
    def get_single_key_input():
        """ SimDem1 uses this method:
            https://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
            For SimDem2, I'm trying this alternative to allow for Windows compatibility
            https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user/510404#510404

            https://stackoverflow.com/questions/1077113/how-do-i-detect-whether-sys-stdout-is-attached-to-terminal-or-not
            Might need to allow config override of the conditional by allowing a config variable.
            Experienced an issue where it hung running in a container and I didn't completely debug
        """

        if sys.stdout.isatty():
            getch = Getch()
            return getch.impl()
        return

    @staticmethod
    def get_line_input(prompt):
        """ Request single line from user """
        return input(prompt)

    @staticmethod
    def println(output=''):
        print(output, flush=True)

    @staticmethod 
    def print(output=''):
        print(output, end="", flush=True)

    def print_validation_failed(self):
        self.println('***PREREQUISITE VALIDATION FAILED***')

    @staticmethod
    def clear():
        # https://www.quora.com/Is-there-a-Clear-screen-function-in-Python
        #print("\033[H\033[J")
        if sys.stdout.isatty():
            os.system('clear')

    def print_test_passed(self):
        self.println('*** SIMDEM TEST RESULT PASSED ***')
    
    def print_test_failed(self):
        self.println('*** SIMDEM TEST RESULT FAILED ***')

    def print_heading(self, content, level):
        """ Print out the heading exactly as we found it """
        self.println(level * '#' + ' ' + content)
        self.print_break()

    def print_prompt(self):
        self.print(self.config.get('render', 'console_prompt', raw=True) + ' ')
    
    def print_cmd(self, cmd):
        self.print(cmd)
    
    def print_result(self, result):
        self.print(result)
    
    def print_break(self):
        self.println()
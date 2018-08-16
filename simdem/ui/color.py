""" Basic Render Class """

import os
import sys
import colorama
from simdem.misc.getch import Getch
from simdem.ui.common import CommonUI

colorama.init(strip=None)

class ColorUI(CommonUI):
    """ No frills, no thrills render object """

    def __init__(self, config):
        self.config = config

    def println(self, output='', color=colorama.Fore.WHITE + colorama.Style.BRIGHT):
        self.display(output, color=color)

    def print(self, output='', color=None):
        self.display(output, end="", flush=True, color=color)

    def print_validation_failed(self):
        self.println('***PREREQUISITE VALIDATION FAILED***', color=colorama.Fore.RED + colorama.Style.BRIGHT)

    @staticmethod
    def clear():
        # https://www.quora.com/Is-there-a-Clear-screen-function-in-Python
        #print("\033[H\033[J")
        if sys.stdout.isatty():
            os.system('clear')

    def print_test_passed(self):
        self.println('*** SIMDEM TEST RESULT PASSED ***', color=colorama.Fore.GREEN + colorama.Style.BRIGHT)
    
    def print_test_failed(self):
        self.println('*** SIMDEM TEST RESULT FAILED ***', color=colorama.Fore.RED + colorama.Style.BRIGHT)

    def print_heading(self, content, level):
        """ Print out the heading exactly as we found it """
        self.println(level * '#' + ' ' + content, color=colorama.Fore.CYAN + colorama.Style.BRIGHT)
        self.print_break()

    def print_prompt(self):
        self.print(self.config.get('render', 'console_prompt', raw=True) + ' ', color=colorama.Fore.WHITE)
    
    def print_cmd(self, cmd):
        self.print(cmd, color=colorama.Fore.WHITE + colorama.Style.BRIGHT)
    
    def print_result(self, result):
        self.print(result, color=colorama.Fore.GREEN + colorama.Style.BRIGHT)
    
    def print_break(self):
        self.println()

    def display(self, text, color=None, flush=False, end='\n'):
        """ Display some text in a given color. Do not print a new line unless
            new_line is set to True.
        """
        if color:
            print(color, end="")
        print(text, end=end, flush=flush)
        if color:
            print(colorama.Style.RESET_ALL, end="")
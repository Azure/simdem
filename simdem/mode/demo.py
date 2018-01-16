"""Demo (default) mode for SimDem"""

import random
import time
from simdem.mode.common import ModeCommon

class DemoMode(ModeCommon):
    """ This class is the default SimDem file processor.
        It's designed for running files in a demo-able mode that looks like a human is typing it
    """

    def process_file(self, file_path):
        """ Parses the file and starts processing it """
        #print("*** Processing " + file_path + " ***")
        steps = self.parser.parse_file(file_path)
        self.process(steps)
        #print("*** Completed Processing " + file_path + " ***")

    def process(self, steps):
        """ Parses the file and starts processing it """

        """ I'd like to use a dispatcher for this; however, we need to exit processing
            if the validation fails. """
        for step in steps:
            if step['type'] == 'commands':
                self.process_commands(step)
            elif step['type'] == 'prerequisites':
                for prereq_file in step['content']:
                    self.process_file(prereq_file)

    def process_commands(self, step):
        """ Pretend to type the command, run it and then display the output """
        for cmd in step['content']:
            self.type_command(cmd)
            results = self.executor.run_cmd(cmd)
            print(results, end="", flush=True)
        print()
        return results

    def type_command(self, cmd):
        """ Displays the command on the screen """

        # Must add ' ' when typing command because whitespaces are removed from configparser
        # https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
        print(self.config.get('RENDER', 'CONSOLE_PROMPT', raw=True) + ' ', end="", flush=True)
        for _, char in enumerate(cmd):
            if char != "\n":
                typing_delay = None #float(self.config.get('RENDER', 'TYPING_DELAY'))
                if typing_delay:
                    delay = random.uniform(0.02, typing_delay)
                    time.sleep(delay)
                print(char, end="", flush=True)
        print("", flush=True)

    @staticmethod
    def process_next_steps(steps):
        """ Is there a good way to test this that doesn't involve lots of test code + expect?
        """
        idx = 1
        if steps:
            print("Next steps available:")
            for step in steps:
                print(idx + ".) " + step['title'])
                idx += 1
            step_request = input("Which step do you want to take next?")
            if step_request:
                return steps[step_request+1]['target']
        return

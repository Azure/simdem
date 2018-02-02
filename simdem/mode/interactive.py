""" Interactive Mode Class """
import sys
import logging
from simdem.mode.common import ModeCommon
from simdem.misc.getch import Getch

class InteractiveMode(ModeCommon):
    """ Interactive Mode subclass """

    def process_commands(self, cmds):
        """ Pretend to type the command, run it and then display the output """
        for cmd in cmds:
            #  Request enter from user to know when to proceed
            key = self.get_single_key_input()
            self.process_command_input(key)
            self.display_command(cmd)
            results = self.executor.run_cmd(cmd)
            print(results, end="", flush=True)
        print()
        return results

    def process_command_input(self, key):
        """ Process the command input.  It's 4AM and I'm sleepy
            For now, just return.  We'll implement that later """
        return key

    def display_command(self, cmd):
        """ Default result for displaying a command """
        print(self.config.get('render', 'console_prompt', raw=True) + ' ' + cmd, flush=True)

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

    def process_next_steps(self, next_steps, start_path):
        """ Is there a good way to test this that doesn't involve lots of test code + expect?
            Not fully tested yet.  Low priority feature.
        """
        idx = 1
        if next_steps:
            print("Next steps available:")
            for step in next_steps:
                print(str(idx) + ". " + step['title'] + " (" + step['target'] + ") ")
                idx += 1
            print()
            # https://stackoverflow.com/questions/1077113/how-do-i-detect-whether-sys-stdout-is-attached-to-terminal-or-not
            if sys.stdout.isatty():
                # You're running in a real terminal
                in_string = ""
                in_value = 0

                while in_value < 1 or in_value > len(next_steps):
                    in_string = input("Choose a step.  " +
                                      "Enter a value between 1 and " +
                                      str(len(next_steps)) + " or 'quit' ")
                    if in_string.lower() == "quit" or in_string.lower() == "q":
                        return
                    try:
                        in_value = int(in_string)
                    except ValueError:
                        pass

                #print('You chose:' + str(steps[int(step_request) - 1]['title']))
                self.process_file(start_path + '/' + next_steps[int(in_string) - 1]['target'])
            else:
                logging.info('Not connected to a TTY terminal  Not requesting input.')
                # You're being piped or redirected
        return

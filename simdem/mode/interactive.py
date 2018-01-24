""" Interactive Mode Class """
import sys
import logging
from simdem.mode.common import ModeCommon
from simdem.misc.getch import Getch

class InteractiveMode(ModeCommon):
    """ Interactive Mode subclass """

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

    def process_next_steps(self, steps, start_path):
        """ Is there a good way to test this that doesn't involve lots of test code + expect?
            Not fully tested yet.  Low priority feature.
        """
        idx = 1
        if steps:
            print("Next steps available:")
            for step in steps:
                print(str(idx) + ". " + step['title'] + " (" + step['target'] + ") ")
                idx += 1
            print()
            # https://stackoverflow.com/questions/1077113/how-do-i-detect-whether-sys-stdout-is-attached-to-terminal-or-not
            if sys.stdout.isatty():
                # You're running in a real terminal
                step_request = input("Choose a step.  " +
                                     "Type the # or 'q' to quit and then press Enter: ")
                #print('You chose:' + str(steps[int(step_request) - 1]['title']))
                self.process_file(start_path + '/' + steps[int(step_request) - 1]['target'])
            else:
                logging.info('Not connected to a TTY terminal  Not requesting input.')
                # You're being piped or redirected
        return

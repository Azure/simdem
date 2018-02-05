""" Interactive Mode Class """
import sys
import logging
from collections import deque
from simdem.mode.common import ModeCommon

class InteractiveMode(ModeCommon):
    """ Interactive Mode subclass """

    def process_commands(self, cmds):
        """ Loop through the commands to run as well as expect interrupt logic from the user """
        result = None
        cmd = None
        cmd_deque = deque(cmds)
        # https://twitter.com/sandwich_cool/status/956932558847176704
        # The "I smell danger" picture is never truer than now
        # This statement is written in VSCode while I work for MSFT
        while True:
            self.display_prompt()
            key = self.ui.get_single_key_input()
            result = self.process_command_input(key, last_command=cmd)
            logging.debug(cmd_deque)
            if result:
                continue
            elif cmd_deque:
                cmd = cmd_deque.popleft()
                result = self.run_command(cmd)
            if not cmd_deque:
                break
        return result

    def run_command(self, cmd):
        """ Pretend to type the command, run it and then display the output """
        #  Request enter from user to know when to proceed
        logging.debug('run_command(' + cmd + ')')
        self.display_command(cmd)
        results = self.executor.run_cmd(cmd)
        self.ui.print(results)
        return results

    def process_command_input(self, key, last_command=None):
        """ Process the command input.  It's 4AM and I'm sleepy
            For now, just return.  We'll implement that later """
        result = None
        if key == 'b':
            logging.debug('Received Break request')
            self.ui.print("\nshell> ")
            command = self.ui.get_line_input()
            if command != "":
                result = self.executor.run_cmd(command)
                self.ui.print(result)
        elif key == 'r':
            logging.debug('Received Run last command request')
            if last_command:
                result = self.run_command(last_command)
        logging.debug('Output=' + str(result))
        return result
        # Otherwise, we will return and assume the user wants to continue

    def display_prompt(self):
        """ Default result for displaying a command """
        self.ui.print(self.config.get('render', 'console_prompt', raw=True) + ' ')

    def display_command(self, cmd):
        """ Default result for displaying a command """
        self.ui.println(cmd)

    def process_next_steps(self, next_steps, start_path):
        """ Is there a good way to test this that doesn't involve lots of test code + expect?
            Not fully tested yet.  Low priority feature.
        """
        idx = 1
        if next_steps:
            self.ui.println("Next steps available:")
            for step in next_steps:
                self.ui.println(str(idx) + ". " + step['title'] + " (" + step['target'] + ") ")
                idx += 1
            self.ui.println()
            # https://stackoverflow.com/questions/1077113/how-do-i-detect-whether-sys-stdout-is-attached-to-terminal-or-not
            if sys.stdout.isatty():
                # You're running in a real terminal
                in_string = ""
                in_value = 0

                while in_value < 1 or in_value > len(next_steps):
                    prompt = "Choose a step.  Enter a value between 1 and " + \
                             str(len(next_steps)) + " or 'q' to quit: "
                    in_string = self.ui.get_line_input(prompt)
                    if in_string.lower() == "quit" or in_string.lower() == "q":
                        return
                    try:
                        in_value = int(in_string)
                    except ValueError:
                        pass

                self.process_file(start_path + '/' + next_steps[int(in_string) - 1]['target'])
            else:
                logging.info('Not connected to a TTY terminal  Not requesting input.')
                # You're being piped or redirected
        return

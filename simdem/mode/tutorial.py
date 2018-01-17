""" Tutorial mode for SimDem"""

from simdem.mode.common import ModeCommon

class TutorialMode(ModeCommon):
    """ This class is the tutorial mode class for SimDem.
        It's designed for running files in a tutorial mode which Displays the descriptive text
        of the tutorial and pauses at code blocks to allow user interaction.
    """

    def process_file(self, file_path):
        """ Parses the file and starts processing it """
        #print("*** Processing " + file_path + " ***")
        steps = self.parser.parse_file(file_path)

        """ I'd like to use a dispatcher for this; however, we need to exit processing
            if the validation fails. """
        if 'prerequisites' in steps:
            for prereq_file in steps['prerequisites']:
                self.process_file(prereq_file)

        for step in steps['body']:
            if step['type'] == 'heading':
                self.process_heading(step)
            elif step['type'] == 'text':
                self.process_text(step)
            elif step['type'] == 'commands':
                self.process_commands(step)

    @staticmethod
    def process_heading(step):
        """ Print out the heading exactly as we found it """
        print(step['level'] * '#' + ' ' + step['content'])
        print()

    @staticmethod
    def process_text(step):
        """ Print out the text exactly as we found it """
        print(step['content'])
        print()

    def process_commands(self, step):
        """ Pretend to type the command, run it and then display the output """
        for cmd in step['content']:
            print(self.config.get('RENDER', 'CONSOLE_PROMPT', raw=True) + ' ' + cmd)
            results = self.executor.run_cmd(cmd)
            print(results, end="", flush=True)
        print()
        return results

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

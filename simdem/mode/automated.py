"""Demo (default) mode for SimDem"""

from simdem.mode.common import ModeCommon

class AutomatedMode(ModeCommon):
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
        last_command_result = None

        """ I'd like to use a dispatcher for this; however, we need to exit processing
            if the validation fails. """
        for step in steps:
            if step['type'] == 'heading':
                self.process_heading(step)
            elif step['type'] == 'text':
                self.process_text(step)
            elif step['type'] == 'commands':
                last_command_result = self.process_commands(step)
#            elif step['type'] == 'result':
#                if self.is_result_valid(step['content'], last_command_result):
#                    print('***VALIDATION PASSED***')
#                else:
#                    print('***VALIDATION FAILED***')
            elif step['type'] == 'prerequisites':
                for prereq_file in step['content']:
                    self.process_file(prereq_file)
            elif step['type'] == 'validation_command':
                last_command_result = self.process_commands(step)
            elif step['type'] == 'validation_result':
                if self.is_result_valid(step['content'], last_command_result):
#                    print('***VALIDATION PASSED***')
                    return
#                else:
#                    print('***VALIDATION FAILED***')

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
            print(cmd, end="", flush=True)
            results = self.executor.run_cmd(cmd)
            print(results, end="", flush=True)
        print()
        return results

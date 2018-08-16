""" Common mode for SimDem mode """

import os
import logging
import difflib
import pathlib

class ModeCommon(object): # pylint: disable=R0903
    """ This class is designed to hold any shared code across modes
    """
    config = None
    executor = None
    parser = None
    render = None

    def __init__(self, config, parser, executor, ui):
        self.config = config
        self.parser = parser
        self.executor = executor
        self.ui = ui 

    def run_setup_script(self, file_path):
        """ Runs setup script """
        logging.debug("run_setup_script(" + file_path + ")")

        cmd = '. ' + file_path
        self.ui.print_prompt()
        self.print_command(cmd)
        self.ui.print_break()
        result = self.executor.run_cmd(cmd)
        self.ui.print_result(result)
        self.ui.print_break()

    def process_file(self, file_path, is_prereq=False, toc={}):
        """ Parses the file and starts processing it """
        logging.debug("parse_file(file_path=" + file_path + ", is_prereq=" + str(is_prereq))
        # Change the working directory in case of any recursion
        start_path = os.path.dirname(os.path.abspath(file_path))

        self.setup_temp_dir()
        logging.debug('parse_file::start_path=' + start_path)
        steps = self.parser.parse_file(file_path, is_prereq)

        # https://github.com/Azure/simdem/issues/92
        env_file = start_path + '/./env.sh'
        if os.path.isfile(env_file):
            self.process_env_file(env_file)

        # We want to inherit the parent's TOC to reduce the # of copies needed 
        if toc:
            logging.debug('Adding parent POC')
            steps['toc'] = toc
            logging.debug(steps)

        #  Begin preqreq processing
        if 'prerequisites' in steps:
            for prereq_file in steps['prerequisites']:
                # Change the working directory in case of any recursion
                self.process_file(start_path + '/' + prereq_file, is_prereq=True)
        if is_prereq and 'validation' in steps:
            last_command_result = self.process_commands(steps['validation']['commands']) # pylint: disable=no-member
            if 'expected_result' in steps['validation']:
                if self.is_result_valid(steps['validation']['expected_result'],
                                        last_command_result):
                    return
                else:
                    self.ui.print_validation_failed()
        #  End prereq processing

        if start_path:
            self.executor.run_cmd('cd ' + start_path)
        self.process(steps) # pylint: disable=no-member

        if 'toc' in steps:
            self.process_next_steps(steps['toc'], start_path) # pylint: disable=no-member

    def process_env_file(self, env_file):
        """ Run the env file.  Assumes it exists """
        logging.debug('process_env_file(' + env_file + ')')
        env_fh = open(env_file)
        env_contents = env_fh.readlines()
        env_fh.close()
        self.process_commands(env_contents)

    def process_commands(self, cmds, display=True):
        """ Pretend to type the command, run it and then display the output """
        for cmd in cmds:
            result = self.process_command(cmd, display=display)
        if display:
            self.ui.print_break()
        return result

    def process_command(self, cmd, display=True):
        """ Process single command """
        if display:
            self.ui.print_prompt()
            self.print_command(cmd)
            self.ui.print_break()
        result = self.executor.run_cmd(cmd)
        if display:
            self.ui.print_result(result)
        return result

    def print_command(self, cmd):
        """ Default action to print the command is to just call the UI. """
        self.ui.print_cmd(cmd)

    @staticmethod
    def is_result_valid(expected_results, actual_results, expected_similarity=0.8):
        """Checks to see if a command execution passes.
        If actual results compared to expected results is within
        the expected similarity level then it's considered a pass.

        expected_similarity = 1.0 could be a breaking change for older SimDem scripts.
        explicit fails > implicit passes
        Ross may disagree with me.  Let's see how this story unfolds.
        """

        if not actual_results:
            logging.error("is_result_valid(): actual_results is empty.")
            return False

        logging.debug("is_result_valid(" + expected_results + "," + actual_results + \
            "," + str(expected_similarity) + ")")

        expected_results_str = expected_results.rstrip()
        actual_results_str = actual_results.rstrip()
        logging.debug("is_result_valid(" + expected_results_str + "," + actual_results_str + \
            "," + str(expected_similarity) + ")")
        seq = difflib.SequenceMatcher(lambda x: x in " \t\n\r",
                                      actual_results_str,
                                      expected_results_str)

        is_pass = seq.ratio() >= expected_similarity

        if is_pass:
            logging.info("is_result_valid passed")

        else:
            logging.error("is_result_valid failed")
            logging.error("actual_results = " + actual_results)
            logging.error("expected_results = " + expected_results)

        return is_pass

    def setup_temp_dir(self):
        """ https://github.com/Azure/simdem/issues/104 """
        directory = str(pathlib.Path.home()) + '/' + self.config.get('main', 'temp_dir', raw=True)
        logging.info("temp_dir=" + directory)
        self.process_command("mkdir -p " + directory, display=False)
        self.process_command("export SIMDEM_TEMP_DIR=" + directory, display=False)
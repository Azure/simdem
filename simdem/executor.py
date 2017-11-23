import pexpect
import time
import logging
from pexpect import replwrap

PEXPECT_PROMPT = u'[PEXPECT_PROMPT>'
PEXPECT_CONTINUATION_PROMPT = u'[PEXPECT_PROMPT+'

class Executor(object):
    _shell = None
    _env = None

    def __init__(self):
        pass


    def run_cmd(self, command=None):
        command = command.strip()
        logging.debug("Execute command: '" + command + "'")
        start_time = time.time()
        response = self.get_shell().run_command(command)
        end_time = time.time()
        # https://pexpect.readthedocs.io/en/stable/overview.html#find-the-end-of-line-cr-lf-conventions
        # Because pexpect respects TTY (which uses CRLF) instead of UNIX, we must swap out.  This might get tricky if we start supporting windows
        # This is because to easily write expected testcase output files, most unix-ish text editors write with \n
        response = response.replace("\r\n", "\n")
        logging.debug("Response: '" + response + "'")
        return response

    def get_shell(self):
        """Gets or creates the shell in which to run commands for the
        supplied demo
        """
        if self._shell == None:
            #  Should we use spawn or spawnu?
            child = pexpect.spawnu('/bin/bash', env=self._env, echo=False, timeout=None)
            ps1 = PEXPECT_PROMPT[:5] + u'\[\]' + PEXPECT_PROMPT[5:]
            ps2 = PEXPECT_CONTINUATION_PROMPT[:5] + u'\[\]' + PEXPECT_CONTINUATION_PROMPT[5:]
            prompt_change = u"PS1='{0}' PS2='{1}' PROMPT_COMMAND=''".format(ps1, ps2)
            self._shell = pexpect.replwrap.REPLWrapper(child, u'\$', prompt_change)
        return self._shell


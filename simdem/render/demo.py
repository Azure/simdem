from .. import helpers,executor

class Demo(object):
    _shell = None
    _env = None
    exe = None

    def __init__(self):
        self.exe = executor.Executor()
        pass

    def run_cmd(self, cmd):
        return self.exe.run_cmd(cmd)

# For managing the environment in which a SimDem demo executes.

import os
import sys
import json

import config

class Environment(object):
    def __init__(self, directory, copy_env=True, is_test=False):
        """Initialize the environment"""
        if copy_env:
            self.env = os.environ.copy()
        else:
            self.env = {}
        self.is_test = is_test
        self.read_simdem_environment(directory)
        self.set("SIMDEM_VERSION", config.SIMDEM_VERSION)
        self.set("SIMDEM_CWD", directory)
        temp_dir = os.path.expanduser(config.SIMDEM_TEMP_DIR)
        self.set("SIMDEM_TEMP_DIR", temp_dir)

    def read_simdem_environment(self, directory):
        """Populates each shell environment with a set of environment vars
        loaded via env.json and/or env.local.json files. Variables are
        loaded in order first from the parent of the current script
        directory, then the current scriptdir itself and finally from
        the directory in which the `simdem` command was executed (the
        CWD).

        Values are loaded in the following order, the last file to
        define a vlaue is the one that "wins".
        
        - PARENT_OF_SCRIPT_DIR/env.json
        - SCRIPT_DIR/env.json
        - PARENT_OF_SCRIPT_DIR/env.local.json
        - SCRIPT_DIR/env.local.json
        - CWD/env.json
        - CWD/env.local.json

        Note that it is possible to supply test values in an
        `env.test.json` file stored in the SCRIPT_DIR, its parent or
        the current working directory. If we are running in test mode
        then the following three files will be loaded, if they exist,
        in the following order at the end of the initialization
        procedure. This means they will take precedence over
        everything else.

        - PARENT_OF_SCRIPT_DIR/env.test.json
        - SCRIPT_DIR/env.test.json
        - CWD/env.json

        """
        env = {}

        if not directory.endswith('/'):
            directory = directory + "/"

        filename = directory + "../env.json"
        if os.path.isfile(directory + "../env.json"):
            with open(filename) as env_file:
                app_env = self.process_env(json.load(env_file))
                env.update(app_env)

        filename = directory + "env.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                script_env = self.process_env(json.load(env_file))
                env.update(script_env)

        filename = directory + "../env.local.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                local_env = self.process_env(json.load(env_file))
                env.update(local_env)

        filename = directory + "env.local.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                local_env = self.process_env(json.load(env_file))
                env.update(local_env)

        filename = "/env.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                local_env = self.process_env(json.load(env_file))
                env.update(local_env)

        filename = "env.local.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                local_env = self.process_env(json.load(env_file))
                env.update(local_env)

        if self.is_test:
            filename = directory + "../env.test.json"
            if os.path.isfile(filename):
                with open(filename) as env_file:
                    script_env = self.process_env(json.load(env_file))
                    env.update(script_env)

            filename = directory + "env.test.json"
            if os.path.isfile(filename):
                with open(filename) as env_file:
                    script_env = self.process_env(json.load(env_file))
                    env.update(script_env)

            filename = "env.test.json"
            if os.path.isfile(filename):
                with open(filename) as env_file:
                    local_env = self.process_env(json.load(env_file))
                    env.update(local_env)
                
        self.env.update(env)

    def process_env(self, new_env):
        """
        Takes an environmetn definition and processes it for use.
        For example, expand '~' to home directory.
        """
        for key in new_env:
            val = new_env[key]
            if val.startswith('~'):
                new_env[key] = os.path.expanduser(val)
        return new_env
        
    def set(self, var, value):
        """Sets a new variable to the environment"""
        self.env[var] = value

    def get(self, key=None):
        """Returns a either a value for a supplied key or, if key is None, a
           dictionary containing the current environment"""
        if key:
            return self.env[key]
        else:
            return self.env

    def get_script_file_name(self, script_dir):
        """
        Backwards compatibility for old script.md - https://github.com/Azure/simdem/issues/5
        """
        file_name = "README.md"
        if not os.path.exists(script_dir + file_name):
            file_name = "script.md"
        return file_name
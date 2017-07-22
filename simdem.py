#!/usr/bin/env python3

# This is a python script that emulates a terminal session and runs
# commands from a supplied markdown file..

import difflib
import optparse
import os
import pexpect
import pexpect.replwrap
import random
import re
import time
import shlex
import sys
import json
import colorama
colorama.init(strip=None)

SIMDEM_VERSION = "0.5.0"
PEXPECT_PROMPT = u'[PEXPECT_PROMPT>'
PEXPECT_CONTINUATION_PROMPT = u'[PEXPECT_PROMPT+'

class Environment(object):
    def __init__(self, directory, copy_env=True, is_test=False):
        """Initialize the environment"""
        if copy_env:
            self.env = os.environ.copy()
        else:
            self.env = {}
        self.is_test = is_test
        self.read_simdem_environment(directory)
        self.set("SIMDEM_VERSION", SIMDEM_VERSION)
        self.set("SIMDEM_CWD", directory)

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
                app_env = json.load(env_file)
                env.update(app_env)

        filename = directory + "env.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                script_env = json.load(env_file)
                env.update(script_env)

        filename = directory + "../env.local.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                local_env = json.load(env_file)
                env.update(local_env)

        filename = directory + "env.local.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                local_env = json.load(env_file)
                env.update(local_env)

        filename = "/env.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                local_env = json.load(env_file)
                env.update(local_env)

        filename = "env.local.json"
        if os.path.isfile(filename):
            with open(filename) as env_file:
                local_env = json.load(env_file)
                env.update(local_env)

        if self.is_test:
            filename = directory + "../env.test.json"
            if os.path.isfile(filename):
                with open(filename) as env_file:
                    script_env = json.load(env_file)
                    env.update(script_env)

            filename = directory + "env.test.json"
            if os.path.isfile(filename):
                with open(filename) as env_file:
                    script_env = json.load(env_file)
                    env.update(script_env)

            filename = "env.test.json"
            if os.path.isfile(filename):
                with open(filename) as env_file:
                    local_env = json.load(env_file)
                    env.update(local_env)
                
        self.env.update(env)

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

class Demo(object):
    def __init__(self, is_running_in_docker, script_dir="demo_scripts", filename="script.md", is_simulation=True, is_automated=False, is_testing=False, is_learning = False):
        """Initialize variables"""
        self.is_docker = is_running_in_docker
        self.filename = filename
        self.script_dir = script_dir
        self.is_simulation = is_simulation
        self.is_automated = is_automated
        self.is_testing = is_testing
        self.is_learning = is_learning
        self.current_command = ""
        self.current_description = ""

        
    def get_current_command(self):
        """
        Return a tuple of the current command and a list of environment
        variables that haven't been set.
        """
        pattern = re.compile(".*?(?<=\$){?(\w*)(?=[\W|\$|\s|\\\"]?)(?!\$).*?")
        matches = pattern.findall(self.current_command)
        var_list = []
        if matches:
            for var in matches:
                if var != "" and (var not in self.env.get() or self.env.get(var) == ""):
                    var_list.append(var)
        return self.current_command, var_list

    def get_scripts(self, directory):
        """
        Starting with the supplied directory find all `script.md` files
        and return them as a list of scripts available to this execution.
        We will not return multiple `script.md` files from each part of 
        the tree. It is assumed that the highest level `script.md` files
        contains an index of scripts in that directory.

        """
        lines = []
        for dirpath, dirs, files in os.walk(directory):
            for file in files:
                if file == "script.md":                                
                    lines.append(os.path.join(dirpath[len(directory):], file) + "\n")
                
        return lines

    def generate_toc(self):
        toc = {}
        lines = []
        lines.append("# Welcome to Simdem\n")
        lines.append("Below is an autogenerated list of scripts available in `" + self.script_dir + "` and its subdirectories. You can execute any of them from here.\n\n")
        lines.append("# Next Steps\n")

        scripts = self.get_scripts(self.script_dir)

        for script in scripts:
            script = script.strip()
            with open(os.path.join(self.script_dir, script)) as f:
                title = f.readline().strip()
                title = title[2:]
            demo = { "title": title, "path": script }
                
            name = script[:script.index(os.sep)]
            if not name.endswith(".md") and name not in toc:
                toc[name] = [ demo ]
            elif name in toc:
                demos = toc[name]
                demos.append(demo)
                toc[name] = demos

        idx = 1
        for item in sorted(toc):
            demos = toc[item]
            for demo in demos:
                lines.append("  " + str(idx) + ". [" + item + " / " + demo["title"] + "](" + demo["path"] + ")\n")
                idx += 1

        return lines
    
    def run(self):
        """
        Reads a script.md file in the indicated directoy and runs the
        commands contained within. If simulation == True then human
        entry will be simulated (looks like typing and waits for
        keyboard input before proceeding to the next command). This is
        useful if you want to run a fully automated demo.

        The script.md file will be parsed as follows:

        ``` marks the start or end of a code block

        Each line in a code block will be treated as a separate command.
        All other lines will be ignored
        """
        self.env = Environment(self.script_dir, is_test = self.is_testing)

        if not self.script_dir.endswith('/'):
            self.script_dir = self.script_dir + "/"

        lines = None
        
        if self.is_testing:
            test_file = self.script_dir + "test_plan.txt"
            if os.path.isfile(test_file):
                plan_lines = list(open(test_file))
                lines = []
                for line in plan_lines:
                    if not line.startswith("#"):
                        # not a comment so should be a path to a script with tests
                        file = self.script_dir + line.strip()
                        lines = lines + list(open(file))

        file = self.script_dir + self.filename
        if not lines and os.path.isfile(file):
            lines = list(open(file))
        elif not lines:
            lines = self.generate_toc()
                    
        in_code_block = False
        in_results_section = False
        expected_results = ""
        actual_results = ""
        passed_tests = 0
        failed_tests = 0
        is_first_line = True
        in_next_steps = False
        next_steps = []
        executed_code_in_this_section = False
        self.current_description = ""

        for line in lines:
            self.current_description += colorama.Fore.CYAN + colorama.Style.BRIGHT
            self.current_description += line;
            self.current_description += colorama.Style.RESET_ALL

            if line.startswith("Results:"):
                # Entering results section
                in_results_section = True
                # DEPRECATED: having the expected similarity in the results line is deprecated as of 6/22/17
                pos = line.lower().find("expected similarity: ")
                if pos >= 0:
                    pos = pos + len("expected similarity: ")
                    similarity = line[pos:]
                    expected_similarity = float(similarity)
                else:
                    expected_similarity = 0.66
            elif line.startswith("```") and not in_code_block:
                # Entering a code block, if in_results_section = True then it's a results block
                in_code_block = True
                pos = line.lower().find("expected_similarity=")
                if pos >= 0:
                    pos = pos + len("expected_similarity=")
                    similarity = line[pos:]
                    expected_similarity = float(similarity)
                else:
                    expected_similarity = 0.66
            elif line.startswith("```") and in_code_block and in_results_section:
                # Finishing results section
                if in_results_section and self.is_testing:
                    if test_results(expected_results, actual_results, expected_similarity):
                        passed_tests += 1
                    else:
                        failed_tests += 1
                expected_results = ""
                actual_results = ""
                in_results_section = False
                in_code_block = False
            elif line.startswith("```") and in_code_block:
                # Finishing code block
                in_code_block = False
                in_results_section = False
            elif in_results_section and in_code_block:
                expected_results += line
            elif in_code_block and not in_results_section:
                # Executable line
                if line.startswith("#"):
                    # comment
                    pass
                else:
                    if not self.is_learning:
                        print("$ ", end="", flush=True)
                        check_for_interactive_command(self)
                        
                    self.current_command = line
                    actual_results = simulate_command(self)
                    executed_code_in_this_section = True
            elif line.startswith("#") and not in_code_block and not in_results_section and not self.is_automated:
                # Heading in descriptive text, indicating a new section
                if line.lower().startswith("# next steps"):
                    in_next_steps = True
                if is_first_line:
                    run_command(self, "clear")
                elif executed_code_in_this_section:
                    executed_code_in_this_section = False
                    print("$ ", end="", flush=True)
                    check_for_interactive_command(self)
                    self.current_description = colorama.Fore.CYAN + colorama.Style.BRIGHT
                    self.current_description += line;
                    self.current_description += colorama.Style.RESET_ALL
                    self.current_command = "clear"
                    simulate_command(self)
                        
                if not self.is_simulation:
                    print(colorama.Fore.CYAN + colorama.Style.BRIGHT, end="")
                    print(line, end="", flush=True)
                    print(colorama.Style.RESET_ALL, end="")

            else:
                if not self.is_simulation and not in_results_section and not in_next_steps:
                    # Descriptive text
                    print(colorama.Fore.CYAN, end="")
                    print(line, end="", flush=True)
                    print(colorama.Style.RESET_ALL, end="")
                if in_next_steps:
                    pattern = re.compile('(.*)\[(.*)\]\(.*\).*')
                    match = pattern.match(line)
                    if match:
                        print(colorama.Fore.CYAN, end="")
                        print('%s%s' % (match.groups()[0], match.groups()[1]), flush=True)
                        print(colorama.Style.RESET_ALL, end="")
                        next_steps.append(line)
                    
            is_first_line = False

        if self.is_testing:
            print("\n\n=============================\n\n")
            print("Test Run Complete.")
            if failed_tests > 0:
                print(colorama.Fore.RED + colorama.Style.BRIGHT)
                print("Failed Tests: " + str(failed_tests))
                print(colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.GREEN + colorama.Style.BRIGHT)
                print("No failed tests")
                print(colorama.Style.RESET_ALL)
                print("Passed Tests: " + str(passed_tests))
            if failed_tests > 0:
                print("\n\n")
                print("View failure reports in context in the above output.")
                print("\n\n=============================\n\n")
                sys.exit(str(failed_tests) + " test failures. " + str(passed_tests) + " test passes.")
            else:
                sys.exit(0)

        if len(next_steps) > 0:
            in_string = ""
            in_value = 0
            print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT)
            print("Would like to move on to one of the next steps listed above?")
            print(colorama.Fore.WHITE + colorama.Style.BRIGHT, end="")

            while in_value < 1 or in_value > len(next_steps):
                print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT, end="")
                print("Enter a value between 1 and " + str(len(next_steps)) + " or 'quit'")
                print(colorama.Fore.WHITE + colorama.Style.BRIGHT, end="")
                in_string = input()
                if in_string.lower() == "quit" or in_string.lower() == "q":
                    return
                try:
                    in_value = int(in_string)
                except ValueError:
                    pass

            pattern = re.compile('.*\[.*\]\((.*)\/(.*)\).*')
            match = pattern.match(next_steps[in_value - 1])
            self.script_dir = self.script_dir + match.groups()[0]
            self.filename = match.groups()[1]
            self.run()

            
def input_interactive_variable(name):
    """
    Gets a value from stdin for a variable.
    """
    print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT, end="")
    print("\n\nEnter a value for ", end="")
    print(colorama.Fore.YELLOW + colorama.Style.BRIGHT, end="")
    print("$" + name, end="")
    print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT, end="")
    print(": ", end="")
    print(colorama.Fore.WHITE + colorama.Style.BRIGHT, end="")
    value = input()
    return value

def type_command(demo):
    """
    Displays the command on the screen
    If simulation == True then it will look like someone is typing the command
    Highlight uninstatiated environment variables
    """
    print(colorama.Fore.WHITE + colorama.Style.BRIGHT, end="")
    end_of_var = 0
    current_command, var_list = demo.get_current_command()
    for idx, char in enumerate(current_command):
        if char == "$" and var_list:
            for var in var_list:
                var_idx = current_command.find(var)
                if var_idx - 1 == idx:
                    end_of_var = idx + len(var)
                    print(colorama.Fore.YELLOW + colorama.Style.BRIGHT, end="")
                    break
                elif var_idx - 2 == idx and current_command[var_idx - 1] == "{":
                    end_of_var = idx + len(var) + 1
                    print(colorama.Fore.YELLOW + colorama.Style.BRIGHT, end="")
                    break
        if end_of_var and idx == end_of_var:
            end_of_var = 0
            print(colorama.Fore.WHITE + colorama.Style.BRIGHT, end="")
        if char != "\n":
            print(char, end="", flush=True)
        if demo.is_simulation:
            delay = random.uniform(0.01, 0.04)
            time.sleep(delay)
    print(colorama.Style.RESET_ALL, end="")

def simulate_command(demo):
    """
    Types the command on the screen, executes it and outputs the
    results if simulation == True then system will make the "typing"
    look real and will wait for keyboard entry before proceeding to
    the next command
    """

    if not demo.is_learning or demo.current_command.strip() == "clear":
        type_command(demo)
        _, var_list = demo.get_current_command()

        # Get values for unknown variables
        for var_name in var_list:
            if (demo.is_testing):
                var_value = "Dummy value for test"
            else:
                var_value = input_interactive_variable(var_name)
            if not var_name.startswith("SIMDEM_"):
                demo.env.set(var_name, var_value)
                run_command(demo, var_name + '="' + var_value + '"')
                
        output = run_command(demo)
        demo.current_command = ""

    else:
        done = False
        while not done:
            print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT, end="")
            print("\nType the command '", end = "")
            print(colorama.Fore.WHITE + colorama.Style.BRIGHT, end="")
            print(demo.current_command.strip(), end = "")
            print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT, end="")
            print("'")
            print("\t- type 'auto' (or 'a') to automatically type the command")
            print(colorama.Fore.WHITE + colorama.Style.BRIGHT, end="")
            print("\n$ ", end = "", flush = True)
            typed_command = input()
            if typed_command.lower() == "a" or typed_command.lower() == "auto":
                demo.is_learning = False
                output = simulate_command(demo)
                demo.is_learning = True
                done = True
            elif typed_command == demo.current_command.strip():
                demo.is_learning = False
                output = simulate_command(demo)
                demo.is_learning = True
                done = True
            else:
                print(colorama.Fore.RED, end="")
                print("You have a typo there")
        
    return output

shell = None
def run_command(demo, command=None):
    """
    Run the demo.curent_command unless command is passed in, in
    which case run the supplied command in the current demo
    encironment.
    """
    global shell
    
    if not shell:
        child = pexpect.spawnu('/bin/bash', env=demo.env.get(), echo=False, timeout=None)
        ps1 = PEXPECT_PROMPT[:5] + u'\[\]' + PEXPECT_PROMPT[5:]
        ps2 = PEXPECT_CONTINUATION_PROMPT[:5] + u'\[\]' + PEXPECT_CONTINUATION_PROMPT[5:]
        prompt_change = u"PS1='{0}' PS2='{1}' PROMPT_COMMAND=''".format(ps1, ps2)
        shell = pexpect.replwrap.REPLWrapper(child, u'\$', prompt_change)
        
    if not command:
        command = demo.current_command

    print(colorama.Fore.GREEN+colorama.Style.BRIGHT)
    response = shell.run_command(command)
    print(response)
    print(colorama.Style.RESET_ALL)
    return response

def check_for_interactive_command(demo):
    """Wait for a key to be pressed.
    
    Most keys result in the script
    progressing, but a few have special meaning. See the
    documentation or code for a description of the special keys.
    """
    if not demo.is_automated:
        key = get_instruction_key()

        if key == 'h':
            print("help")
            print()
            print("SimDem Help")
            print("===========")
            print()
            print("Pressing any key other than those listed below will result in the script progressing")
            print()
            print("b           - break out of the script and accept a command from user input")
            print("b -> CTRL-C - stop the script")
            print("d           - (re)display the description that precedes the current command then resume from this point")
            print("h           - displays this help message")
            print()
            print("Press SPACEBAR to continue")
            while key != ' ':
                key = get_instruction_key()
            print()
            print("$ ", end = "", flush = True)
            check_for_interactive_command(demo)
        elif key == 'b':
            command = input()
            run_command(demo, command)
            print("$ ", end="", flush=True)
            check_for_interactive_command(demo)
        elif key =='d':
            print("")
            print(colorama.Fore.CYAN) 
            print(demo.current_description);
            print(colorama.Style.RESET_ALL)
            print("$ ", end="", flush=True)
            print(demo.current_command, end="", flush=True)
            check_for_interactive_command(demo)

def get_instruction_key():
    """Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns the character of the key that was pressed (zero on
    KeyboardInterrupt which can happen when a signal gets handled)

    This method is licensed under cc by-sa 3.0 
    Thanks to mheyman http://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key\
    """
    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK 
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR 
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    try:
        ret = sys.stdin.read(1) # returns a single character
    except KeyboardInterrupt:
        ret = 0
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return ret

def test_results(expected_results, actual_results, expected_similarity = 0.66):
    """Compares the similarity of the expected vs actual results.

    Pass when the similarity ratio is greater or equal to the expected
    similarity. Defaults to 66% similarity to pass.
    """
    differ = difflib.Differ()
    comparison = differ.compare(actual_results, expected_results)
    diff = differ.compare(actual_results, expected_results)
    seq = difflib.SequenceMatcher(lambda x: x in " \t\n\r", actual_results, expected_results)

    is_pass = seq.ratio() >= expected_similarity

    if not is_pass:
        print("\n\n=============================\n\n")
        print(colorama.Fore.RED + colorama.Style.BRIGHT)
        print("FAILED")
        print(colorama.Style.RESET_ALL)
        print("Similarity ratio:    " + str(seq.ratio()))
        print("Expected Similarity: " + str(expected_similarity))
        print("\n\n=============================\n\n")
        print("Expected results:")
        print(colorama.Fore.GREEN + colorama.Style.BRIGHT)
        print(expected_results)
        print(colorama.Style.RESET_ALL)
        print("Actual results:")
        print(colorama.Fore.RED + colorama.Style.BRIGHT)
        print(actual_results)
        print(colorama.Style.RESET_ALL)
        print("\n\n=============================\n\n")
        print(colorama.Style.RESET_ALL)
    return is_pass

def get_bash_script(script_dir, is_simulation = True, is_automated=False, is_testing=False):
    """
    Reads a script.md file in the indicated directoy and builds an
    executable bash script from the commands contained within.
    """
    if not script_dir.endswith('/'):
        script_dir = script_dir + "/"
    filename = script_dir + "script.md"


    script = ""
    env = Environment(script_dir, False).get()
    for key, value in env.items():
        script += key + "='" + value + "'\n"

    in_code_block = False
    in_results_section = False
    lines = list(open(filename))
    for line in lines:
        if line.startswith("Results:"):
            # Entering results section
            in_results_section = True
        elif line.startswith("```") and not in_code_block:
            # Entering a code block, if in_results_section = True then it's a results block
            in_code_block = True
        elif line.startswith("```") and in_code_block:
            # Finishing code block
            in_results_section = False
            in_code_block = False
        elif in_code_block and not in_results_section:
            # Executable line
            script += line
        elif line.startswith("#") and not in_code_block and not in_results_section and not is_automated:
            # Heading in descriptive text
            script += "\n"
    return script

def main():
    """SimDem CLI interpreter"""

    p = optparse.OptionParser("%prog [run|demo|learn|test|script] <options> DEMO_NAME", version= SIMDEM_VERSION)
    p.add_option('--style', '-s', default="tutorial",
                 help="The style of simulation you want to run. 'tutorial' (the default) will print out all text and pause for user input before running commands. 'simulate' will not print out the text but will still pause for input.")
    p.add_option('--path', '-p', default="demo_scripts/",
                 help="The Path to the demo scripts directory.")
    p.add_option('--auto', '-a', default="False",
                 help="Set to 'true' (or 'yes') to prevent the application waiting for user keypresses between commands. Set to 'no' when running in test mode to allow users to step through each test.")
    p.add_option('--test', '-t', default="False",
                 help="If set to anything other than False the output of the command will be compared to the expected results in the sript. Any failures will be reported")

    options, arguments = p.parse_args()

    if len(arguments) == 0:
        arguments.append("run")

    if not options.path.endswith("/"):
        options.path += "/"

    if options.auto == "False":
        is_automatic = False
    else:
        is_automatic = True

    if options.test == "False":
        is_test = False
    else:
        is_test = True

    if options.style == "simulate":
        simulate = True
    elif options.style == 'tutorial':
        simulate = False
    else:
        print("Unknown style (--style, -s): " + options.style)
        exit(1)

    if len(arguments) == 2:
        script_dir = options.path + arguments[1]
    else:
        script_dir = options.path

    cmd = arguments[0]

    filename = "script.md"
    is_docker = os.path.isfile('/.dockerenv')
    if cmd == "run":
        demo = Demo(is_docker, script_dir, filename, simulate, is_automatic, is_test);
        demo.run()
    elif cmd == "demo":
        demo = Demo(is_docker, script_dir, filename, True, is_automatic, is_test);
        demo.run()
    elif cmd == "test":
        is_automatic = not options.auto.lower() == "no"
        is_test = True and options.test
        demo = Demo(is_docker, script_dir, filename, simulate, is_automatic, is_test);
        demo.run()
    elif cmd == "script":
        print(get_bash_script(script_dir))
    elif cmd == "learn":
        demo = Demo(is_docker, script_dir, filename, simulate, is_automatic, is_test, is_learning=True);
        demo.run()
    else:
        print("Unknown command: " + cmd)
        print("Run with --help for guidance.")

main()

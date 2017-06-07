#!/usr/bin/env python3

# This is a python script that emulates a terminal session and runs
# commands from a supplied markdown file..

import difflib
import optparse
import os
import pexpect
import random
import time
import shlex
import sys
import json

def type_command(command, script_dir, simulation):
    # Displays the command on the screen
    # If simulation == True then it will look like someone is typing the command
    for char in command:
        if (char != '\n'):
            print(char, end="", flush=True)
        if simulation:
            delay = random.uniform(0.01, 0.04) 
            time.sleep(delay)

def simulate_command(command, script_dir, env = None, simulation = True, is_automatic=False):
    # Types the command on the screen, executes it and outputs the
    # results if simulation == True then system will make the "typing"
    # look real and will wait for keyboard entry before proceeding to
    # the next command
    type_command(command, script_dir, simulation)
    check_for_interactive_command(script_dir, is_automatic)
    print()
    output = run_command(command, script_dir, env)

    return output

def get_simdem_environment(directory):
    # Populates each shell environment with a set of environment vars
    # loaded via env.json file stored either in the project root
    # directory

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
    
    return env

def run_command(command, script_dir, env=None):
    if command.startswith("sudo "):
        is_docker_command = 'if [ -f /.dockerenv ]; then echo "True"; else echo "False"; fi'
        shell = pexpect.spawnu('/bin/bash', ['-c', is_docker_command], env=env, cwd=script_dir, timeout=None)
        shell.expect(pexpect.EOF)
        is_docker = shell.before.strip() == "True"
        if is_docker:
            command = command[5:]

    shell = pexpect.spawnu('/bin/bash', ['-c', command], env=env, cwd=script_dir, timeout=None)
    shell.logfile = sys.stdout
    shell.expect(pexpect.EOF)
    return shell.before
    
def check_for_interactive_command(script_dir, is_automated=False):
    # Wait for a key to be pressed. Most keys result in the script
    # progressing, but a few have special meaning. See the
    # documentation or code for a description of the special keys.
    if not is_automated:
        key = get_instruction_key()
    
        if key == 'b' or key == 'B':
            command = input()
            run_command(command, script_dir)
            print("$ ", end="", flush=True)
            check_for_interactive_command(script_dir, is_automated)

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
    differ = difflib.Differ()
    comparison = differ.compare(actual_results, expected_results)
    diff = differ.compare(actual_results, expected_results)
    seq = difflib.SequenceMatcher(lambda x: x in " \t\n\r", actual_results, expected_results)

    is_pass = seq.ratio() >= expected_similarity

    if not is_pass:
        print("\n\n=============================\n\n")
        print("FAILED")
        print("Similarity ratio:    " + str(seq.ratio()))
        print("Expected Similarity: " + str(expected_similarity))
        print("\n\n=============================\n\n")
        print("Expected results:")
        print(expected_results)
        print("Actual results:")
        print(actual_results)
        print("\n\n=============================\n\n")

    return is_pass

def run_script(script_dir, env=None, is_simulation = True, is_automated=False, is_testing=False):
    # Reads a script.md file in the indicated directoy and runs the
    # commands contained within. If simulation == True then human
    # entry will be simulated (looks like typing and waits for
    # keyboard input before proceeding to the next command). This is
    # useful if you want to run a fully automated demo.
    # 
    # The script.md file will be parsed as follows:
    #
    # ``` marks the start or end of a code block
    #
    # Each line in a code block will be treated as a separate command.
    #
    # All other lines will be ignored

    in_code_block = False
    in_results_section = False

    if not script_dir.endswith('/'):
        script_dir = script_dir + "/"
    filename = script_dir + "script.md"
    
    lines = list(open(filename)) 
    expected_results = ""
    actual_results = ""
    passed_tests = 0
    failed_tests = 0
    is_first_line = True
    executed_code_in_this_section = False

    for line in lines:
        if in_results_section and in_code_block and not line.startswith("```"):
            expected_results += line

        if line.startswith("Results:"):
            # Entering results section
            in_results_section = True
            pos = line.lower().find("expected similarity: ")
            if pos >= 0:
                pos = pos + len("expected similarity: ")
                s = line[pos:]
                expected_similarity = float(s)
            else:
                expected_similarity = 0.66
        elif line.startswith("```") and not in_code_block:
            # Entering a code block, if in_results_section = True then it's a results block
            in_code_block = True
        elif line.startswith("```") and in_code_block and in_results_section:
            # Finishing results section
            if in_results_section and is_testing:
                if test_results(expected_results, actual_results, expected_similarity):
                    passed_tests += 1
                else:
                    failed_tests += 1
            expected_results = ""
            actual_results = ""
            in_results_section = False
            in_code_block = False
        elif line.startswith("```") and in_code_block and not in_results_section:
            # Finishing executable code block
            in_code_block = False
        elif in_code_block and not in_results_section:
            # Executable line
            print("$ ", end="", flush=True)
            check_for_interactive_command(script_dir, is_automated)
            actual_results = simulate_command(line, script_dir, env, is_simulation, is_automated)
            executed_code_in_this_section = True
        elif line.startswith("#") and not in_code_block and not in_results_section and not is_automated:
            # Heading in descriptive text, indicating a new section
            if is_first_line:
                run_command("clear", script_dir, env)
            elif executed_code_in_this_section:
                executed_code_in_this_section = False
                print("$ ", end="", flush=True)
                check_for_interactive_command(script_dir, is_automated)
                simulate_command("clear", script_dir, env, is_simulation, is_automated)
                if not is_simulation:
                    print("$ ", end="", flush=True)
                    # Since this is a heading we are not really simulating a command, it appears as a comment
                    simulate_command(line, script_dir, env, is_simulation, is_automated)
        elif not is_simulation and not in_results_section:
            # Descriptinve text
            print(line, end="", flush=True)

        is_first_line = False
        
    if is_testing:
        print("\n\n=============================\n\n")
        print("Test Run Complete.")
        print("Failed Tests: " + str(failed_tests))
        print("Passed Tests: " + str(passed_tests))
        if failed_tests > 0:
            print("\n\n")
            print("View failure reports in context in the above output.")
        print("\n\n=============================\n\n")

def get_bash_script(script_dir, env=None, is_simulation = True, is_automated=False, is_testing=False):
    # Reads a script.md file in the indicated directoy and builds an
    # executable bash script from the commands contained within.
    
    in_code_block = False
    in_results_section = False

    if not script_dir.endswith('/'):
        script_dir = script_dir + "/"
    filename = script_dir + "script.md"

    script = ""
    env = get_simdem_environment(script_dir)
    for key, value in env.items():
        script += key + "='" + value + "'\n"

    lines = list(open(filename)) 
    for line in lines:
        if line.startswith("Results:"):
            # Entering results section
            in_results_section = True
        elif line.startswith("```") and not in_code_block:
            # Entering a code block, if in_results_section = True then it's a results block
            in_code_block = True
        elif line.startswith("```") and in_code_block and in_results_section:
            # Finishing results section
            in_results_section = False
            in_code_block = False
        elif line.startswith("```") and in_code_block and not in_results_section:
            # Finishing executable code block
            in_code_block = False
        elif in_code_block and not in_results_section:
            # Executable line
            script += line
        elif line.startswith("#") and not in_code_block and not in_results_section and not is_automated:
            # Heading in descriptive text
            script +="\n"
    return script
        
def main():
    """SimDem CLI interpreter"""

    p = optparse.OptionParser("%prog [run|test|script] <options> DEMO_NAME", version="%prog 0.2.3")
    p.add_option('--style', '-s', default="tutorial",
                 help="The style of simulation you want to run. 'tutorial' (the default) will print out all text and pause for user input before running commands. 'simulate' will not print out the text but will still pause for input.")
    p.add_option('--path', '-p', default="demo_scripts/",
                 help="The Path to the demo scripts directory.")
    p.add_option('--auto', '-a', default="False",
                 help="If set to anything other than False the application will not wait for user keypresses between commands.")
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
        print("Unkown style (--style, -s): " + options.style)
        exit(1)

    if len(arguments) == 2:
        script_dir = options.path + arguments[1]
    else:
        script_dir = options.path

    env = os.environ.copy()
    env.update(get_simdem_environment(script_dir))
    cmd = arguments[0]

    if cmd == "run":
        run_script(script_dir, env, simulate, is_automatic, is_test)
    elif cmd == "test":
        is_automatic = True and options.auto
        is_test = True and options.test
        run_script(script_dir, env, simulate, is_automatic, is_test)
    elif cmd == "script":
        print(get_bash_script(script_dir, env))
    else:
        print("Unknown command: " + cmd)
        print("Run with --help for guidance.")
main()

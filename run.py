# This is a python script that emulates a terminal session and runs
# commands from a supplied markdown file..

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
            delay = random.uniform(0.02, 0.08) 
            time.sleep(delay)

def simulate_command(command, script_dir, env = None, simulation = True, is_automatic=False):
    # Types the command on the screen, executes it and outputs the
    # results if simulation == True then system will make the "typing"
    # look real and will wait for keyboard entry before proceeding to
    # the next command
    type_command(command, script_dir, simulation)
    check_for_interactive_command(script_dir, is_automatic)
    print()
    
    run_command(command, script_dir, env)

def environment_setup(directory):
    # Populates each shell environment with a set of environment vars
    # loaded via env.json file stored either in the project root
    # directory
    env = os.environ.copy()
    
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
    shell = pexpect.spawn('/bin/bash', ['-c', command], env=env, cwd=script_dir, timeout=None)
    shell.expect(pexpect.EOF)
    output = shell.before
    
    print(output.decode(encoding='UTF-8'))
    
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

def run_script(script_dir, env=None, simulation = True, is_automated=False):
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
    if simulation:
        print("You are now in demo simulation mode.")
        print("Press a key to clear the terminal and start the demo")
        check_for_interactive_command(script_dir, is_automated)
        run_command("clear", script_dir, env)
        
    for line in lines:
        if line.startswith("Results:"):
            in_results_section = True
        elif line.startswith("```") and not in_code_block:
            in_code_block = True
        elif line.startswith("```") and in_code_block:
            in_results_section = False
            in_code_block = False
        elif in_code_block and not in_results_section:
            print("$ ", end="", flush=True)
            check_for_interactive_command(script_dir, is_automated)
            simulate_command(line, script_dir, env, simulation, is_automated)
        elif not simulation and not in_results_section:
            print(line, end="", flush=True) 

def get_usage():
    commands = [
        {
            "name": "run",
            "description": "Run the demo as if in a normal terminal typing the commands",
            "options": [
                {
                    "name": "DEMO_NAME",
                    "description": "Name of the demo to be run. Demo files should be in a directory with the same name",
                    "type": "required"                    
                },
                {
                    "name": "--style",
                    "description": "Either 'tutorial' (default) or 'simulate'",
                    "type": "optional",
                    "default": "tutorial"
                },
                {
                    "name": "--path",
                    "description": "Path to the directory containining the demo scripts",
                    "type": "optional",
                    "default": "demo_scripts"
                },
                {
                    "name": "--auto",
                    "description": "If set to any value the application does not wait for key presses from the user",
                    "type": "optional",
                    "default": "False"
                }
            ] 
        }
    ]

    req = ""
    opt = ""
    usage = "Usage: %prog [OPTIONS] COMMAND\n\n"
    usage += "Commands\n"
    usage += "========\n\n"
    for cmd in commands:
        usage += cmd["name"]
        for option in cmd["options"]:
            if option["type"] == "required":
                usage += " " + option["name"]
                req += option["name"] + "\n" + option["description"]
                req += "\n\n"
            else:
                opt += option["name"] + "\n" + option["description"] + "\nDefault: " + option["default"]
                opt += "\n\n"
    usage += " <options>\n"
    usage += cmd["description"] + "\n"
    usage += "\n\nRequired Parameters\n"
    usage += "-------------------\n\n"
    usage += req
    usage += "\n\nOptional Options\n"
    usage += "----------------\n\n"
    usage += opt
    usage += "\n\n"
    return usage

def main():
    """SimDem CLI interpreter"""

    p = optparse.OptionParser(usage=get_usage(), version="%prog 0.1")
    p.add_option('--style', '-s', default="tutorial",
                 help="The style of simulation you want to run. 'tutorial' (the default) will print out all text and pause for user input before running commands. 'simulate' will not print out the text but will still pause for input.")
    p.add_option('--path', '-p', default="demo_scripts/",
                 help="The Path to the demo scripts directory.")
    p.add_option('--auto', '-a', default="False",
                 help="If set to anything other than False the application will not wait for user keypresses between commands.")
    options, arguments = p.parse_args()
 
    if len(arguments) == 0:
        arguments.append("run")
        for f in os.listdir("demo_scripts"):
            if os.path.isdir(os.path.join("demo_scripts/", f)):
                arguments.append(f)
                break

    cmd = arguments[0]

    if cmd == "run":
        script_dir = options.path + arguments[1]

        env = environment_setup(script_dir)

        if options.auto == "False":
            is_automatic = False
        else:
            is_automatic = True
        
        if options.style == "simulate":
            simulate = True
        elif options.style == 'tutorial':
            simulate = False
        else:
            print("Unkown style (--style, -s): " + options.style)
            exit(1)
            
        run_script(script_dir, env, simulate, is_automatic)
    else:
        print("Unkown command: " + cmd)
        print(get_usage())



main()

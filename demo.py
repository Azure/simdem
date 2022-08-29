# This class represents a Demo to be executed in SimDem.

import datetime
import difflib
from itertools import tee, islice, zip_longest
import json
import os
import re
import sys
import urllib.request
from environment import Environment

from cli import Ui
import config

def get_next(some_iterable, window=1):
    items, nexts = tee(some_iterable, 2)
    nexts = islice(nexts, window, None)
    return zip_longest(items, nexts)

class Demo(object):
    def __init__(self, is_running_in_docker, script_dir="demo_scripts", filename="README.md", is_simulation=True, is_automated=False, is_testing=False, is_fast_fail=True,is_learning = False, parent_script_dir = None, is_prep_only = False, is_prerequisite = False, output_format="log"):
        """
        is_running_in_docker should be set to true is we are running inside a Docker container
        script_dir is the location to look for scripts
        filename is the filename of the script this demo represents
        is_simulation should be set to true if we want to simulate a human running the commands
        is_automated should be set to true if we don't want to wait for an operator to indicate it's time to execute the next command
        is_testing is set to true if we want to compare actual results with expected results, by default execution will stop if any test fails (see is_fast_fail)
        is_fast_fail should be set to true if we want to contnue running tests even after a failure
        is_learning should be set to true if we want a human to type in the commands
        parent_script_dir should be the directory of the script that calls this one, or None if this is the root script
        is_prep_only should be set to true if we want to stop execution after all prerequisites are satsified
        is_prerequisite indicates whether this is a prerequisite or not. It is used to decide behaviour with respect to simulation etc.
        """
        self.mode = None
        self.is_docker = is_running_in_docker
        self.filename = filename
        self.script_dir = ""
        self.set_script_dir(script_dir)
        self.is_simulation = is_simulation
        self.is_automated = is_automated
        self.is_testing = is_testing
        self.is_fast_fail = is_fast_fail
        self.is_learning = is_learning
        self.current_command = ""
        self.current_description = ""
        self.last_command = ""
        self.is_prep_only = is_prep_only
        self.parent_script_dir = parent_script_dir
        if self.parent_script_dir:
            self.env = Environment(self.parent_script_dir, is_test = self.is_testing)
        else:
            self.env = Environment(self.script_dir, is_test = self.is_testing)
        self.is_prerequisite = is_prerequisite
        self.output_format = output_format
        self.all_results = []
        self.completed_validation_steps = []
        
    def set_script_dir(self, script_dir, base_dir = None):
        if base_dir is not None and not base_dir.endswith(os.sep):
            base_dir += os.sep
        elif base_dir is None:
            base_dir = ""
            
        self.script_dir = os.path.abspath(os.path.join(base_dir,  script_dir))
        
    def get_current_command(self):
        """
        Return a tuple of the current command and a list of environment
        variables that haven't been set and a list that have been set..
        """

        # If the command sets a variable put it in our env copy
        pattern = re.compile("^(\w*)=(.*)$")
        match = pattern.match(self.current_command)
        if match:
            key = match.groups()[0]
            val = match.groups()[1]
            self.env.set(key, val)
            
        # Get all the vars, check to see if they are uninitialized
        var_pattern = re.compile(".*?(?<=\$)\(?{?(\w*)(?=[\W|\$|\s|\\\"]?)\)?(?!\$).*")
        matches = var_pattern.findall(self.current_command)
        undefined_var_list = []
        defined_var_list = []
        if matches:
            for var in matches:
                have_value = False
                if self.env:
                    for item in self.env.get():
                        if var == item:
                            have_value = True
                            defined_var_list.append(var)
                            break
                if len(var) > 0 and not have_value and not '$(' + var in self.current_command:
                    value = self.ui.get_shell().run_command("echo $" + var).strip()
                    if len(value) == 0:
                        undefined_var_list.append(var)
                    else:
                        defined_var_list.append(var)
        return self.current_command, undefined_var_list, defined_var_list

    def get_scripts(self, directory):
        """
        Starting with the supplied directory find all `README.md` files
        and return them as a list of scripts available to this execution.
        We will not return multiple `README.md` files from each part of 
        the tree. It is assumed that the highest level `README.md` files
        contains an index of scripts in that directory.

        """
        lines = []
        for dirpath, dirs, files in os.walk(directory):
            for file in files:
                if file == "README.md" or file == "script.md":
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

            name, _ = os.path.split(script)
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
                if not item == "":
                    lines.append("  " + str(idx) + ". [" + item + " / " + demo["title"] + "](" + demo["path"] + ")\n")
                else:
                    lines.append("  " + str(idx) + ". [" + demo["title"] + "](" + demo["path"] + ")\n")
                idx += 1

        return lines
    
    def run(self, mode = None):
        """
        Reads a README.md file in the indicated directoy and runs the
        commands contained within. If simulation == True then human
        entry will be simulated (looks like typing and waits for
        keyboard input before proceeding to the next command). This is
        useful if you want to run a fully automated demo.

        The README.md file will be parsed as follows:

        ``` marks the start or end of a code block

        Each line in a code block will be treated as a separate command.
        All other lines will be ignored
        """
        if self.ui is None:
            raise Exception("Attempt to run a demo before ui is configured")
        
        if mode is None:
            mode = self.ui.get_command(config.modes)
        self.mode = mode

        self.ui.log("debug", "Running script in " + self.mode + " mode")

        if mode == "script":
            print(self.get_bash_script())
            return
        elif mode == "demo":
            # we automate the prereq steps so start in auto mode without simulation
            # we'll switch these two values once prereqs are complete
            self.is_simulation = False
            self.is_automated = True 
        elif mode == "test":
            self.is_testing = True
            self.is_automated = True
        elif mode == "learn":
            self.is_learning = True
        elif mode == "prep":
            self.is_prep_only = True
            self.is_testing = True
            self.is_automated = True
        elif mode == "run" or mode == "tutorial":
            pass
        else:
            raise Exception("Unkown mode: '" + mode + "'")

        self.env = Environment(self.script_dir, is_test = self.is_testing)

        self.ui.log("debug", (str(self.env)))
        
        self.ui.log("debug", "Running script called '" + self.filename + "' in '" + self.script_dir +"'")
        
        classified_lines = self.classify_lines()
        failed_tests, passed_tests = self.execute(classified_lines)

        if self.is_prep_only:
            if failed_tests == 0:
                self.ui.information("Preparation steps for '" + self.script_dir + "' complete", True)
            else:
                self.ui.error("Preparation steps for '" + self.script_dir + "' failed", True)
        elif self.is_testing:
            self.ui.horizontal_rule()
            self.ui.heading("Test Results")
            if failed_tests > 0:
                self.ui.warning("Failed Tests: " + str(failed_tests))
                self.ui.information("Passed Tests: " + str(passed_tests))
                self.ui.new_para()
            else:
                self.ui.information("No failed tests.", True)
                self.ui.information("Passed Tests: " + str(passed_tests))
                self.ui.new_para()
            if failed_tests > 0:
                self.ui.instruction("View failure reports in context in the above output.")
                if self.is_fast_fail:
                    self.output_results()

        if not self.is_simulation and not self.is_testing and not self.is_prep_only:
            next_steps = []
            for line in classified_lines:
                if line["type"] == "next_step" and len(line["text"].strip()) > 0:
                    pattern = re.compile('.*\[.*\]\((.*)\/(.*)\).*')
                    match = pattern.match(line["text"])
                    if match:
                        next_steps.append(line)

            if len(next_steps) > 0:
                if self.parent_script_dir:
                    return
                in_string = ""
                in_value = 0
                self.ui.instruction("Would you like to move on to one of the next steps listed above?")

                while in_value < 1 or in_value > len(next_steps):
                    in_string = self.ui.request_input("Enter a value between 1 and " + str(len(next_steps)) + " or 'quit'")
                    if in_string.lower() == "quit" or in_string.lower() == "q":
                        return
                    try:
                        in_value = int(in_string)
                    except ValueError:
                        pass

                self.ui.log("debug", "Selected next step: " + str(next_steps[in_value -1]))
                pattern = re.compile('.*\[.*\]\((.*)\/(.*)\).*')
                match = pattern.match(next_steps[in_value -1]["text"])
                self.set_script_dir(match.groups()[0], self.script_dir)
                self.filename = match.groups()[1]
                self.run(self.mode)

        self.output_results()

    def output_results(self):
        """Output the results of the run in the format requested. Note that
if `--output` is `log` (or undefined) we will have been outputing the
logs throughout execution."""
        passed = True            
        if self.output_format == "json":
            output = []
        else:
            output = ""
            
        for result in self.all_results:
            timestamp = datetime.datetime.utcnow().strftime("%Y%m%d - %H:%M")
            test_name = os.path.join(self.script_dir, self.filename)
            is_success = result["passed"]
            if is_success:
                failure_message = None
            else:
                failure_message = result
            test_type = "SimDem"
            resource_group = self.env.get("SIMDEM_RESOURCE_GROUP")
            region = self.env.get("SIMDEM_LOCATION")
            orchestrator = self.env.get("SIMDEM_ORCHESTRATOR")

            if self.output_format == "summary":
                if is_success:
                    meta = "Succesful test"
                else:
                    meta = "Failed test:\t" + json.dumps(failure_message)
                meta += "\nTime (UTC):\t" + timestamp
                meta += "\nTest Name:\t" + test_name
                meta += "\nOrchestrator:\t" + orchestrator
                meta += "\nResource Group:\t" + resource_group
                meta += "\nRegion:\t\t" + region
                meta += "\n\n"

                output += meta
            elif self.output_format == "json":
                meta = {
                    "TimeStampUTC": timestamp,
                    "TestName": test_name,
                    "TestType": test_type,
                    "ResourceGroup": resource_group,
                    "Region": region,
                    "Orchestrator": orchestrator,
                    "Success": is_success,
                    "FailureStr": failure_message
                }
                output.append(meta)
            elif self.output_format != "log":
                sys.exit("Invalid option for '--output', see 'simdem --help' for available options")
            else:
                message = "" # logs were output during execution

            if not is_success:
                passed = False

        if len(output) == 0:
            output = "Completed run."
                
        if passed:
            if self.parent_script_dir:
                # This is a prereq script so we don't output summary results for this, but we'll log them
                if self.output_format == "json":
                    self.ui.log("debug", json.dumps(output))
                else:
                    self.ui.log("debug", output)
            else:
                if self.output_format == "json":
                    print(json.dumps(output))
                else:
                    print(output)
                
        else:
            if self.output_format == "json":
                sys.exit(json.dumps(output))
            else:
                sys.exit(output)

    def classify_lines(self):
        lines = None

        # Only run through test plan for the first script
        if self.is_testing and self.parent_script_dir is None:
            test_file = os.path.join(self.script_dir,  "test_plan.txt")
            if os.path.isfile(test_file):
                self.ui.log("info", "Executing test plan in " + test_file)
                plan_lines = list(open(test_file))
                lines = []
                for line in plan_lines:
                    line = line.strip()
                    if not line == "" and not line.startswith("#"):
                        # not a comment or whitespace so should be a path to a script with tests
                        self.ui.log("debug", "Including " + line + " in tests.")
                        before = len(lines)
                        file = os.path.join(self.script_dir, line)
                        lines.append("START TEST FILE: " + file)
                        lines = lines + list(open(file))
                        lines.append("END TEST FILE: " + file)
                        after = len(lines)
                        self.ui.log("debug", "Added " + str(after - before) + " lines.")
                        
        if lines is None:
            if (self.script_dir.endswith(".md")):
                self.script_dir, self.filename = os.path.split(self.script_dir)
                
            file = os.path.join(self.script_dir, self.filename)
            self.ui.log("info", "Reading lines from " + file)
    
            if file.startswith("http"):
                # FIXME: Error handling
                response = urllib.request.urlopen(file)
                data = response.read().decode("utf-8")
                lines = data.splitlines(True)
            else:
                if not lines and os.path.isfile(file):
                    lines = list(open(file))
                elif not lines:
                    if self.parent_script_dir != "":
                        # If we have a parent then this is a preqiusite and therefore it should exist
                        # if it doesn't then it may be that we are using relative paths
                        # from the script location and that is different from self.script_dir
                        exit("Missing prerequisite script: " + self.filename + " in " + self.script_dir)
                    else:
                        lines = self.generate_toc()

        test_file_path = None
        in_code_block = False
        in_non_executable_code_block = False
        in_results_section = False
        in_next_steps = False
        in_prerequisites = False
        in_validation_section = False
        executed_code_in_this_section = False

        classified_lines = []

        # TODO: this for loop is awful. We need to make this a state machine. It has grown out of control.
        for line in lines:
            # print("Classifying line: " + line)
            if line.startswith("START TEST FILE: "):
                test_file_path = line[17:]
                self.ui.log("debug", "Entering test file: " + test_file_path)
                classified_lines.append({"type": "start_test_file",
                                         "file": test_file_path})
            elif line.startswith("END TEST FILE: "):
                test_file_path = line[15:]
                self.ui.log("debug", "Exiting test file: " + test_file_path)
                classified_lines.append({"type": "end_test_file",
                                         "file": test_file_path})
                test_file_path = None
            elif line.lower().startswith("results:"):
                # Entering results section
                # print("Entering results section " + line)
                in_results_section = True
            elif not in_code_block and line.strip().lower() == "```bash":
                # Entering a code block,
                # print("Entering executable code block " + line);
                in_code_block = True 
            elif not in_code_block and not in_non_executable_code_block and line.startswith("```"):
                if (not in_results_section and line.strip() == "```"):
                        self.ui.warning("Found a backtick line with no language hint near line " + str(len(classified_lines) + 1) + " of '" + file + "'\n. Treating as a non-executable code block, this can result in failed tests if this is intended to be executable. Add a 'bash' language hint to mark it as executable.")
                # Entering a non executable code block - one we don't know how to execute
                #print("Entering a non-executable block " + line)
                in_non_executable_code_block = True
                pos = line.lower().find("expected_similarity")
                if pos >= 0:
                    pos = line.find("=", pos) + 1
                    similarity = line[pos:].strip()
                    expected_similarity = float(similarity)
                else:
                    expected_similarity = 0.5
                self.ui.log("debug", "Expected similarity set to " + str(expected_similarity) + " because of line '" + line + "'")
            elif (in_code_block or in_non_executable_code_block or in_results_section) and line.strip().startswith("```"):
                # Finishing code block
                # print("Exiting code block " + line)
                in_code_block = False
                in_non_executable_code_block = False
                in_results_section = False
                in_validation_section = False
            elif in_results_section and (in_code_block or in_non_executable_code_block):
                # print("Adding results line " + line)
                classified_lines.append({"type": "result",
                                         "expected_similarity": expected_similarity,
                                         "text": line})
            elif in_code_block and not in_results_section:
                # Executable line
                # print("Add executable line " + line)
                if line.strip().startswith("#"):
                    # comment
                    pass
                else:
                    classified_lines.append({"type": "executable",
                                             "text": line})
            elif not in_code_block and not in_results_section and line.strip().startswith("#"):
                # Heading in descriptive text, indicating a new section
                if line.lower().strip().endswith("# next steps"):
                    in_next_steps = True
                    in_prerequisites = False
                    in_validation_section = False
                elif line.lower().strip().endswith("# prerequisites"):
                    self.ui.log("debug", "Found a prerequisites section")
                    in_prerequisites = True
                    in_validation_section = False
                    in_next_steps = False
                elif line.lower().strip().startswith("# validation"):
                    # Entering validation section
                    self.ui.log("debug", "Entering Validation Section")
                    in_validation_section = True
                    in_prerequisites = False
                    in_next_steps = False
                else:
                    in_prerequisites = False
                    in_validation_section = False
                    in_next_steps = False
                classified_lines.append({"type": "heading",
                                         "text": line})
            else:
                if in_next_steps:
                    classified_lines.append({"type": "next_step",
                                             "text": line})
                elif in_prerequisites and len(line.strip()) > 0:
                    if test_file_path:
                        source_file_path = test_file_path
                    else:
                        source_file_path = os.path.join(self.script_dir, self.filename)
                    classified_lines.append({"type": "prerequisite",
                                             "text": line,
                                             "source_file_path": source_file_path})
                elif in_validation_section:
                    classified_lines.append({"type": "validation",
                                             "text": line})
                else:
                    classified_lines.append({"type": "description",
                                             "text": line})

            is_first_line = False

        classified_lines.append({"type": "EOF",
                                 "text": ""})

        if config.is_debug:
            self.ui.log("debug", "Classified lines: ")
            for line in classified_lines:
                self.ui.log("debug", str(line))
        
        return classified_lines

    def execute(self, lines):
        """Execute the script found in the lines. Return the number of failed
           tests and the number of passed tests."""
        
        source_file_directory = None
        is_first_line = True
        in_results = False
        expected_results = ""
        actual_results = ""
        failed_tests = 0
        passed_tests = 0
        done_prerequisites = False

        if not self.is_testing:
            self.ui.clear()
        for line, next_line in get_next(lines):
            # print("Executing line of Type: " + line["type"])

            if line["type"] == "start_test_file":
                source_file_directory = os.path.dirname(line["file"])
                self.ui.get_shell().run_command("pushd " + source_file_directory)
                done_prerequisites = False
            elif line["type"] == "end_test_file":
                source_file_directory = None
                self.ui.get_shell().run_command("popd")
            elif line["type"] == "result":
                if not in_results:
                    in_results = True
                    expected_results = ""
                expected_results += line["text"]
                expected_similarity = line["expected_similarity"]
            elif line["type"] != "result" and in_results:
                # Finishing results section
                if self.is_testing:
                    results = self.is_pass(expected_results, self.strip_ansi(actual_results), expected_similarity)
                    self.ui.test_results(results)
                    self.all_results.append(results)
                    if results["passed"]:
                        passed_tests += 1
                    else:
                        # print("Failed test")
                        # print(line)
                        failed_tests += 1
                        if self.is_fast_fail:
                            break
                expected_results = ""
                actual_results = ""
                in_results = False
            elif line["type"] == "prerequisite":
                if not done_prerequisites:
                    self.ui.heading(line["text"])
                    self.check_prerequisites(lines, source_file_directory)
                    done_prerequisites = True
                    if self.is_prep_only:
                        return failed_tests, passed_tests

                    if self.mode == "demo":
                        # prereqs are now complete, so switch to simulated demo mode
                        self.is_simulation = True
                        self.is_automated = False
            elif line["type"] == "executable":
                # print("Execting:")
                # print(line["text"])
                if line["text"].strip() == "":
                    break
                if not self.is_learning:
                    self.ui.prompt()
                    self.ui.check_for_interactive_command()
                self.current_command = line["text"]
                actual_results = self.ui.simulate_command()
                self.current_description = ""
                if not self.is_automated and not next_line["type"] == "executable":
                    self.ui.check_for_interactive_command()
            elif line["type"] == "heading":
                if not is_first_line and not self.is_simulation:
                    self.ui.check_for_interactive_command()
                if not self.is_simulation and not self.is_testing:
                    self.ui.clear()
                    self.ui.heading(line["text"])
            else:
                if not self.is_simulation and (line["type"] == "description" or line["type"] == "validation"):
                    # print("Description:")
                    # print(line)
                    # Descriptive text
                    if not self.is_testing:
                        self.ui.description(line["text"])
                    self.current_description += line["text"]
                if line["type"] == "next_step" and not self.is_simulation:
                    pattern = re.compile('(.*)\[(.*)\]\(.*\).*')
                    match = pattern.match(line["text"])
                    if match:
                        self.ui.next_step(match.groups()[0], match.groups()[1])
                    else:
                        self.ui.description(line["text"])

            is_first_line = False

        return failed_tests, passed_tests
    
    def check_prerequisites(self, lines, source_file_directory = None):
        """Check that all prerequisites have been satisfied by iterating
        through them and running the validation steps. If the
        validatin tests pass then move on, if they do not then execute
        the prerequisite script. If running in test mode assume that
        this is the case (pre-requisites should be handled in the
        test_plan).

        When running in test mode the script_dir may be different from 
        the location of the prerequisite script file. In these cases the 
        'source_file_directory' should container the directory in which
        the prequisite script is located.
        """
        if source_file_directory is None:
            source_file_directory = self.script_dir
        steps = []
        for line in lines:
            step = {}
            if line["type"] == "prerequisite" and len(line["text"].strip()) > 0:
                if source_file_directory and line["source_file_path"].startswith(source_file_directory):
                    self.ui.log("debug", "Looking for prereq file in line: " + line["text"])
                    self.ui.description(line["text"])
                    pattern = re.compile('.*\[(.*)\]\((.*)\).*')
                    match = pattern.match(line["text"])
                    if match:
                        step["title"] = match.groups()[0].strip()
                        href = match.groups()[1]
                        if not href.endswith(".md"):
                            if not href.endswith("/"):
                                href = href + "/"
                            href = href + "README.md"
                        step["href"] = href
                        steps.append(step)
                        self.ui.log("debug", "Found prereq: " + str(step))

        for step in steps:
            path, filename = os.path.split(step["href"])
            self.ui.log("debug", "Source file directory is " + source_file_directory)
            if (step["href"].startswith(".")):
                if source_file_directory is not None:
                    new_dir = os.path.join(self.script_dir, source_file_directory, path)
                else:
                    new_dir = os.path.join(self.script_dir, path)
            else:
                new_dir = path

            new_dir = os.path.abspath(new_dir)
            full_path = os.path.join(new_dir, filename)
            if full_path in self.completed_validation_steps:
                self.ui.log("debug", "Already validated / executed script in  " + full_path)
                continue
            
            self.ui.new_para()

            self.ui.log("debug", "Execute prerequisite step in " + filename + " in " + new_dir)
            demo = Demo(self.is_docker, new_dir, filename, self.is_simulation, self.is_automated, self.is_testing, self.is_fast_fail, self.is_learning, self.script_dir, is_prerequisite = True, output_format=self.output_format)
            demo.mode = self.mode
            demo.set_ui(self.ui)
            demo.run_if_validation_fails(self.mode)
            self.ui.get_shell().run_command("popd ") # set_ui runs pushd
            self.ui.set_demo(self) # demo.set_ui(...) assigns new demo to ui, this reverts after prereq execution

            self.completed_validation_steps.append(full_path)
            self.ui.check_for_interactive_command()
            
    def run_if_validation_fails(self, mode = None):
        self.ui.information("Validating pre-requisite of '" + self.parent_script_dir + "' in '" + os.path.abspath(os.path.join(self.script_dir, self.filename)) + "'")
        self.ui.new_para()
        lines = self.classify_lines()
        self.check_prerequisites(lines, self.script_dir)
        if self.validate(lines):
            self.ui.information("Validation passed.", True)
        else:
            self.ui.information("Validation failed of pre-requisite execution did not pass. Running prerequisite steps in '" + os.path.abspath(os.path.join(self.script_dir, self.filename)) + "'", True)
            self.ui.new_para()
            self.ui.check_for_interactive_command()
            self.run(mode)
            if not self.is_testing:
                self.ui.clear()
            
    def validate(self, lines):
        """Run through the supplied lines, executing and testing any that are
found in the validation section.

        """
        self.ui.prompt()
        result = True
        in_validation = False
        has_validation_steps = False
        in_results = False
        expected_results = ""
        for line in lines:
            if line["type"] == "validation":
                in_validation = True
                has_validation_steps = True
            elif line["type"] == "heading":
                in_validation = False
            elif in_validation and line["type"] == "executable":
                self.current_command = line["text"]
                self.ui.log("debug", "Execute validation command: " + self.current_command)
                actual_results = self.ui.simulate_command(not config.is_debug)
                expected_results = ""
            elif in_validation and line["type"] == "result":
                if not in_results:
                    in_results = True
                    expected_results = ""
                expected_results += line["text"]
                expected_similarity = line["expected_similarity"]
            elif (line["type"] != "result" and in_results):
                # Finishing results section
                test_results = self.is_pass(expected_results, self.strip_ansi(actual_results), expected_similarity)
                if not test_results["passed"]:
                    self.ui.log("debug", "validation expected results: '" + expected_results + "'")
                    self.ui.log("debug", "validation actual results: '" + actual_results + "'")
                    result = False
                expected_results = ""
                actual_results = ""
                in_results = False

        return result and has_validation_steps

    def strip_ansi(self, text):
        """ Strip ANSI codes from a string."""
        ansi_escape = re.compile(r'\x1b[^m]*m')
        return ansi_escape.sub('', text)
    
    def is_pass(self, expected_results, actual_results, expected_similarity = 0.66):
        """Checks to see if a command execution passes.
        If actual results compared to expected results is within
        the expected similarity level then it's considered a pass.

        Returns a dictionary containing the results:
        {
          "passed": boolean,
          "command": "the command executed",
          "results": "Results returned",
          "expected_results": "Expected results",
          "similarity": float,
          "required_similarity": float
        }

        """
        differ = difflib.Differ()
        comparison = differ.compare(actual_results, expected_results)
        diff = differ.compare(actual_results, expected_results)
        seq = difflib.SequenceMatcher(lambda x: x in " \t\n\r", actual_results, expected_results)

        is_pass = seq.ratio() >= expected_similarity
        
        self.ui.log("debug", "Similarity is: " + str(seq.ratio()))

        message = {
            "passed": is_pass,
            "command": self.last_command,
            "results": actual_results,
            "expected_results": expected_results,
            "similarity": seq.ratio(),
            "required_similarity": expected_similarity
        }

        return message
                
    def __str__( self ):
        s = "Demo directory: " + self.script_dir + "\n"
        s += "Demo filename: " + self.filename + "\n"
        if self.is_docker:
            s += "Running in a Docker container\n"
        else:
            s += "Not running in a Docker container\n"
        s += "Simulation mode: {0}\n".format(self.is_simulation)
        s += "Automatic mode: {0}\n".format(self.is_automated)
        s += "Learn mode: {0}\n".format(self.is_learning)
        s += "Test mode: {0}\n".format(self.is_testing)
        if self.is_testing:
            s += "Fast fail test mode: {0}\n".format(self.is_fast_fail)
        
        return s

    def set_ui(self, ui):
        self.ui = ui
        ui.set_demo(self)
        self.ui.get_shell().run_command("pushd " + self.script_dir)
        self.ui.log("debug", str(self))

    def get_bash_script(self):
        """Reads a README.md file in the indicated directoy and builds an
        executable bash script from the commands contained within.

        """
        if not self.script_dir.endswith('/'):
            self.script_dir = self.script_dir + "/"
        
        script = ""
        env = Environment(self.script_dir, False).get()
        for key, value in env.items():
            script += key + "='" + value + "'\n"

        in_code_block = False
        in_results_section = False
        lines = list(open(self.script_dir + "README.md"))
        for line in lines:
            if line.startswith("Results:"):
                # Entering results section
                in_results_section = True
            elif (line.strip().lower() == "```bash" or line.strip().lower() == "```") and not in_code_block:
                # Entering a code block, if in_results_section = True then it's a results block
                in_code_block = True
            elif line.strip().startswith("```") and in_code_block:
                # Finishing code block
                in_results_section = False
                in_code_block = False
            elif in_code_block and not in_results_section:
                # Executable line
                script += line
            elif line.startswith("#") and not in_code_block and not in_results_section:
                # Heading in descriptive text
                script += "\n"
        return script

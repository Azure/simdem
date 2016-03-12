This project provides ways to script demo's. it can the human
interaction parts of running the demo live so that you can concentrate
on explaining what is happening, while still being able to go
off-script in response to questions and the need for further
exploration.

# Writing Demo Scripts

At the very least a demo script consists of a script.md file. This
will contain both descriptinve text and command blocks describing the
commands that need to be run. These files are intended to be human
readable, however, you can use them to drive a simulation of the demo
being run. See next section for details.

Ideally script directories will also contain a `setup.sh` and
`clearup.sh` files. These are intended to be run to configure the demo
environment and to cleanup after the demo is complete.

# Running Automated Demo's

Script.md files are human readable, but they can also be used to drive
an automated demo flow. This means you don't need to worry about
remember the exact commands or typos in the live demo. However, the
commands are still run live. Your demo is really live. The demo gods
will still be ready to wreak havoc on you in every other way possible.

To test this out try running the command `./simulate` in this
directory. By default this runs the `demo-scripts/docker_101` demo.

Once in the demo script and at the simulated command prompt system
waits for a key press. Most keys simply cause the demo to proceed to
the next step. However, a few keys enable special actions. These are
described listed here with each feature being described below:

'b' or 'B' - Break from the Script

If you press any key other than those listed above the engine will
simulate the typing of the next command. Note that there is no visiual
indicator that you are now in an interactive mode. Once complete hit a
key and the command will be executed. Once complete it will return you
again to the simulated command prompt.

## Break from the Script

If you want to break from the script in order to show something
different, perhaps in response to a question, you can do so. Simplay
wait until the current command has finished and your cursor is at the
start of a new command line and press 'b' or 'B'. You can now enter
the command you want to run.

Once your command as completed you will be back at the simulated
command prompt. From here you can press a command key to execute that
command (including hitting b to do another customer command) or any
other key to progress to the next step of the demo.

# Limitations of Automated Demo's

Not all commands work well in the automated environment. For example
you might want to edit a file. This needs to be done in a true
terminal. We therefore recommend using multiple shells to allow this
kind of functionality. This will allow you to switch to the other
shell for interactive parts.
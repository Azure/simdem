# Welcome to SimDem: A Tutorial That is Also a Demo (and a test script)

Simdem allows you to wite a tutorial in markdown format and then run
the commands within it as a simulated demo, interactive tutorial or
even a test script.

It reads a script, written in the form of a human readable markdown
file, and executes the commands within this script on your behalf. It
will even make it look like you are really typing the commands, which
is great if you want to concentrate on explaining what you are doing
but still run the demo live.

It's easier to describe if you see it working. In fact you are already
in a SimDem. Press a key (other than 'b', we'll look at that shortly)
to "type" a command, once the command has been "typed" hit
a key to execute the command.

```
echo "It might look like this was typed into the terminal (even more so if you ran SimDem with the '--style simulate' flag), it actually comes from a markdown file."
echo "As will all the commands you see here, not only are they 'typed' but they are executed in real time..."
```

The date command will prove this is running in real time.

```
date
```

Results:

```
Sat Mar 12 08:59:01 UTC 2016
```

```
# Let's take a look at the start of markdown file that is the script
head -n 45 script.md 
```

Cool, huh?

# Modes of Operation

SimDem demos are interactive and can be run in different modes.

  * Tutorial: Displays the descriptive text of the tutorial and pauses
    at code blocks to allow user interaction.
  * Simulate: Does not disply the descriptive text, but pauses at each
    code block. When the user hits a key the command is "typed", a
    second keypress executes the command.
  * Test: Runs the commands and then verifies that the output is
    sufficiently similar to the expected results (recorded in the
    markdown file) to be considered correct.
  * Script: Creates an executable bash script from the document
  * Auto: allows any of the above modes to be run but without user
    interaction

Tutorial mode is ideal if you are using this as a learning or teaching
tool. In this mode a description of what you are about to do is shown
on the screen, hit a key to see the command, hit another key to
execute the command. Tutorial mode is the default.

Demo mode is ideal if you are using this to teach or demonstrate how
to achive the goal. In this mode no descriptive text is shown, instead
when you press a key the next command is "typed", pressing another key
will execute the command. The idea is that you describe what is
happening as the application "types" the command for you. To run in
demo mode use the `--style simulate` command line switch.

Test mode runs the commands and then verifies that the output is
sufficiently similar to the expected results (recorded in the markdown
file) to be considered correct. To run in test mode use the `--test
yes` switch. For convenience you can use the command `test` to execute
tests with the optimal configuration for automated testing..

Script mode does not execute any of the commands, instead is outputs
an executable bash script that can be run without SimDem. Use the
command `script` to generate the executable script.

Each of these modes can be run in auto mode too. This means that the
program does not wait for a keypress before proceeding. This can be
useful if you want to runthe complete script unattended. To run in
automated or unnattended mode use the `--auto true` command line
switch.

Manual mode is ideal if you would like to manually type the commands,
many people find this helps them remember. It can be useful in the
first few runs, but we still recommend using "demo" mode when doing
live demo's - it's much harder to make a mistake this way.


# Automated Testing

When running with the `--test` flag or using the `test` command SimDem
will verify that the output of each command is as expected. It does
this by comparing the output of the command with the `Results:`
section in the script. By default a 66% or more match indicates a
pass. However, in some cases a much lower similarity is expected, for
example, the output of `date` will vary considerably each time it is
run. In these situations you can provide an expected similarity as
part of your `Results:` section header, for example:

```
date
```

Results: Expected Similarity: 0.2

```
Tue Jun  6 15:23:53 UTC 2017
```

# Directory structure

SimDem projects consist of a root directory and one or more tutorial
sub-directories. Project directories will contain at least a
`script.md` file that will be used by default when SimDem is run
against the project. Therefore the minimum directory structure for a
simple tutorial is:

`
My_SimDem_Tutorial
└── script.md 
`

A more complex project will contain a number of sub-directories
containing tutorials. Tutorial sub-directories will contain at least a
`script.md` file, this is the main file for that tutorial. For example:

`
My_Complex_SimDem_Tutorial
├── script.md 
├── Tutotial_1
│   └── script.md
├── Tutotial_2
│   └── script.md
└── Tutotial_3
    └── script.md
`

The SimDem application has the following setup:

```
tree ..
```

Results: Expected Similarity: 0.5

```
demo_scripts/
├── env.json
├── env.local.json
├── script.md
├── simdem
│   ├── env.json
│   ├── env.local.json
│   └── script.md
└── test
    ├── env.json
    └── script.md						
```

# Environment Variables

In order to use environment variables, you can define one or more
files. These variables are available in every command that is
executed.

Tutorials can carry `env.json` files in the project directory and/or
in tutorial sub- directories. Files in tutorial sub-directories will
overwrite settings pulled from the project directory. 

This tutorial defines an 'env.json' in the project directory:

```
cat ../env.json
```

Results:

```
{
    "TEST": "Hello from the project"
}
```

It also defines an 'env.json' file in the tutorial folder:

```
cat env.json
```

Results:

```
{
    "TEST": "hello-world"
}
```

The file that "wins" is the most local one, that is the one in the tutorial:

```
echo $TEST
```

Results:

```
hello-world
```

## Interactive Variables

If you include an environment variable that isn't set, SimDem will prompt 
you to give it a value and will add it to the running environment.

```
echo $NEW_VARIABLE $TEST
```

Results:

```
Enter a value for $NEW_VARIABLE: SimDem

SimDem hello-world

```

```
echo $LOCAL_TEST $TEST
```

Results:

```
A warm local hello hello-world
```

```
echo $NEW_VARIABLE $TEST
```

Results:

```
SimDem hello-world
```

## User provided environment

Since it is helpful to provide configuration files in published
scripts SimDem also provides a way for users to provide user specific
configurations. So that users can setup their demo's to use private
keys etc. These files are provided in the same way as `env.json` files
(i.e. in the project and tutorial sub-directories) but are called
`env.local.json`. These files take precedence over both project and
tutorial provided files.

For example, this project provides a local files in both the project
and this tutorial sub-directories. Note that in this case we have
checked them into version control as they are part of the example,
normally they would be added to your local '.gitignore' or equivalent.

```
cat ../env.local.json
```

Results:

```
{
    "LOCAL_TEST": "Hello from the local project config"
}
```

It also defines an 'env.json' file in the tutorial folder:

```
cat env.local.json
```

Results:

```
{
    "LOCAL_TEST": "A warm local hello"
}
```

The file that "wins" is the most local one, that is the one in the tutorial:

```
echo $LOCAL_TEST
```

Results:

```
A warm local hello
```


# Going Off-Script

You can go off-script if you want to. This is where you should hit 'b'
(for break). You will now be able to type a command to be
run. However, note that at the time of writing the parser for this
command is not very smart, so some commands do not work. In addition
you can't run fully interactive commands this way (so no editors for
example). Go ahead and try it, hit 'b' and type a command, e.g. 'ls'.

Note that when you hit 'b' you will not see any change in the output,
but you can now start typing freely.

```
```

# Running SimDem

SimDem is packaged as a container, you run it with:

`docker run -it rgardler/simdem`

This will run the demo script you are working through now.

## Adding Your Own Demo Script

You will likely want to add your own demo script. To do this you can
either build your own container or you can mount a volume which
contains your demo scripts. To mount a volume run:

`docker run -it -v ~/my_demo_dir:/demo_scripts rgardler/simdem`

When mounting a directory the script found in the first folder within
the mounted folder will be run. If you want to run a specific demo
within that folder add `run SCRIPT_NAME` to the command, where
SCRIPT_NAME is replaced with the name of the folder containing the
script you want to run. For example:

`docker run -it -v ~/my_demo_dir:/demo_scripts rgardler/simdem run myscript`

## Building your own Demo Container

Create a Dockerfile and add (at least) the following:

   ```
   FROM rgardler/simdem
   
   COPY my_script_dir demo_scripts
   ```

## Writing Scripts

At the very least a demo script consists of a script.md file. This
will contain both descriptinve text and command blocks describing the
commands that need to be run. These files are intended to be human
readable, however, you can use them to drive a simulation of the demo
being run. See next section for details.

Ideally script directories will also contain a `setup.sh` and
`clearup.sh` files. These are intended to be run to configure the demo
environment and to cleanup after the demo is complete.

### Including Results in the Script

When using the script as a web page or printout it is likley that you
will want to include the results. However, when you are running in a
simulation or tutorial mode you will want to rely on the real results
from the current run. You can include a "Results:" section after any
code block. The first code block after this text will be ignored when
running in an interactive mode (such as tutorial or simulation). That
is, in the example below, the `date -u` command will be run
interactively but the `Sat Mar 12 10:09:12 UTC 2016` will only be
included in a static form of the script.

    ```
    date -u
    ```

    Results:

    ```
    Sat Mar 12 10:09:12 UTC 2016
    ```

# Ending the Demo Run

When you reach the end of the script (like now) you will return to
your normal terminal.

If you ran with the `--test yes` flag (or with the command `test`)
then the final output will be a summary of test results. This script
is designed to have a failing test. Scroll back in the results to see
why it failed.

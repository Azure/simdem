This project provides ways to write tutorials in markdown that then
become interactive demo's and automated tests. You can run in a number
of different modes:

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

# Try it Out

The easiest way to try SimDem out is with a Docker container, this
approach is fully documented below. he most flexible way to run SimDem
is to use the Python code directly. This is generally best for
deelopers so we provide minimal documentation here.

## Python

To learn more install Python 3 and pip, then type the following
commands:

```
sudo pip3 install -r requirements.txt
python3 simdem.py --help
```

## Docker Containers

There are two containers available, the 'cli' version and the 'novnc'
version. The first is command line only, the latter provides a browser
based Linux desktop envirnment in which the CLI is availale. The NoVNC
version makes it easy to do demo's with browser based steps without
having to install any softare (other than Docker) on your client.

We provide scripts that make it easy to run the container and to load
custom scripts into it.

### CLI Container

The CLI container can be run in four modes:

Tutorial : in which full textual descriptions are provided
Learn    : similar to Tutorial mode, but users are expected to type the commands
Demo     : in which no textual descriptions are shown and commands are "typed"
Test     : run the tests

#### Tutorial Mode

It's easier to explain through action, so just run the container and
work through the interactive tutorial that is included

```
./scripts/run.sh cli
```

If you want to start execution in a different place, or load in your
own scripts provide the path as the second parameter. For example, the
following example skips the introductory text and runs the demo script
provided in the SimDem GitHub repository.

```
./scripts/run.sh cli demo_scripts/simdem
```

#### Learn mode

Learn mode is similar to tutorial mode, but the user is expected to
type the commands after being provided instructions.

```
./scripts/run.sh cli learn
```

If you want to start execution in a different place, or load in your
own scripts provide the path as the second parameter. For example, the
following example skips the introductory text and runs the demo script
provided in the SimDem GitHub repository.

```
./scripts/run.sh cli demo_scripts/simdem learn
```

#### Demo mode

To run the same file as a demo (that is without explanatory text and
with simulated typing)simply add a third paramater with the value
`demo` as folows:

```
./scripts/run.sh cli demo_scripts/simdem demo
```

#### Test mode

To run the same file as a series of tests use a third parameter value
of `test` as follows:

```
./scripts/run.sh cli demo_scripts/simdem test
```

### NoVNC Container

When running in NoVNC mode a lightweight Linux desktop is run inside
the container you can then access that container using a browser. To
run the container use:

```
./scripts/run.sh
```

Now connect using the URL http://HOSTNAME_OR_IP:8080/?password=vncpassword

Open a terminal and type:

```
simdem --help
```

To load your own demo scripts into this container use:

```
./scripts/run.sh novnc /path/to/scripts
```

# Hacking Guide

If you make changes to the code the easiest way to build and redeploy
the container is with the scripts in `scripts` directory. These
scripts pull the current version number from the SimDem.py (see
`SIMDEM_VERSION=x.y.z` near the top of the file. This version number
is used as the defaiult for the scripts in this folder.

## Building

./scripts/build.sh Builds the noVNC (browser based) version of
the container with the default tag of `rgardler/simdem_novnc:x.y.z`

## Running

./scripts/run.sh <SCRIPTS_DIR> Runs an instance of the noVNC container
with the name `simdem`, after stopping and deleting any existing
containers. This container uses a volume container called `azure_data`
to maintain state for the preferred Azure subscription and creates
another called `simdem_novnc_scripts` containing the scripts in the
provided `SCRIPTS_DIR` (or `./demo_scripts` if no vlaue provided).

## Publishing

The `latest` version is built from source on each commit. To publish a
tagged version use `./scripts/publish.sh` script.

Don't forget to bump the version number after using this script.

# Learn more

If you want to learn more before running the container then why not
read the interactive tutorial as
a
[markdown page on GitHub](https://github.com/rgardler/simdem/blob/master/demo_scripts/simdem/script.md).

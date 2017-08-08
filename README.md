This project provides ways to write tutorials in markdown that then
become interactive demo's and automated tests. You can run in a number
of different modes:

  * Tutorial: Displays the descriptive text of the tutorial and pauses
    at code blocks to allow user interaction.
  * Simulate: Does not display the descriptive text, but pauses at each
    code block. When the user hits a key the command is "typed", a
    second keypress executes the command.
  * Test: Runs the commands and then verifies that the output is
    sufficiently similar to the expected results (recorded in the
    markdown file) to be considered correct.
  * Script: Creates an executable bash script from the document
  * Auto: allows any of the above modes to be run but without user
    interaction

The application can be run in either a CLI mode, which is ideal for
console based demo's and tutorials, or it can be run using NoVNC for a
browser based desktop experience - that is, using only a browser you
can have a full desktop experience.

# Try it Out

The easiest way to try SimDem out is with a Docker container and work
through the embedded tutorial. The following command will run the
latest developer version of the code (i.e. there may be errors).

```
docker run -it rgardler/simdem
```

The most flexible way to run SimDem is to use the Python code
directly. This is generally best for developers of SimDem, so we
provide minimal documentation here. 

# Writing a Script

The above command will walk you through the SimDem documentation. Pay
particular attention to the Syntax page, but the short version is that
you are writing markdown with code blocks. For more information see
`demo_scripts/simdem/tutorial/script.md`.

## Running in a Docker Container

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

## Python

You can run the Python source without a Docker container. To learn
more install Python 3 and pip, then type the following commands:

```
sudo pip3 install -r requirements.txt
python3 simdem.py --help
```

## Azure Cloud Shell

The CLI version of SimDem works fine in Azure Cloud Shell, but you
need to install it manually at this time. Here's how..

```
git clone git@github.com:rgardler/simdem.git
cd simdem
./scripts/install.sh
simdem
```

# Hacking Guide

If you make changes to the code the easiest way to build and redeploy
the container is with the scripts in `scripts` directory. These
scripts pull the current version number from the config.py (see
`SIMDEM_VERSION=x.y.z`). This version number is used as the defaiult
for the scripts in this folder.

## Building

./scripts/build.sh Builds the noVNC (browser based) version of
the container with the default tag of `rgardler/simdem_novnc:x.y.z`

## Running

Use `./script/run.sh <FLAVOR> <SCRIPT_DIR>` to execture the container
using two volume containers (see below). The `FLAVOR` is either
`novnc` (for the browser based version) or `cli` fo rthe command line
version..

`azure_data` volume container is used to maintain details of your
Azure Subscription (including login details).

`simdem_VERSION_scripts` volume container has the scripts to execute
in the container, that is the contents in `SCRIPTS_DIR` (or `./demo_scripts` if no value provided).

### Running the NoVNC container

`./scripts/run.sh novnc <SCRIPTS_DIR>` runs an instance of the noVNC
container

Once the container is running you can connect to it at `http://HOST:8080?password=vncpassword`. Open a terminal and run:

`simdem` to run the default script

Use `simdem --help` for more information.

### Running the CLI container

`./scripts/run.sh cli <SCRIPTS_DIR>` runs an instance of the CLI
container

## Contributing

This is an open source project. Don't keep your code improvements,
features and cool ideas to yourself. Please issue pull requests
against our [GitHub repo](http://github.com/rgardler/simdem).

Be sure to use our Git pre-commit script to test your contributions
before committing, simply run the following command:

```
ln -s ../../pre-commit.sh .git/hooks/pre-commit
```

This project welcomes contributions and suggestions.  Most
contributions require you to agree to a Contributor License Agreement
(CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit
https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine
whether you need to provide a CLA and decorate the PR appropriately
(e.g., label, comment). Simply follow the instructions provided by the
bot. You will only need to do this once across all repos using our
CLA.

This project has adopted
the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see
the
[Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with
any additional questions or comments.

## Publishing

The `latest` version is built from source on each commit. To publish a
version tagged image use `./scripts/publish.sh <FLAVOR>` script. This
will publish both the CLI and NoVNC containers if no `FLAVOR` is
provided.

Don't forget to bump the version number after using this script. To do
this open simdem.py and find and edit the following line (somewhere
near the top of the file):

`SIMDEM_VERSION = "0.4.1"`

# Learn more

If you want to learn more before running the container then why not
read the interactive tutorial as
a
[markdown page on GitHub](https://github.com/rgardler/simdem/blob/master/demo_scripts/simdem/script.md).

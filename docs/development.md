# Preface

We would love for you to contribute to SimDem.  If there is anything that would make adoption/developing of SimDem easier, please open up an issue with your request.

# Setup Dev Environment

## Prerequisites

* python3
* pip3
* Linux shell

## Initialize

Fetch the necessary packages

```
pip3 install -r requirements.txt
```

## Validation

Verify the tests pass

```
python3 setup.py nosetests
```

# Code Structure

SimDem is broken into the following class types

## Parse

This class type parses the markdown document into a "SimDem Execution Object".  This object has everything SimDem needs to know on how to run the document (e.g. prerequisites, commands, validations, etc.)

Follow the links to see an [example document](../content/prerequisites/README.md) with its output [SimDem Execution Object](../content/prerequisites/expected_output.dump)

Implementations:
* [SimDem1](../simdem/parser/simdem1.py)

## Mode

This class contains the logic for how the markdown document is processed.

Implementations:
* [Demo mode](../simdem/mode/demo.py)
* [Automated mode](../simdem/mode/automated.py)
* [Dump](../simdem/mode/dump.py)
* [Tutorial](../simdem/mode/tutorial.py)

## Execute

This class type executes the desired commands into the shell

Implementations:
* [Bash](../simdem/executor/bash.py)
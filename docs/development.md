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
make init
```

## Validation

Verify the tests pass

```
make test
```

# Code Structure

SimDem is broken into the following class types

## Parse

This class type parses the markdown document into a "SimDem Execution Object".  This object has everything SimDem needs to know on how to run the document (e.g. prerequisites, commands, validations, etc.)

Implementations:
* Context 
* CodeBlock

Example SimDem Execution Object:
```
{ 'prerequisites': ['prereq.md', 'prereq-2.md'],
  'commands': [ { 'command': 'echo foo' },
                { 'command': 'echo bar' },
                { 'command': 'echo baz', 'expected_result': 'baz' } ]
        }
```

## Render

This class type formats the result of running the commands into the desired output

Implementations:
* Demonstration mode
* Automated mode (coming soon)

## Execute

This class type executes the desired commands into the shell

Implementations:
* Bash
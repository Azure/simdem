# SimDem

This project provides an easy way to convert tutorials written in markdown into interactive demos and automated tests. 

# Features

SimDem supports the following features:
* Command execution
* Environment variable injection
* Prerequisites
* Output validation

Details on the complete feature list can be found in the [feature documentation](docs/features.md).

# Getting Started

## Installation

Currently, it's only available for installation in development mode:

```
git clone git@github.com:Azure/simdem.git
git checkout -b simdem2 remotes/origin/simdem2
pip3 install -r requirements.txt
pip3 install -v -e .
```

Note: in rare machine configuations you may get a "simdem: command not
found" error after installing. If you see this error take a look at
the workaround in [issue #99](https://github.com/Azure/simdem/issues/99).

## Running

A great place to start working on SimDem is to run SimDem on its own documentation

```
simdem docs/README.md
```

## Documentation

It's more fun to run SimDem on it's own documentation; however, you can learn how how SimDem works by [reading the docs](https://github.com/Azure/simdem/tree/simdem2/docs).

We provide a [simple hello-world example](https://github.com/Azure/simdem/blob/simdem2/docs/hello_world.md).

### Examples

If you want to see existing examples, with expected output, check out the [examples](https://github.com/Azure/simdem/tree/simdem2/examples)

# Syntax

Currently, SimDem supports Markdown as the source document.  Details on how to compose Markdown documents can be found in the [syntax documentation](docs/syntax.md).

# Development

We would love to have you be a part of the SimDem development team.  For details, see the [development documentation](docs/development.md).

# History

SimDem v2 is a complete rewrite of SimDem v1.  The latest commit for v1 can be found at:
https://github.com/Azure/simdem/tree/cb1caf17fd684e125789c26817f43eeae0e1c523

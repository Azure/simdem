# Advanced Features

## Setup Script

A setup script is a simple way of bootstrapping your environment prior to running the document.

You might use this feature if you want to do the following before running the main documentation:
* Set environment variables
* Script prerequisite commands

Example usage:

```shell
simdem -s examples/setup-script/setup.sh examples/setup-script/README.md
```
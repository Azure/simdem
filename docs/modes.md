# Modes of Operation

SimDem and can be run one of the following modes:

* Tutorial: Displays the descriptive text of the tutorial and pauses
  at code blocks to allow user interaction.
* Demo: Does not display the descriptive text, but pauses at each
  code block. When the user hits a key the command is "typed", a
  second keypress executes the command.
* Test: Runs the commands and then verifies that the output is
  sufficiently similar to the expected results (recorded in the
  markdown file) to be considered correct.
* Dump:  Prints out the internal SimDem object

# Next Steps

  1. [Beginning](README.md)
  1. [Build Hello World Demo](hello_world.md)
  1. [SimDem document syntax](syntax.md)
  1. [Use your documents as an interactive tutorial](mode_tutorial.md)
  1. [Use your documents as an interactive demo](mode_demo.md)
  1. [Use your documents as an automated test](mode_test.md)
  1. [Dump your parsed documentation](mode_dump.md)
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

## Tutorial Mode

Tutorial mode is ideal if you are using this as a learning or teaching
tool (see also learn mode below, which suits some learning styles
better. In this mode a description of what you are about to do is
shown on the screen, hit a key to see the command, hit another key to
execute the command. Tutorial mode is the default.

To run a document in Tutorial Mode: `simdem content/simple/README.md`


## Demo (or Simulation) mode

Demo mode is ideal if you are using this to teach or demonstrate how
to achive the goal. In this mode no descriptive text is shown, instead
when you press a key the next command is "typed", pressing another key
will execute the command. The idea is that you describe what is
happening as the application "types" the command for you.

To run a document in Demo Mode: `simdem -m demo content/simple/README.md`


## Test Mode

Test mode runs the commands and then verifies that the output is
sufficiently similar to the expected results (recorded in the markdown
file) to be considered correct.

To run a document in Test Mode: `simdem -m test content/simple/README.md`

## Dump Mode

Dump mode is used for debugging to see how SimDem has parsed the document

To run a document in Dump Mode: `simdem -m dump content/simple/README.md`


# Next Steps

  1. [Beginning](README.md)
  1. [Build Hello World Demo](build_hello_world.md)
  1. [SimDem document syntax](syntax.md)
  1. [Use your documents as interactive tutorials or demos](demo_mode.md)
  1. [Use your documents as automated tests](test_mode.md)
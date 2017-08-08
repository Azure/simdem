# Modes of Operation

SimDem demos are interactive and can be run in a number of different
modes:

  * Tutorial: Displays the descriptive text of the tutorial and pauses
    at code blocks to allow user interaction.
  * Learn: similar to Tutorial mode, but users are expected to type
    the commands themselves.
  * Simulate: Does not display the descriptive text, but pauses at each
    code block. When the user hits a key the command is "typed", a
    second keypress executes the command.
  * Test: Runs the commands and then verifies that the output is
    sufficiently similar to the expected results (recorded in the
    markdown file) to be considered correct.
  * Script: Creates an executable bash script from the document
  * Auto: allows any of the above modes to be run but without user
    interaction

## Tutorial Mode

Tutorial mode is ideal if you are using this as a learning or teaching
tool (see also learn mode below, which suits some learning styles
better. In this mode a description of what you are about to do is
shown on the screen, hit a key to see the command, hit another key to
execute the command. Tutorial mode is the default.

## Learn mode

Learn mode is similar to tutorial mode above, however, in learn mode
the user is expected to type each command themselves. Some people find
that this aids recall.

## Demo (or Simulation) mode

Demo mode is ideal if you are using this to teach or demonstrate how
to achive the goal. In this mode no descriptive text is shown, instead
when you press a key the next command is "typed", pressing another key
will execute the command. The idea is that you describe what is
happening as the application "types" the command for you. To run in
demo mode use the `--style simulate` command line switch.

## Test Mode

Test mode runs the commands and then verifies that the output is
sufficiently similar to the expected results (recorded in the markdown
file) to be considered correct. To run in test mode use the `--test
yes` switch. For convenience you can use the command `test` to execute
tests with the optimal configuration for automated testing..

## Script mode

Script mode does not execute any of the commands, instead is outputs
an executable bash script that can be run without SimDem. Use the
command `script` to generate the executable script.

# Unnattended (Auto) Mode

Each of these modes can be run in auto mode too. This means that the
program does not wait for a keypress before proceeding. This can be
useful if you want to runthe complete script unattended. To run in
automated or unnattended mode use the `--auto true` command line
switch.

Manual mode is ideal if you would like to manually type the commands,
many people find this helps them remember. It can be useful in the
first few runs, but we still recommend using "demo" mode when doing
live demo's - it's much harder to make a mistake this way.

# Next Steps

  1. [Hello World Demo](../demo/script.md)
  2. [SimDem Index](../script.md)
  3. [Write SimDem documents](../syntax/script.md)
  4. [Build a SimDem container](../building/script.md)

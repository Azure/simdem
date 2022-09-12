# Modes of Operation

SimDem demos are interactive and can be run in a number of different
modes:

  * Tutorial: Displays the descriptive text of the tutorial and pauses
    at code blocks to allow user interaction.
  * Learn: similar to Tutorial mode, but users are expected to type
    the commands themselves.
  * Demo: Runs the complete script continuously, only pausing when custom input is required
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
execute the command. Tutorial mode is the default. `python3 main.py tutorial simdem`

## Learn mode

Learn mode is similar to tutorial mode above, however, in learn mode
the user is expected to type each command themselves. Some people find
that this aids recall. `python3 main.py learn simdem`

## Demo (or Simulation) mode

Demo mode is ideal if you are using this to teach or demonstrate how
to achieve the goal. In this mode no descriptive text is shown, and the script os continuously executed. `python3 main.py demo simdem`

## Test Mode

Test mode runs the commands and then verifies that the output is
sufficiently similar to the expected results (recorded in the markdown
file) to be considered correct. `python3 main.py test simdem`

## Script mode

Script mode does not execute any of the commands, instead is outputs
an executable bash script that can be run without SimDem. Use the
command `script` to generate the executable script. `python3 main.py script simdem`


# Next Steps

  1. [Hello World Demo](../demo/README.md)
  2. [SimDem Index](../README.md)
  3. [Write SimDem documents](../syntax/README.md)

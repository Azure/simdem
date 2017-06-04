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
  * Auto: allows any of the above modes to be run but without user
    interaction

# Try it Out

It's easier to explain through action, so just run the container and
work through the interactive tutorial that we include.

```
docker run -it rgardler/simdem
```

To run the same file as a demo (that is without explanatory text and
with simulated typing) as `--style simulate` to the command:

```
docker run -it rgrdler/simdem --style simulate
```

To run the same file as a series of tests us the `--test yes`
flag. When running in test mode you will usually want to also add the
`--auto yes` option to prevent the need for human intervention. 

```
docker run -it rgrdler/simdem --test yes --auto yes
```

For convenience you can use the command `test` to give the same
results as above:

```
docker run -it rgrdler/simdem test
```

## Running with your own scripts

To use your own demo script mount a directory with `script.md` into
the simdem containers `demo_scripts` directory.:

```
docker run -it -v ~/my_demo_dir:/demo_scripts rgardler/simdem
```

If you have more than one demo in your demo directory you can tell
SimDem which to run by passing a folder name:

```
docker run -it -v ~/my_demo_dir:/demo_scripts rgardler/simdem run ademo
```

See `demo_scripts/simdem/script.md` for details on how to write a demo
script.


# Learn more

If you want to learn more before running the container then why not read the interactive tutorial as a [markdown page on GitHub](https://github.com/rgardler/simdem/blob/master/demo_scripts/simdem/script.md).

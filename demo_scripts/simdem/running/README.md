# Running SimDem

SimDem is packaged as a container, you run it with:

`docker run -it rgardler/simdem`

This will run the demo script you are working through now.

## Adding Your Own Demo Script

You will likely want to add your own demo script. To do this you can
either build your own container or you can mount a volume which
contains your demo scripts. To mount a volume run:

`docker run -it -v ~/my_demo_dir:/demo_scripts rgardler/simdem`

When mounting a directory the script found in the first folder within
the mounted folder will be run. If you want to run a specific demo
within that folder add `run SCRIPT_NAME` to the command, where
SCRIPT_NAME is replaced with the name of the folder containing the
script you want to run. For example:

`docker run -it -v ~/my_demo_dir:/demo_scripts rgardler/simdem run myscript`

# Going Off-Script

You can go off-script if you want to. This is where you should hit 'b'
(for break). You will now be able to type a command to be
run. However, note that at the time of writing the parser for this
command is not very smart, so some commands do not work. In addition
you can't run fully interactive commands this way (so no editors for
example). Go ahead and try it, hit 'b' and type a command, e.g. 'ls'.

Note that when you hit 'b' you will not see any change in the output,
but you can now start typing freely.

```
echo "This is a dummy code block to ensure SimDem pauses in interactive mode"
```

# Repeating Commands

Sometimes a command will need to be run a number of times, for example
it might be monitoring the state of an operation. The easiest way to
repeat a command is simply to press 'r'.

```
echo "This is a dummy code block to ensure SimDem pauses in interactive mode"
```

# Next Steps

  1. [Use your documents as automated tests](../test/README.md)
  2. [SimDem Index](../README.md)
  3. [Modes of operation](../modes/README.md)
  4. [Build a SimDem container](../building/README.md)

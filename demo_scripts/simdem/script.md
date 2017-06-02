# Welcome to SimDem

Simdem allows you to run a simulated demo. It reads a script, written
in the form of a human readable markdown file, and executes the
commands on your behalf. It will even make it look like you are really
typing the commands, which is great if you want to concentrate on
explaining what you are doing but still run the demo live.

Each easier to desribe if you see it working. In fact you are already
in a SimDem. Press a key (other than 'b', we'll look at that shortly)
to "type" the `date` command, once the command has been "typed" hit
a key to run the command.

```
date
```

Results:

```
Sat Mar 12 08:59:01 UTC 2016
```

Cool huh?

```
echo $TEST
```

# A Tutorial That is Also a Demo

This text is being pulled from the `script.md` file inside the
`demo_scripts\simdem` folder. Since this is a markdown file this
document can also be rendered as a web page, blog post or event a Word
or PDF document. However, you don't have to display the text of the
document when running the demo. If you run the demo container with
`docker run rgardler/simdem simulate` then the text will be surpressed
and the typing will look more realistic, as though you are typing for
real.

Lets, try something else. Hit another key (other than 'b') to run a
different command (don't forget to hit a key to actually execute the
command).

```
echo "this is cool, when the output of this finishes, hit another key"
echo "and now hit enter to run this command"
```

As you can see we can run multiple commands, in sequence.

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
```

# Running SimDem

SimDem is packagesd as a container, you run it with:

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

## Building your own Demo Container

Create a Dockerfile and add (at least) the following:

   ```
   FROM rgardler/simdem
   
   COPY my_script_dir demo_scripts
   ```

## Writing Scripts

At the very least a demo script consists of a script.md file. This
will contain both descriptinve text and command blocks describing the
commands that need to be run. These files are intended to be human
readable, however, you can use them to drive a simulation of the demo
being run. See next section for details.

Ideally script directories will also contain a `setup.sh` and
`clearup.sh` files. These are intended to be run to configure the demo
environment and to cleanup after the demo is complete.

### Including Results in the Script

When using the script as a web page or printout it is likley that you
will want to include the results. However, when you are running in a
simulation or tutorial mode you will want to rely on the real results
from the current run. You can include a "Results:" section after any
code block. The first code block after this text will be ignored when
running in an interactive mode (such as tutorial or simulation). That
is, in the example below, the `date -u` command will be run
interactively but the `Sat Mar 12 10:09:12 UTC 2016` will only be
included in a static form of the script.

    ```
    date -u
    ```

    Results:

    ```
    Sat Mar 12 10:09:12 UTC 2016
    ```

# Ending the Demo Run

When you reach the end of the script (like now) you will return to
your normal terminal.

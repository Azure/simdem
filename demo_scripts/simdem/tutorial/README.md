# Removed as I believe a lot of this info comes in the main readme and in the building our own simdem script.


# Writing a SimDem script

This document desribes how to write a SimDem script. 

## Install SimDem

These commands can't be run from within SimDem - danger of turning the
whole world into a recursive simulation of itself ;-). Therefore you
should execute them on your client (Linux, Mac or Windows Subsystem
for Linux).

`git clone https://github.com/Azure/simdem.git`
`cd simdem`
`pip3 install -r requirements.txt`
`python3 main.py tutorial simdem`

This last command will launch you into the SimDem documentation. If
you haven't reviewed it already you should do so, of particular
importance is the Syntax section.

## Hello World Script

Let's build a hello world script:

```bash
mkdir -p hello_world
echo "# Hello World Script" > hello_world/README.md
```

## Run the script

You can't run SimDem within SimDem so if you are reading this from
within SimDem you will need to exit and run `simdem -p hello_world` to
see this in action.

# Next Steps

Now you have a working hello world script you are on your own (not
really ask questions / report bugs via the
http://github.com/rgardler/simdem issue tracker). If you feel a little
lost then try one of these documents for guidance:

  1. [Review SimDem Syntax](../syntax/README.md)
  2. [Understand how to parameterize scripts](../variables/README.md)
  3. [Understand how to make a script a test](../test/README.md)


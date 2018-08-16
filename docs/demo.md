# Hello World SimDem Demo

This script is intended to be used to demonstrate the key features of
Simdem.

When you hit 'spacebar' a command will be displayed and
executed. Actually you can hit almost any key but we recommend
'spacebar' here because we've not told you about the special keys yet
and spacebar is not one of them.

```
echo "Hello World"
```

That's cool, lets try again:

```
echo "It might look like this was typed into the terminal, but it really comes from a markdown file."
```

The date command will show that these commands are being executed in real time.

```
date
```

Results: 

```expected_similarity=0.3
Sat Mar 12 08:59:01 UTC 2016
```

You can run almost any shell command this way.

# Special keys

Although we said "spacebar" above, in reality you can hit almost any
key. There are a few exceptions though:

## 'd' for description

Hitting 'd' will print all the text since the last command, that is it
will print the description of the next command to be executed.

```
echo "Hitting 'd' now will display the description for this command."
```

## 'b' for break

Hitting 'b' will "break" from the current script. This allows you to
type in commands that are not part of the script. This is particularly
useful when running in demo mode as it alllows you to respond to
questions by entering an unscripted command.

```
echo "Give it a go, why not hit 'b' and type 'ls', or some other command"
```

NOTE: at the time of writing it is not possible to use interactive
commands or commands.

# Next Steps

It's possible to provide a branching point a the end of a script. The
user can select one of a selection of options or they can enter "quit"
(or just "q") to exit SimDem.

  1. [Write SimDem documents](../syntax/README.md)
  2. [SimDem Index](../README.md)
  3. [Modes of operation](../modes/README.md)




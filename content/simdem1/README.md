# Prerequisites

This is the prerequisite section.  SimDem looks for a set of links to extract and run through first

* [prereq-ignored](content/simdem1/prereq-ignored.md)

They don't even need to be in the same list

* [prereq-processed](content/simdem1/prereq-processed.md)

By this point, the prerequisites have either run or have passed their validation

# Did our prerequisites run?

```shell
echo prereq_ignored = $prereq_ignored
echo prereq_processed = $prereq_processed
```

# Do stuff here

We want to execute this because the code type is shell

```shell
echo foo
echo bar
var=foo
```


# Do more stuff here

```shell
echo baz
```

# Results

The only thing that makes it a result is the code type is result.
We assume the result is for the last command of the last code block

```result
baz
```

# Next Steps

The list inside this block are steps that could be followed when performing an interactive tutorial

  1. [Step #1](step-1.md)
  1. [Step #2](step-2.md)



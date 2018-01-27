# Prerequisites

This is the prerequisite section.  SimDem extracts links to run through prior to executing the main steps.

Here is an example of a prerequisite that will be ignored because it's conditions are already met.

* [prereq-ignored](./prereq-ignored.md)

Here is an example of a prerequisites that will be run because it's conditions are not met.

* [prereq-processed](./prereq-processed.md)

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
var=bar
```


# Do more stuff here

We assume the result is for the last command of the last code block

```shell
echo baz
echo $var
```

Results:

```result
bar
```

# Next Steps

The list inside this block are steps that could be followed when performing an interactive tutorial

  1. [Step #1](step-1.md)
  1. [Step #2](step-2.md)



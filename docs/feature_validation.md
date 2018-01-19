# Automated Testing

When running with the `--test` flag  will verify that the output of each command is as expected. It does this by comparing the output of the command with the subsequent `Results:` section in the script. 

```
cat docs/feature_validation.md
```

## Running in test mode

Running with demo renderer will not check the results against expectations. However, running with the `test` command will do so.

```
echo "This test is expected to fail"
```

Results:

```
It fails because the results we have in the script are significantly 
different to the output of the command.
```

By default a 66% or more match indicates a pass. However, in some
cases a much lower similarity is expected, for example, the output of
`date` will vary considerably each time it is run. In these situations
you can provide an expected similarity as part of the three backticks
that start a code block, for example ```Expected_Similarity=0.2 which
is low enough for the test to be recorded as a pass. Note, it is
important that you do not insert any spaces in this notation.

```
date
```

Results: 

```Expected_Similarity=0.2
Tue Jun  6 15:23:53 UTC 2017
```

# Fast Fail

The default setting is for SimDem to stop the test run on the first
test failure. This can be overridden by setting the command line flag
`--fastfail` to any value other than `True`.

# Test Plans

It is often a good idea to split tests into separate files. SimDem
will allow you to do this by providing a `test_plan.txt` file. Each
line in this file is either a comment (lines starting with '#') or a
filename for a SimDem script to be used in testing. Each of these
files will be concatenated together to create a complete test plan.

For example, the following example `test_plan.txt` will run all the
code and tests in `preparation/README.md` followed by those in
`main/README.md` and finally those in `cleanup/README.md`.

`
preparation/README.md
main/README.md
cleanup/README.md
`

# Next Steps

  1. [SimDem Index](README.md)
  2. [Build a Hello World script](hello_world.md)
  3. [Write SimDem documents](syntax.md)

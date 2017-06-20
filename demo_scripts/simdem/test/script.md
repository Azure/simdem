# Automated Testing

When running with the `--test` flag or using the `test` command SimDem
will verify that the output of each command is as expected. It does
this by comparing the output of the command with the `Results:`
section in the script. 

First, lets take a look at the source of this file. 

```
cat $SIMDEM_CWD/script.md
```

## Running in test mode

Running in demo mode will not check the results against
expectations. However, running with the `test` command will do so.

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
you can provide an expected similarity as part of your `Results:`
section header, for example in the below section we have `Results:
Expected similarity: 0.2` which is low enough for the test to be
recorded as a pass.:


```
date
```

Results: Expected Similarity: 0.2

```
Tue Jun  6 15:23:53 UTC 2017
```

# Next Steps

  1. [SimDem Index](../script.md)
  2. [Write SimDem documents](../syntax/script.md)
  3. [Configure your scripts through variables](../variables/script.md)

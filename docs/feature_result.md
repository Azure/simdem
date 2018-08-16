# Command Testing

An example of a Result test is:

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

`
preparation/README.md
main/README.md
cleanup/README.md
`

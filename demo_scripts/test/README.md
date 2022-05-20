# SimDem Test Script

This is a simple test script. It runs a number of commands in
succession. This script also lists commands known not to work.

# Setup

Ensure the test environment is correctly setup.

## SimDem version check

```
echo $SIMDEM_VERSION
```

Results:

```expected_similarity=0.8
0.8.2-dev
```

## Clean test working files

Ensure that our working files folder exists and that there are no
residual files from previus test runs.

```
echo $SIMDEM_TEMP_DIR
mkdir -p $SIMDEM_TEMP_DIR/test
rm -Rf $SIMDEM_TEMP_DIR/test/*
```

# Prerequisites

Test to see if our prerequesites work. In the setup we cleaned out our
test files. The [prerequisite test script](./prerequisites/README.md)
validates whether the file exists and, if it doesn't it will execute
and create it.

This will run our Azure test scripts. 
The [Azure scripts](./azureTests/README.md) 
creates azure resources and validates that our
current documentation is up to date

Each [prerequisite](./prerequisites/README.md) will only be run once,
so even though this partucular prereq appears twice it will only
execute once. This is important when building multi-part tutorials/
demos where a prereq may be included in more than one part.

## Validate prerequisite ran

The prerequisite script should have run and created a `prereq_ran`
file.

```
ls $SIMDEM_TEMP_DIR/test
```

Results:

```
prereq_ran
```


# Directory Check

```
head -n 1 README.md
```

Results: 

``` Expected_Similarity=0.8
# SimDem Test Script
```

# Simple Echo

``` 
echo "Hello world" 
```

Results: 

```
Hello world
```

# Code comments

```
# This is a comment and should be ignored
echo "This output should be displayed, the comment before this line should be ignored"
```

Results:

```
This output should be displayed, the comment before this line should be ignored
```

# Expected different results

When we know the results will be different and we want to use them in
tests we need to override the similarity expected by adding
`expected_similarity=x.y` in the start line of the results block:

```
date
```

Results: 

```expected_Similarity=0.1
Tue Jun  6 15:23:53 UTC 2017
```

# For Loop

Because SimDem will interactively ask for values for undefined
variables it is sometimes necessary to first declare a variable to
prevent this action. For example:

```
i=0
for i in {0..10}; do echo "Welcome $i times"; done
```

Results:

```
Welcome 0 times
Welcome 1 times
Welcome 2 times
Welcome 3 times
Welcome 4 times
Welcome 5 times
Welcome 6 times
Welcome 7 times
Welcome 8 times
Welcome 9 times
Welcome 10 times
```

# Stripping ANSI escape sequances

To make it easier to write scripts we don't want to include ANSI
escape sequences (such as colors and text deocration) in the results
section. SimDem automatically strips these when capturing the results.

```
printf "Normal \e[4mUnderlined\e[24m Normal"
```

Results:

```expected_similarity=0.9
Normal Underlined Normal
```




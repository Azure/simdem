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

```
0.7.4-dev
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
echo $SIMDEM_CWD
```

Results: 

``` Expected_Similarity=0.8
demo_scripts/test/
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

```expected_Similarity=0.2
Tue Jun  6 15:23:53 UTC 2017
```

# For Loop

```
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
echo -e "Normal \e[4mUnderlined\e[24m Normal"
```

Results:

```expected_similarity=0.9
Normal Underlined Normal
```

# Commands that do not work

  * ping bing.com
  * curl bing.com

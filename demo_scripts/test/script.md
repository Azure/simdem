# SimDem Test Script

This is a simple test script. It runs a number of commands in
succession. This script also lists commands known not to work.

# Version check

```
echo $SIMDEM_VERSION
```

Results:

```
0.4.1
```

# Directory Check

```
echo $SIMDEM_CWD
```

Results: 

``` Expected_Similarity=0.9 
demo_scripts/test/
```

# Configuraiton Check

We should be able to retrieve environment variables from the directory
in which the command was given:

```
cat env.json
```

Results:

```
{
    "TEST": "Hello from the current working directory (where the simdem command was executed)"
}
```

We should also be able to retrieve locallay defined environment
variables from the directory in which the command was given:


```
cat env.local.json
```

Results:

```
{
    "TEST": "A local hello from the current working directory (where the simdem command was executed)"
}
```

There should also be environment variables in the the directory in
which the current script resides.

```
cat $SIMDEM_CWD/env.json
```

Results:

```
{
    "TEST": "Hello from the test script"
}
```

Local variables can also be found in the the directory in which the
current script resides.

```
cat $SIMDEM_CWD/env.local.json
```

Results:

```
{
    "TEST": "A local hello from the current working directory (where the simdem command was executed)"
}
```

For the `TEST` variable we should have the `env.local.json` value from
the directory in which the application was executed.

```
echo $TEST
```

Results:

```
A local hello from the current working directory (where the simdem command was executed)
```

There should be variable definitions in the parent of the
current script directory:

```
cat $SIMDEM_CWD/../env.json
```

Results:

```
{
  "PARENT_TEST": "Hello from the parent"
}
```

Since the value of `PARENT_TEST` is only defined in this file we
should have the value from there:

```
echo $PARENT_TEST
```

Results:

```
Hello from the parent
```

## Test Environment

We can also provide values in `env.test.json` in either the script
directory or the parent of the script directory. If available these
will be loaded first and overwritten by subsequent `env.json` and
`env.local.json` files. For this reason if you want to dorce the user
to provide a value for an environment variable it is important that
you define it as an empty string in `env.json` if a value has been
provided in `env.test.json`.


```
echo $TEST_VALUE
```

Results:

```
Test value for the test script
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

# Commands that do not work

  * ping bing.com
  * curl bing.com

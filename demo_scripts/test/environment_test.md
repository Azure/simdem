# Environment tests

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

# Capturing the output of commands

```
CAPTURED_OUTPUT=$(uname)
```

Captured value is:

```
echo $CAPTURED_OUTPUT
```

Results:

```
Linux
```

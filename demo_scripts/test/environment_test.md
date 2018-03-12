# Environment tests

We should be able to retrieve environment variables from the directory
in which the command was given. Note that SimDem provides the
environment variable `SIMDEM_EXEC_DIR` which provides access to this
folder in SimDem scripts should it be necessary.

```
cat $SIMDEM_EXEC_DIR/./env.json
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
cat env.json
```

Results:

```
{
    "TEST": "Hello from the test script",
    "DIR_IN_HOME": "~/should/be/expanded"
}
```

Local variables can also be found in the the directory in which the
current script resides.

```
cat env.local.json
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
cat ../env.json
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

# Replacing variables in special commands

Some commands cannot be run in headless mode, e.g. `xdg-open`. These
commands will be replaced with an appropriate alternative,
e.g. `curl`. Variables included in such commands will be expanded at
execution time as expected.

```
url=http://bing.com
xdg-open $url
```

Results: 

```expected_similarity=0.2
HTTP/1.1 405 Method Not Allowed
Content-Length: 0
Server: Microsoft-IIS/10.0
X-MSEdge-Ref: Ref A: D6871D12117C436FAE3762BC8BCA0C29 Ref B: CO1EDGE0415 Ref C: 2017-08-17T15:37:59Z
Date: Thu, 17 Aug 2017 15:37:58 GMT
```

Note: this test will only pass when running in headless mode as the
`xdg-open` command will be executed in other environments.

# Setting new variables in script

If a script sets a variable during execution this will be recorded in
the SimDem environment. This includes setting to an empty string, this
will prevent SimDem interactively requesting a value for the variable
(or setting a dummt value in test mode).

```
new_var=""
echo $new_var
```

Results:

```expected_similarity=0.2
```

# Capturing the output of commands

```
CAPTURED_OUTPUT=$(echo foo | sed 's/foo/bar/')
```

Captured value is:

```
echo $CAPTURED_OUTPUT
```

Results:

```
bar
```

# Processing of Environment Variables

'~' should be expanded to a home directory (no way to test this).

```
echo $DIR_IN_HOME
```

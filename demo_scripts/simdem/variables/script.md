# Environment Variables

In order to use environment variables, you can define one or more
files. These variables are available in every command that is
executed.

Tutorials can carry `env.json` files in the project directory and/or
in tutorial sub- directories. Files in tutorial sub-directories will
overwrite settings pulled from the project directory. 

This tutorial defines an 'env.json' in the project directory:

```
cat $SIMDEM_CWD/../env.json
```

Results:

```
{
    "TEST": "Hello from the project"
}
```

It also defines an 'env.json' file in the tutorial folder:

```
cat $SIMDEM_CWD/env.json
```

Results:

```
{
    "TEST": "hello-world"
}
```

The file that "wins" is the most local one, that is the one in the tutorial:

```
echo $TEST
```

Results:

```
hello-world
```

## Interactive Variables

If you include an environment variable that isn't set, SimDem will prompt 
you to give it a value and will add it to the running environment.

```
echo $NEW_VARIABLE $TEST
```

Results: Expected similarity: 0.5

```
Enter a value for $NEW_VARIABLE: SimDem

SimDem hello-world

```

```
echo $LOCAL_TEST $TEST
```

Results: 

```
A warm local hello hello-world
```

```
echo $NEW_VARIABLE $TEST
```

Results: Expected similarity: 0.5

```
SimDem hello-world
```

## User provided environment

Since it is helpful to provide configuration files in published
scripts SimDem also provides a way for users to provide user specific
configurations. So that users can setup their demo's to use private
keys etc. These files are provided in the same way as `env.json` files
(i.e. in the project and tutorial sub-directories) but are called
`env.local.json`. These files take precedence over both project and
tutorial provided files.

For example, this project provides a local files in both the project
and this tutorial sub-directories. Note that in this case we have
checked them into version control as they are part of the example,
normally they would be added to your local '.gitignore' or equivalent.

```
cat $SIMDEM_CWD/../env.local.json
```

Results:

```
{
    "LOCAL_TEST": "Hello from the local project config"
}
```

It also defines an 'env.json' file in the tutorial folder:

```
cat $SIMDEM_CWD/env.local.json
```

Results:

```
{
    "LOCAL_TEST": "A warm local hello"
}
```

The file that "wins" is the most local one, that is the one in the tutorial:

```
echo $LOCAL_TEST
```

Results:

```
A warm local hello
```

## SimDem Environemnt Variables

SimDem provides some information about itself in environment
variables. These are all nameed `SIMDEM_*`. At present the available
variables are:

```
env | grep "SIMDEM_"
```

# Next Steps

  1. [SimDem Index](../script.md)
  2. [Use your documents as interactive tutorials or demos](../running/script.md)
  3. [Use your documents as automated tests](../testing/script.md)
  4. [Build a SimDem container](../building/script.md)

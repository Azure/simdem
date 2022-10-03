# Environment Variables

In order to use environment variables, you can define one or more
files. These variables are available in every command that is
executed.

Tutorials can carry `env.json` files in the directory the simdem
command was run and/or in tutorial sub-directories. Files in tutorial
sub-directories will overwrite settings pulled from the project
directory.

For example, this tutorial defines an 'env.json' in the `simdem`
parent folder and in the `variables` subdirectory that contains this
script. Here is the content from the test subdirectory.

```bash
cat $SIMDEM_CWD/env.json
```

Results:

```
{
    "NAME": "Hello from the variables subdirectory"
}
```

It also defines an 'env.json' file in the `SimDem` root
folder. Assuming you executed the `simdem` command from within that
folder the followin command will display it's content.

```bash
cat env.json
```

Results:

```
{
    "TEST": "A local hello from the current working directory (where the simdem command was executed)"
}	
```

Finally, a project may define an `env.local.json` file in the
directory from which the `simdem` command is run. This file is the
last to be loaded and overrides all other values.

Values are loaded in the following order, the last file to define a
        vlaue is the one that "wins".
        
    - PARENT_OF_SCRIPT_DIR/env.json
    - SCRIPT_DIR/env.json
    - PARENT_OF_SCRIPT_DIR/env.local.json
    - SCRIPT_DIR/env.local.json
    - CWD/env.json
    - CWD/env.local.json


## Interactive Variables

If you include an environment variable that isn't set, SimDem will
prompt you to give it a value and will add it to the running
environment. If you are running in test mode the variable will be
given a value of 'Dummy vlaue for test'.

```bash
echo $NEW_VARIABLE
```

Results: 

``` Expected_Similarity=0
Enter a value for $NEW_VARIABLE: SimDem

SimDem

```

### Defining variables can be important

Because SimDem will interactively ask for values for undefined
variables it is sometimes necessary to first declare a variable to
prevent this action. For example:

```bash
i=0
for i in {0..4}; do echo "Welcome $i times"; done
```

Results:

```
Welcome 0 times
Welcome 1 times
Welcome 2 times
Welcome 3 times
Welcome 4 times
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

```bash
cat $SIMDEM_CWD/../env.local.json
```

Results:

```
{
    "LOCAL_TEST": "Hello from the local project config"
}
```

It also defines an 'env.json' file in the tutorial folder:

```bash
cat $SIMDEM_CWD/env.local.json
```

Results:

```
{
    "LOCAL_TEST": "A warm local hello"
}
```

The file that "wins" is the most local one, that is the one in the tutorial:

```bash
echo $LOCAL_TEST
```

Results:

```
A warm local hello
```

## SimDem Environment Variables

SimDem provides some information about itself in environment
variables. These are all nameed `SIMDEM_*`. At present the available
variables are:

```bash
env | grep "SIMDEM_"
```

# Next Steps
  1. [Write multi-part documents](multipart/README.md)
  2. [Use your documents as automated tests](../test/README.md)
  3. [SimDem Index](../README.md)


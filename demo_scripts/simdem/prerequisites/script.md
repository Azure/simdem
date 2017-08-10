# Understanding Prerequisites

Prerequisite scripts are scripts that must be run in order for another
script to work. When SimDem finds a pre-requisite section it will test
whether the steps have been completed (see validation below). If the
validation tests fail then the code blocks in the pre-requisite script
are executed.

There aren't really any pre-requisites for this tutorial /
demo. Howeve,r this document is inserted as a pre-requisite so that we
can see how they work.

# Syntax Prerequisites

The prerequisites section starts with a heading of `# prerequisites`.

The body of this section will contain 0 or more links to a script that
should be run ahead of the current one.

The scripts should appear in the order of required exection in the body.

# Behavior

When a prerequisite script is identified SimDem will ask the user if
they have satisfied the requirement. If SimDem is running in test or
auto mode it is assumed that prerequisites have been satisified.

If the user indicates a prerequisite has been satisfied then execution
moves to the next prerequisite or onto the rest of the script.

If the user indicates a prereqiusite has not been satisfied then the
required script is executed.

# Automatically validating Pre-requisites

Some pre-requisite steps can take a long time to execute. For this
reason it is possible to provide some validation checks to see if the
pre-requisite step has been completed. These are defined in a section
towards the end of the script, before the next steps section (if one
exists). The validation steps will be executed by SimDem *before*
running the pre-requisite steps, if the tests in that section pass
then there is no need to run the pre-requisites.

It's easier to explain with an example.

Imagine we have a prerequisite step that takes 5 seconds, we don't
want to wait 5 seconds only to find that we already completed that
pre-requisite (OK, we know 5 seconds is not long, but it's long enough
to serve for this demo). For this example we will merely sleep for 5
seconds then touch a file. To validate this prequisite has been
satisfied we will test the modified date of the file, if it has been
modified in the last 5 minutes then the pre-requisite has been
satisfied.

```
sleep 5
echo $SIMDEM_TEMP_DIR
mkdir -p $SIMDEM_TEMP_DIR
touch $SIMDEM_TEMP_DIR/this_file_must_be_modfied_every_minute.txt
```

Now we have a set of commands that should be executed as part of this
pre-requisite. In order to use them we simply add a reference to this
file in the pre-requisites section of any other script. The following
"Validation" section will be executed before the above step

# Validation

For this pre-requisite we need to ensure that the test.txt file has
been updated in the last 5 minutes. If not then we need to run the
commands in this document. If you are running through this document in
SimDem itself then it might be worth going back to the page that calls
this as a pre-requisite, as long as you do this in the next five
minutes you won't come back here. You can do this by selecting
"Understanding SimDem Syntax" in the next steps section.

``` 
find $SIMDEM_TEMP_DIR -name "this_file_must_be_modfied_every_minute.txt" -newermt "1 minutes ago"
```

Results:

```
/home/<username>/.simdem/tmp/this_file_must_be_modfied_every_minute.txt
```

# Next Steps

  1. [Understanding SimDem Syntax](../syntax/script.md)
  2. [Configure your scripts through variables](../variables/script.md)
  3. [Build a Hello World script](../tutorial/script.md)
  4. [SimDem Index](../script.md)
  5. [Write multi-part documents](../multipart/script.md)
  6. [Use your documents as interactive tutorials or demos](../running/script.md)



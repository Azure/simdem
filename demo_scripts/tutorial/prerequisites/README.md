# Understanding Prerequisites

Prerequisite scripts are scripts that must be run in order for another
script to work. When SimDem finds a pre-requisite section it will test
whether the steps have been completed (see validation below). If the
validation tests fail then the code blocks in the pre-requisite script
are executed.

There aren't really any pre-requisites for this tutorial /
demo. Howeve,r this document is inserted as a pre-requisite so that we
can see how they work.

# Prerequisites Syntax

The prerequisites section starts with a heading of `# prerequisites`.

The body of this section will contain 0 or more links to a script that
should be run ahead of the current one.

The scripts should appear in the order of required exection in the body.

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

```bash
sleep 5
echo $SIMDEM_TEMP_DIR
mkdir -p $SIMDEM_TEMP_DIR
touch $SIMDEM_TEMP_DIR/this_file_must_be_modfied_every_minute.txt
```

Now we have a set of commands that should be executed as part of this
pre-requisite. In order to use them we simply add a reference to this
file in the pre-requisites section of any other script. 

Any code in a section headed with '# Validation' will be used by
SimDem to test whether the pre-requisites have been satisfied. If
validation tests pass the pre-requisite step will be skipped over,
otherwise the other commands in the script will be executed.

# Validation

In order to continue with our example we include some vlaidation steps
in this script. If you have not run through the commands above less
than one minute ago this validation stage will fail. If you are
working through this tutorial now you just executed the above
statements and so the tests here will pass, but if you include this
file as pre-requisite again it may well fail and thus automatically
execute this script.

For this pre-requisite we need to ensure that the test.txt file has
been updated in the last 5 minutes. If not then we need to run the
commands in this document. If you are running through this document in
SimDem itself then it might be worth going back to the page that calls
this as a pre-requisite, as long as you do this in the next five
minutes you won't come back here. You can do this by selecting
"Understanding SimDem Syntax" in the next steps section.

```bash
find $SIMDEM_TEMP_DIR -name "this_file_must_be_modfied_every_minute.txt" -newermt "1 minutes ago"
```

Results:

```
/home/<username>/.simdem/tmp/this_file_must_be_modfied_every_minute.txt
```

# Next Steps

  1. [Understanding SimDem Syntax](../syntax/script.md)
  2. [Configure your scripts through variables](../variables/script.md)
  3. [SimDem Index](../script.md)
  4. [Write multi-part documents](../multipart/script.md)



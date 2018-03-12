# A remote script

This file will be pulled from GitHub as a remote file to ensure that
execution of remote files works. It is pulled into the test suite in
two ways:

  1. As a remote prerequisite
  2. AS a remote file in a test plan

# Create the test file

```
mkdir -p $SIMDEM_TEMP_DIR/test
touch $SIMDEM_TEMP_DIR/test/remote_prereq_ran
```

# Validation

If the `remote_prereq_ran` file exists then we don't need to run this
script. In our tests the setup phase removes this file so the
validation test should always fail.

```
ls $SIMDEM_TEMP_DIR/test
```

Results:

```
nested_prereq_ran
prereq_ran
remote_prereq_ran who
```

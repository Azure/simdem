# Test Prerequisites

This script is not included as part of the test plan, but it should be
executed as part of the root `script.md`. Therefore, there should be a
file called `prereq_ran` in the temp directory.

```
touch $SIMDEM_TEMP_DIR/test/prereq_ran
```

# Validation

If the `prereq_ran` file exists then we don't need to run this
script. In our tests the setup phase removes this file so the
validation test should always fail.

```
ls $SIMDEM_TEMP_DIR/test
```

Results:

```
prereq_ran
```

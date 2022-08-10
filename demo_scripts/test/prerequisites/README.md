# Test Prerequisites

This script is not included as part of the test plan, but it should be
executed as part of the root `script.md`. Therefore, because of this
prerequisite there should be a file called `prereq_ran` and another
called `nested_prereq_ran` in the temp directory.

# Prerequisites

We should be able to run [nested prerequisites](./nested_prereq.md).

# Create the test file

```bash
touch $SIMDEM_TEMP_DIR/test/prereq_ran
```

# Validation

If the `prereq_ran` file exists then we don't need to run this
script. In our tests the setup phase removes this file so the
validation test should always fail.

```bash
echo temp is $SIMDEM_TEMP_DIR
ls $SIMDEM_TEMP_DIR/test
```

Results:

```
nested_prereq_ran
prereq_ran
```

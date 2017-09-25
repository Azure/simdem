# Nested Prerequisites

This prerequisite is executed from the main prerequisite test file.

# Create the test file

```
touch $SIMDEM_TEMP_DIR/test/nested_prereq_ran
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
nested_prereq_ran
```

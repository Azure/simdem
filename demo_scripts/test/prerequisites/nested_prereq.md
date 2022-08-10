# Nested Prerequisites

This prerequisite is executed from the main prerequisite test file.

# Create a test file

```bash
touch $SIMDEM_TEMP_DIR/test/nested_prereq_ran
```

# Validation

If the `prereq_ran` file exists then we don't need to run this
script. In our tests the setup phase removes this file so the
validation test should always fail.

```bash
ls $SIMDEM_TEMP_DIR/test
```

Results:

```expected_similarity=0.5
nested_prereq_ran
```

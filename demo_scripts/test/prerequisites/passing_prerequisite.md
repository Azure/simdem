# Passing Prerequisite

This is a dummy prerequisite file that contains a validation step that
will always pass and thus the body of this script will never be
executed. To ensure this is the case when we run tests we have placed
a failing test in the body.

```bash
echo "This test will always fail"
```

Results:

```
So we can ensure it never runs (the validation step will always pass)
```

# Validation

This section is used to ensure that the commands in this document succeeded.

```bash
echo "This validation step is designed to always pass"
```

Results:

```expected_similarity=0.5
This validation step is designed to always pass
```

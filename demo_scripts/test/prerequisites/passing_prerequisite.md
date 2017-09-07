# Passing Prerequisite

This is a dummy prerequisite file that contains a validation step that
will always pass and thus the body of this script will never be
executed. To ensure this is the case when we run tests we have placed
a failing test in the body.

```
echo "This test will always fail"
```

Results:

```
So we can ensure it never runs (the validation step will always pass)
```

# Validation

```
echo "This validation step is designed to always pass"
```

Results:

```
This validation step is designed to always pass
```

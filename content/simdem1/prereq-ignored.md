# WE ARE IN prereq-ignored.md

This file is designed to have the validation pass.  This means that we should stop executing this document after the results section

# Validation

This is a validation section.  If this validation section passes, we stop processing this file.  The command below should be the last text displayed

```
echo prereq_validation_pass
```

Results:

```
prereq_validation_pass
```

# Main area

This should never be run since the validation for the prereq has been met

```
echo YOU SHOULD NOT SEE THIS
```

# Set a variable that passes through

```
prereq_ignored=true
```

# WE ARE IN prereq-processed.md

This file is designed to have the validation fail.  This means that we should completely execute this file

# Validation

This is a validation section.  If this validation section passes, we stop processing this file

```
echo prereq_validation_fail
```

Results:

```
blah
```

# Main area

This should be run since the validation for the prereq has failed

```
echo YOU SHOULD SEE THIS
```

# Set a variable that passes through

```
prereq_processed=true
```

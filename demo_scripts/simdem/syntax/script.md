# Document syntax

For the most part SimDem uses
standard
[Markdown syntx](https://daringfireball.net/projects/markdown/syntax). There
are a few special strings that can be used to influence how SimDem
works, but even these are intended to be human readable, thus
preventing the need to maintain separate documents for the different
use cases (documentation, tutorial, demo, test and script).

For example, lets take a look at the start of this file this file:

```
head -n 25 $SIMDEM_CWD/script.md 
```

# Prerequisites

It is common for a tutorial or demo to have a number of
prerequisites. For example, it's a good idea to understand how these
work, so take a look at our [prerequisites](./prerequisites/script.md)
before proceeding.

# SimDem Syntax

There are a small number of SimDem specific items that you should be
aware of. They are detailed in the next few sections.

## Code Blocks

In SimDem a code block is marked in exactly the same way it is in
Markdown, that is with three backticks (``````). Unless a Code Block
is marked as a Results block (see next section) it is assumed that
this is executable code. SimDem will execute each line individually.

For example:

```
# This is a code block, this comment will be ignored by SimDem
echo "This command will be 'typed' and executed."
```

### Command Limitations

At the time of writing it is not possible to have interactive
commands. If you try to include such a command SimDem will "hang" as
it waits, silently, for input.

## Result Blocks

### Including Results in the Script

When using the script as a web page or printout it is likley that you
will want to include the results. However, when you are running in a
simulation or tutorial mode you will want to rely on the real results
from the current run. You can include a "Results:" section after any
code block. The first code block after this text will be ignored when
running in an interactive mode (such as tutorial or simulation). That
is, in the example below, the `date -u` command will be run
interactively but the `Sat Mar 12 10:09:12 UTC 2016` will only be
included in a static form of the script.

```
date -u
```

Results:

```
Sat Mar 12 10:09:12 UTC 2016
```

### Modifying Test Accuracy

When running a script as a test the outputs of the command are
compared to the result block associated with the code block. By
default a similarity of 66%, meaning at least 66% of the characters
are the same, is considered a pass. However, in some cases this is too
high or too low.

The expected similarity between the command output and the contents of
the result block can be set in the `Results:` header by adding
`Expected similarity: 0.2`, where `0.2` is the similarity desired.

This can be used to ensure things that have low similarity in the results will pass tests, for example, outputing a date will always result in a different date and thus a much lower expected similarity.

The date command will prove this is running in real time.

```
date
```

Results: Expected similarity: 0.3

```
Sat Mar 12 08:59:01 UTC 2016
```

## Defining Next Steps

When running in interactive mode it is possible to provide optional
paths for the user to take next. These appear in a section with the
heading "# Next Steps". Note, for this to work as an interactive set
of options this must be the last section in the document. if it is not
the last section then it will be treated like any other heading.

For example, this document offers next steps options.

# Next Steps

  1. [Configure your scripts through variables](../variables/script.md)
  2. [SimDem Index](../script.md)
  3. [Write multi-part documents](../multipart/script.md)
  4. [Use your documents as interactive tutorials or demos](../running/script.md)

# Multi-Part Demo's

Most tutorials's will consist of at least three parts, preparation,
main body and cleanup. Many will have multiple staged in the main part
of the tutorial. SimDem is able to provide an interactive menu
allowing users to select which part of the tutorial to work through
next. This is achieved by providing a final section with the title `#
Next Steps`. This section should include a list in which each item
provides a link to a markdown document that contain SimDem scripts
that the user may want to work through next.

For example, this file is one part of a multi-part document.

```
cat $SIMDEM_CWD/script.md
```

When executed using SimDem this results in the user being prompted to
select a "next step" (or hit 'q' to quit). If the user selects one of
the scripts it will be executed.

# Prerequisites

It is assumed that you have a basic understanding of the various
SimDem execution [modes](../modes/script.md). You should also ensure
you understand the SimDem [document syntax](../syntax).

# Directory structure

SimDem projects consist of a root directory and one or more
sub-directories. Project directories will contain at least a
`script.md` file that will be used by default when SimDem is run
against the project. Therefore the minimum directory structure for a
simple tutorial is:

`
My_SimDem_Tutorial
└── script.md 
`

# Multi-part tutorials

A more complex project will contain a number of sub-directories
containing tutorials. Tutorial sub-directories will contain at least a
`script.md` file, this is the main file for that tutorial. For example:

`
My_Complex_SimDem_Tutorial
├── script.md 
├── Tutotial_1
│   └── script.md
├── Tutotial_2
│   └── script.md
└── Tutotial_3
    └── script.md
`

## Auto Table of Contents

If the root of the demo scripts directory does not contain a
`script.md` file then SimDem will create a Table of Contents from all
sub-directories that contain a `script.md` file. This ToC will use the
first line (which should be a heading marked with '# ' at the start)
as the text for the link to the script. This ToC will be displayed as
a 'Next Steps' section, thus users will be able to step into any area
of the available demo's.

# Other files

Tutorials may also provide an `env.json` and/or an `env.local.json`
and/or an `env.test.json` file to define environment variables to use
when executing in demo or test mode.

# Demo Scripts example

The directory structure for the SimDem demo scripts is:

```
tree $SIMDEM_CWD/..
```

Results: Expected Similarity: 0.5

```
demo_scripts/
├── env.json
├── env.local.json
├── script.md
├── simdem
│   ├── env.json
│   ├── env.local.json
│   └── script.md
└── test
    ├── env.json
    └── script.md						
```

# Next Steps

  1. [Configure your scripts through variables](../variables/script.md)
  2. [SimDem Index](../script.md)
  3. [Use your documents as interactive tutorials or demos](../running/script.md)
  4. [Use your documents as automated tests](../test/script.md)
  5. [Build a SimDem container](../building/script.md)
  
  

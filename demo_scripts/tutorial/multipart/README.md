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

```bash
cat $SIMDEM_CWD/README.md
```

When executed using SimDem this results in the user being prompted to
select a "next step" (or hit 'q' to quit). If the user selects one of
the scripts it will be executed.


# Directory structure

SimDem projects consist of a root directory and one or more
sub-directories. Project directories will contain at least a
`README.md` file that will be used by default when SimDem is run
against the project. Therefore the minimum directory structure for a
simple tutorial is:

`
My_SimDem_Tutorial
└── README.md 
`

# Multi-part tutorials

A more complex project will contain a number of sub-directories
containing tutorials. Tutorial sub-directories will contain at least a
`README.md` file, this is the main file for that tutorial. For example:

`
My_Complex_SimDem_Tutorial
├── README.md 
├── Tutorial_1
│   └── README.md
├── Tutorial_2
│   └── README.md
└── Tutorial_3
    └── README.md
`

## Auto Table of Contents

If the root of the demo scripts directory does not contain a
`README.md` file then SimDem will create a Table of Contents from all
sub-directories that contain a `README.md` file. This ToC will use the
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

```bash
tree $SIMDEM_CWD/..
```

Results: Expected Similarity: 0.5

```
demo_scripts/
├── env.json
├── env.local.json
├── README.md
├── simdem
│   ├── env.json
│   ├── env.local.json
│   └── README.md
└── test
    ├── env.json
    └── README.md						
```

# Next Steps

  1. [Configure your scripts through variables](../variables/README.md)
  2. [SimDem Index](../README.md)
  3. [Use your documents as automated tests](../test/README.md)
  
  

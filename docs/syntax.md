# Syntax

Currently, there are two implementation of Markdown syntax supported.

## Context Based (default)

This is similar to SimDem v1's syntax.

[Example Context Based Document](../content/complete-features/context.md)

Feature | Implementation 
--- | --- 
Command | \```shell 
Prerequisite | `# Prerequisite` followed by natural language text containing links to local or remote SimDem documents taht that should be executed prior to the main body of the current document. See [Prerequisites](https://github.com/Azure/simdem/tree/master/demo_scripts/simdem/prerequisites) for more details.
Validation | `# Validation` followed by descriptive natural language and code-blocks to be run as tests prior to running the main content in this document. If all tests pass then there is no need to run the main document. See the [validation](https://github.com/Azure/simdem/tree/master/demo_scripts/simdem/prerequisites#validation) section of the prerequisites documentation for more details.
Result | `# Result` followed by a code block with the expected result of the code block immediately before the Results header. See the [testing](https://github.com/Azure/simdem/tree/master/demo_scripts/simdem/test) documentation for more details.


## Codeblock Based (Experimental)

[Example Codeblock Document](../content/complete-features/codeblock.md)

## Features

The only sections processed are code blocks and all features are determined by the code block type.  

Feature |  Implementation
--- | --- 
Command | \```shell
Prerequisite | \```prerequisite
Validation | \```validation
Result | \```result

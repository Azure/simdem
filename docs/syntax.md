# Syntax

Currently, there are two implementation of Markdown syntax supported.

## Context Based (default)

This is similar to SimDem v1's syntax.

[Example Context Based Document](../content/complete-features/context.md)

Feature | Implementation 
--- | --- 
Command | \```shell 
Prerequisite | `# Prerequisite` followed by list of links 
Validation | `# Validation` followed by code block 
Result | `# Result` followed by a code block with the result 


## Codeblock Based

[Example Codeblock Document](../content/complete-features/codeblock.md)

## Features

The only sections processed are code blocks and all features are determined by the code block type.  

Feature |  Implementation
--- | --- 
Command | \```shell
Prerequisite | \```prerequisite
Validation | \```validation
Result | \```result

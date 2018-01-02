# Syntax

Currently, there are two implementation of Markdown syntax supported.

## Context Based

This is similar to SimDem v1's syntax.

[../content/complete-features/context.md](Example Context Based Document)

## Codeblock Based

[../content/complete-features/codeblock.md](Example Codeblock Document)

## Features

The only sections processed are code blocks and all features are determined by the code block type.  

Feature | Context Based | Codeblock Based
--- | --- | ---
Command | \```shell | \```shell
Prerequisite | `# Prerequisite` followed by list of links | \```prerequisite
Validation | `# Validation` followed by code block | \```validation
Result | `# Result` followed by a code block with the result | \```result

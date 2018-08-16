# Syntax

One of the designs of SimDem is to allow multiple implementations of Markdown to support different use cases and documentation patterns.

Currently, there is only one implementation of Markdown syntax supported.

# Context Syntax Specification

This is the syntax for the default codeblock format.  It's design is to allow more natural, expressive, and readable documentation.  It is based off of SimDem v1's syntax.

## SimDem V1 Based (default)

[Example Context Based Document](../examples/simdem1/README.md)

Feature | Implementation 
--- | --- 
Command | \```shell
[Prerequisite](feature_prerequisite.md) | `# Prerequisite` followed by natural language text containing links to local or remote SimDem documents taht that should be executed prior to the main body of the current document. See [Prerequisites](https://github.com/Azure/simdem/tree/master/demo_scripts/simdem/prerequisites) for more details.
[Validation](feature_validation.md) | `# Validation` followed by descriptive natural language and code-blocks to be run as tests prior to running the main content in this document. If all tests pass then there is no need to run the main document. See the [validation](https://github.com/Azure/simdem/tree/master/demo_scripts/simdem/prerequisites#validation) section of the prerequisites documentation for more details.
Result | `# Result` followed by a code block with the expected result of the code block immediately before the Results header. See the [testing](https://github.com/Azure/simdem/tree/master/demo_scripts/simdem/test) documentation for more details.

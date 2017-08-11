# Understanding Prerequisites

There aren't really any pre-requisites for this tutorial / demo, but
this is a convenient place to explain how they work.

# Syntax

The prerequisites section starts with a heading of `# prerequisites`.

The body of this section will contain 0 or more links to a script that
should be run ahead of the current one.

The scripts should appear in the order of required exection in the body.

# Behavior

When a prerequisite script is identified SimDem will ask the user if
they have satisfied the requirement. If SimDem is running in test or
auto mode it is assumed that prerequisites have been satisified.

If the user indicates a prerequisite has been satisfied then execution
moves to the next prerequisite or onto the rest of the script.

If the user indicates a prereqiusite has not been satisfied then the
required script is executed.

# SimDem Test Script

This is a simple test script. It runs a number of commands in
succession. This script also lists commands known not to work.

# Version check

```
echo $SIMDEM_VERSION
```

Results:

```
0.5.0
```

# Directory Check

```
echo $SIMDEM_CWD
```

Results: 

``` Expected_Similarity=0.9 
demo_scripts/test/
```

# Simple Echo

``` 
echo "Hello world" 
```

Results: 

```
Hello world
```

# Code comments

```
# This is a comment and should be ignored
echo "This output should be displayed, the comment before this line should be ignored"
```

Results:

```
This output should be displayed, the comment before this line should be ignored
```

# Expected different results

When we know the results will be different and we want to use them in
tests we need to override the similarity expected by adding
`expected_similarity=x.y` in the start line of the results block:

```
date
```

Results: 

```expected_Similarity=0.2
Tue Jun  6 15:23:53 UTC 2017
```

# For Loop

```
for i in {0..10}; do echo "Welcome $i times"; done
```

Results:

```
Welcome 0 times
Welcome 1 times
Welcome 2 times
Welcome 3 times
Welcome 4 times
Welcome 5 times
Welcome 6 times
Welcome 7 times
Welcome 8 times
Welcome 9 times
Welcome 10 times
```

# Commands that do not work

  * ping bing.com
  * curl bing.com

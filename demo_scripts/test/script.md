This is a simple test script. It runs a number of commands in
succession. This script also lists commands known not to work.

# Simple Echo

```
echo "Hello world"
```

Results: 

```
Hello world
```

# Cat a file

```
cat env.json
```

Results:

```
{
    "TEST": "hello-world"
}
```

# Expected different results

When we know the results will be different and we want to use them in
tests we need to override the similarity expected.

```
date
```

Results: Expected Similarity: 0.2

```
Tue Jun  6 15:23:53 UTC 2017
```

# Sudo

NOTE: there is no sudo in Docker containers, so we need to strip
`sudo` from commands if running in a Docker container. If we are not
in a container we need to run SimDem as `sudo`. This test should pass
in both scenarios.

```
sudo echo "Sudo Works"
```

Results:

```
Sudo Works 
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

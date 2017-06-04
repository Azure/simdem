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

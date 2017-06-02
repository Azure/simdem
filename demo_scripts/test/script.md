This is a simple test script. It runs a number of commands in
succession. This script also lists commands known not to work.

```
echo "Hello world"
```

Results: 

```
Hello world
```

```
date -u
```

Results:

```
Sat Mar 12 10:09:12 UTC 2016
```

```
cat env.json
```

Results:

```
{
    "TEST": "hello-world"
}
```

```
echo $TEST
```

Results:

```
hello-world
```

# Commands that do not work

  * ping bing.com
  * curl bing.com

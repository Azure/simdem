The following will demonstrate a bug in simdem. If there is an indent then the parser will not run the command. 

```
echo "hello world"
```

Results:
```
hello world
```

1. If I run a command which is indented it will skip it

    ```
    echo "Hello world indent"
    ```

Results:
```
Hello world indent
```

Now things will work again
```
echo "that is a weird bug"
```

Results:
```
that is a weird bug
```

Finished Test

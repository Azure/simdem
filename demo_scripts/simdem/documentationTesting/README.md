The following will demonstrate a bug in simdem. If run a command non indented it will run

```bash
echo "hello world"
```

Results:
```expected_similarity=0.8
hello world
```

1. If I run a command which is indented it will skip it

    ```
    echo "Hello world indent"
  
    ```
Results:
```expected_similarity=0.8
Hello world indent
```
Now things will work again

```
echo "that is a weird bug"
```

Results:
```expected_similarity=0.8
that is a weird bug
```
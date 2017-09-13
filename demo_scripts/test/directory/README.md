# Directory Check

In this test ensures that the currrent working directory is set
correctly when a test file is loaded as part of the test_plan.txt
file, see [Issue #70](https://github.com/Azure/simdem/issues/70).

Frst lets check the current working directory, this is useful for
debugging if the test fails.

```
pwd
```

Since we don't know exactly where this will be stored we need to check
that we can open this file in the test.

```
head -n 1 README.md
```

Results: 

``` Expected_Similarity=0.8
# Directory Check
```


This project provides ways to write tutorials that then become
interactive demo's. When running in 'tutorial' mode the user is taken
through the tutorial document one section at a time, but when code
snippets are encountered the user interacts with the application and
the commands are run live.

When run in a 'simulation' mode the application emulates the human
interaction parts of running the demo live so that you can concentrate
on explaining what is happening, while still being able to go
off-script in response to questions and the need for further
exploration.

# Try it Out

It's easier to explain through action, so just run the container and
work through the interactive tutorial that we include.

```
docker run -it rgardler/simdem
```

To run the tutorial as a demo (that is without explanatory text and
with simulated typing) as `--style simulate` to the command:

```
docker run -it rgrdler/simdem --style simulate
```

## Running with your own scripts

To use your own demo script mount a directory with `script.md` into
the simdem container:

```
docker run -it -v ~/my_demo_dir:/demo_scripts rgardler/simdem
```

If you have more than one demo in your demo directory you can tell
SimDem which to run by passing a folder name:

```
docker run -it -v ~/my_demo_dir:/demo_scripts rgardler/simdem run ademo
```

See `demo_scripts/simdem/script.md` for details on how to write a demo
script.


# Learn more

If you want to learn more before running the container then why not read the interactive tutorial as a [markdown page on GitHub](https://github.com/rgardler/simdem/blob/master/demo_scripts/simdem/script.md).

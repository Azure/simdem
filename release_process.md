# Releasig Simdem

This document describes the process for releasing SimDem.

# Ensure we are building master

```
git checkout master
git pull upstream master
git push
```

# Test

```
./script/install.sh
simdem -p demo_scripts/test test
```

# Remove '-dev' from the version number

The '-dev' prefix is used to indicate unreleased version, therefore it
should be removed.

In `config.py` change the line that starts with `SIMDEM_VERSION = `.

# Docker Containers

## Build containers

```
./scripts/build.sh
```

## Publish the containers

```
./scripts/publish.sh
```

# Tag Git

````
git tag -a $SIMDEM_VERSION -m "Build and publish $SIMDEM_VERSION"
git push origin 0.8.1
git push upstream 0.8.1
```

# Bump the version number

Increment the version number as appropriate, adding '-dev' to indicate
this is an unreleased version. In `config.py` change the line that
starts with `SIMDEM_VERSION = `.

## Update version number in tests

In `demo_sctipts/test/README.md` update the expected version number in
the first test.`

# Commit the new version number

```
git add config.py
git add demo_scripts/test/README.md
git commit -m "bump version number"
git push
```

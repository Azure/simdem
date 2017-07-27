#! /bin/sh
# script to run tests on what is to be committed
# Thanks Torek,
# https://stackoverflow.com/questions/20479794/how-do-i-properly-git-stash-pop-in-pre-commit-hooks-to-get-a-clean-working-tree

# First, stash index and work dir, keeping only the
# to-be-committed changes in the working directory.
old_stash=$(git rev-parse -q --verify refs/stash)
git stash save -q --keep-index
new_stash=$(git rev-parse -q --verify refs/stash)

# If there were no changes (e.g., `--amend` or `--allow-empty`)
# then nothing was stashed, and we should skip everything,
# including the tests themselves.  (Presumably the tests passed
# on the previous commit, so there is no need to re-run them.)
if [ "$old_stash" = "$new_stash" ]; then
    echo "pre-commit script: no changes to test"
    sleep 1 # XXX hack, editor may erase message
    exit 0
fi

echo "Running SimDem pre-commit.sh"

STASH_NAME="pre-commit-$(date +%s)"
git stash save -q --keep-index $STASH_NAME

# Test prospective commit
python3 main.py -p demo_scripts/test test
RESULT=$?

# Restore uncommitted Git changes
git reset --hard -q && git stash apply --index -q && git stash drop -q

# Exit with status from test-run: nonzero prevents commit
exit $RESULT



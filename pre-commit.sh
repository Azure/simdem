echo "Running SimDem pre-commit.sh"

STASH_NAME="pre-commit-$(date +%s)"
git stash save -q --keep-index $STASH_NAME

# Test prospective commit
python3 simdem.py -p demo_scripts/test test
RESULT=$?


STASHES=$(git stash list)
if [[ $STASHES == "$STASH_NAME" ]]; then
    git stash pop -q
fi

if [ $RESULT -ne 0 ]; then
    echo "$RESULT"
    exit 1
else
    echo "Tests passed"
    exit 0
fi

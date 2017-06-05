python3 simdem.py test test

read -p "Test in a Docker container? (Y or N)" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    source build.sh
    docker run rgardler/simdem test test
fi


if [ -f /.dockerenv ]; then
    echo "Running in a Docker container"
    IS_DOCKER=true
    INSTALL_DIR=~/bin/
else
    echo "Not running in a Docker container"
    IS_DOCKER=false
    INSTALL_DIR=/usr/local/bin/
fi
FILE=simdem.py
SYMLINK=simdem

if [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
        brew install python3
else
    if [ "$IS_DOCKER" = false ]; then
	# If running in Docker assume python3 is already installed
	sudo apt-get install -y python3-pip
    fi
fi

pip3 install -r requirements.txt

mkdir -p $INSTALL_DIR

if [ "$IS_DOCKER" = true ]; then
    cp $FILE $INSTALL_DIR
    chmod +x $INSTALL_DIR$FILE

    if [ ! -L $INSTALL_DIR$SYMLINK ]; then
	ln -s $INSTALL_DIR$FILE $INSTALL_DIR$SYMLINK
    fi
else
    sudo cp $FILE $INSTALL_DIR
    sudo chmod +x $INSTALL_DIR$FILE

    if [ ! -L $INSTALL_DIR$SYMLINK ]; then
	sudo ln -s $INSTALL_DIR$FILE $INSTALL_DIR$SYMLINK
    fi
fi

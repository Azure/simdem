function removeEarlier() {
# Remove < 0.7.0 version
    if [ -f ~/bin/simdem.py ]; then
	echo "Since version 0.7.0 Simdem is installed in a different way, we need to remove the old Simdem version."
	rm ~/bin/simdem.py
	rm ~/bin/simdem
    fi

    if [ -f /usr/local/bin/simdem.py ]; then
	echo "Since version 0.7.0 Simdem is installed in a different way, we need to remove the old Simdem version."
	sudo rm /usr/local/bin/simdem.py
	sudo rm /usr/local/bin/simdem
    fi

    if [ -f /.dockerenv ]; then
	echo "Running in a Docker container"
	IS_DOCKER=true
	INSTALL_DIR=~/bin/simdem-dev/
    else
	echo "Not running in a Docker container"
	IS_DOCKER=false
	INSTALL_DIR=/usr/local/bin/simdem-dev/
    fi
}

function installLinuxDependencies() {
    if [ "$IS_DOCKER" = true ]; then
	apt update
	apt-get install -y python3-pip
    else
	sudo apt update
	sudo apt-get install -y python3-pip
    fi
}

if [ -f /.dockerenv ]; then
    echo "Running in a Docker container"
    IS_DOCKER=true
    BIN_DIR=~/bin
else
    echo "Not running in a Docker container"
    IS_DOCKER=false
    BIN_DIR=/usr/local/bin
fi

INSTALL_DIR=$BIN_DIR/simdem-dev/
MAIN_FILE=main.py
SYMLINK=simdem

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     installLinuxDependencies;;
    Darwin*)    brew install python3;;
    *)          echo "Unsupported OS: ${unameOut}"
esac

virtualenv simdem-env
source simdem-env/bin/activate

pip3 install -r requirements.txt

if [ "$IS_DOCKER" = true ]; then
    mkdir -p $INSTALL_DIR
    
    cp -r * $INSTALL_DIR
    chmod +x $INSTALL_DIR$MAIN_FILE
    
    echo 'export PATH=$PATH:'$BIN_DIR >> ~/.bashrc

    if [ ! -L $INSTALL_DIR../$SYMLINK ]; then
	ln -s $INSTALL_DIR$MAIN_FILE $INSTALL_DIR../$SYMLINK
    fi
else
    echo "Make install directory at $INSTALL_DIR"
    sudo mkdir -p $INSTALL_DIR

    echo "Copy source into install dir"
    sudo cp -r * $INSTALL_DIR
    echo "Make main file executable"
    sudo chmod +x $INSTALL_DIR$MAIN_FILE

    if [ ! -L $INSTALL_DIR../$SYMLINK ]; then
	echo "Create symlink to main.py file"
	sudo ln -s $INSTALL_DIR$MAIN_FILE $INSTALL_DIR../$SYMLINK
    fi
fi

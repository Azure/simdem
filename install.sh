INSTALL_DIR=/usr/local/bin/
FILE=simdem.py
SYMLINK=simdem

sudo apt-get install -y python3-pip
pip3 install pexpect
pip3 install colorama

sudo cp $FILE $INSTALL_DIR
sudo chmod +x $INSTALL_DIR$FILE

if [ ! -L $INSTALL_DIR$SYMLINK ]; then
    sudo ln -s $INSTALL_DIR$FILE $INSTALL_DIR$SYMLINK
fi

INSTALL_DIR=/usr/local/bin/
FILE=simdem.py
SYMLINK=simdem

if [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
        brew install python3
else
  sudo apt-get install -y python3-pip
fi

pip3 install -r requirements.txt

sudo cp $FILE $INSTALL_DIR
sudo chmod +x $INSTALL_DIR$FILE

if [ ! -L $INSTALL_DIR$SYMLINK ]; then
    sudo ln -s $INSTALL_DIR$FILE $INSTALL_DIR$SYMLINK
fi

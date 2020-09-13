#!/usr/bin/env bash

pip3 install -r requirements.txt
sudo cp ./bgd/__main__.py /usr/bin/bgd
sudo chmod go+rx /usr/bin/bgd
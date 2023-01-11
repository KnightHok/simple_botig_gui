#!/bin/bash

OS="$1";

# get OS from argument
if [ $OS = "windows" ]; then
    venv/Scripts/Activate.ps1;
elif [ $OS = "unix" ]; then
    source venv/bin/activate;
elif [ $OS = "" ]; then
    printf "Please enter in a argument after \"bash install.sh\"\nExample: bash install *"
else
    printf "OS not a option\nPlease type \"windows\" or \"unix\" as a argument\n";
    exit 1;
fi

# install packages
echo "INSTALLING PACKAGES";
pip install -r requirements.txt;

# make installer directory
mkdir ./installer;
cd ./installer;

# make executable
pyinstaller --onefile -w ../smn_bot/main.py;
#!/bin/bash
mkdir -p '.AddOn'
mv ./AddOn/*.dat './.AddOn/'
rmdir AddOn
rm PlayMaxPayne3.exe
ln -s MaxPayne3.exe PlayMaxPayne3.exe
rm install.bat
rm install.sh

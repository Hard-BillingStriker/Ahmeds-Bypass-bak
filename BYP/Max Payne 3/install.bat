@echo off
cd /D "%~dp0"
rmdir /s /q ".AddOn"
ren "AddOn" ".AddOn"
del "PlayMaxPayne3.exe"
mklink "PlayMaxPayne3.exe" "MaxPayne3.exe"
del "install.sh"
del "install.bat"
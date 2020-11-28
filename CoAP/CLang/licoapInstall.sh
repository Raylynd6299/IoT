#!/bin/bash/

echo "Instalando dependencias"
sudo apt-get install autoconf automake libtool -y
sudo apt-get update
sudo apt-get install libssl-dev

echo "Clonando repositorio"
git clone https://github.com/obgm/libcoap.git

echo "Inciamos instalacion"
bash libcoap/autogen.sh
bash libcoap/configure --disable-documentation

make
sudo make install

echo "Creando Variable de entorno"
sudo echo "LD_LIBRARY_PATH='/usr/local/lib'" >> /etc/environment
sudo source /etc/environment

echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"



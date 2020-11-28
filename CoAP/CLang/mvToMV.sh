#!/bin/bash/

IPMV=""
Archivos="licoapInstall.sh"
Password=""
Usuario=""
DireccionDest="~"

sshpass -p $Password scp $Archivos $Usuario@$IPMV:$DireccionDest





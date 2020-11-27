# IoT - Manejo de Pines GPIO con C

Para más informacion click [aqui](http://wiringpi.com)

Para ver un pequeño tutorial [aqui](https://www.electronicwings.com/raspberry-pi/raspberry-pi-gpio-access)

Para Instalar
```Bash 
	sudo apt-get install wiringpi
```
o
```Bash 
	cd /tmp
	wget https://project-downloads.drogon.net/wiringpi-latest.deb
	sudo dpkg -i wiringpi-latest.deb
```
Para comprobar instalacion
```Bash 
	gpio -v
```
Para ver todos los pines del la Raspberry
```Bash 
	gpio readall
```
Para compilar
```Bash 
	gcc Archivo.c -o Archivo -l wiringPi
```

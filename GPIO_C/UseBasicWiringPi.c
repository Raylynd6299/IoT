#include <wiringPi.h>
#include <stdio.h>

int LED = 26;
int main(){
	
	wiringPiSetup();
	pinMode(LED,OUTPUT);
	while(1){
		digitalWrite(LED,HIGH);
		delay(1000);
		digitalWrite(LED,LOW);
		delay(1000);	
	}
	
}

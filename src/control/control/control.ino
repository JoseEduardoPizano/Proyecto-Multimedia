#include <IRremote.h>		// importa libreria IRremote
#include <Wire.h>

#define VAREF 2.7273
#define I2C_SLAVE_ADDR 31

#define boton_Apagar 3125149440
#define boton_Mode 3108437760
#define boton_Clk 3091726080

#define boton_1 3141861120
#define boton_2 3208707840
#define boton_3 3158572800

#define boton_4 4161273600
#define boton_5 3927310080
#define boton_6 4127850240

#define boton_Loud 3910598400
#define boton_Arriba 3860463360
#define boton_Eq 4061003520

#define boton_Izquierda 4077715200
#define boton_Enter 3877175040
#define boton_Derecha 2707357440

#define boton_Aps 4144561920
#define boton_Abajo 3810328320
#define boton_Band 2774204160

int SENSOR = 11;    		// sensor KY-022 a pin digital 11  
float boton = 0;

// Prototypes
void i2c_received_handler(int count);
void i2c_request_handler(int count);

 
void setup() { 
  //______________________________
    // Configure ADC to use voltage reference from AREF pin (external)
    analogReference(EXTERNAL);
    // Set ADC resolution to 10 bits
    // analogReadResolution(10);

  // Configure I2C to run in slave mode with the defined address
    Wire.begin(I2C_SLAVE_ADDR);
    // Configure the handler for received I2C data
    Wire.onReceive(i2c_received_handler);
    // Configure the handler for request of data via I2C
    Wire.onRequest(i2c_request_handler);


  Serial.begin(9600);     				// inicializa comunicacion serie a 9600 bps
  IrReceiver.begin(SENSOR, DISABLE_LED_FEEDBACK);    	// inicializa recepcion de datos
} 

void i2c_request_handler(){
	Wire.write((byte*) &boton, sizeof(float));
}

void i2c_received_handler(int count){
	char received = 0;
	while (Wire.available()){
		received = (char)Wire.read();
		digitalWrite(13, received ? HIGH : LOW);
		Serial.println(received);
	}

}


void loop() { 
  if (IrReceiver.decode()) {   				// si existen datos ya decodificados
    Serial.println(IrReceiver.decodedIRData.decodedRawData);  // imprime valor en hexadecimal en monitor

  switch (IrReceiver.decodedIRData.decodedRawData)
    {
      case boton_Apagar:      boton = 1.0; Serial.println("Apagar");  break;
      case boton_Mode:        boton = 2.0; Serial.println("Mode"); break; 
      case boton_Clk:         boton = 3.0; Serial.println("Clk"); break;

      case boton_1:           boton = 4.0; Serial.println("1"); break;
      case boton_2:           boton = 5.0; Serial.println("2"); break;
      case boton_3:           boton = 6.0; Serial.println("3"); break;

      case boton_4:           boton = 7.0; Serial.println("4"); break;
      case boton_5:           boton = 8.0; Serial.println("5"); break;
      case boton_6:           boton = 9.0; Serial.println("6"); break;

      case boton_Loud:        boton = 10.0; Serial.println("Load"); break;
      case boton_Arriba:      boton = 11.0; Serial.println("Arribs"); break;
      case boton_Eq:          boton = 12.0; Serial.println("Eq"); break;

      case boton_Izquierda:   boton = 13.0; Serial.println("Izquierda"); break;
      case boton_Enter:       boton = 14.0; Serial.println("Enter"); break;
      case boton_Derecha:     boton = 15.0; Serial.println("Derecha"); break;

      case boton_Aps:         boton = 16.0; Serial.println("Aps"); break;
      case boton_Abajo:       boton = 17.0; Serial.println("Abajo"); break;
      case boton_Band:        boton = 18.0; Serial.println("Band"); break;
      default:                boton = 19.0; Serial.println("Boton no reconocido"); break;
  }

    IrReceiver.resume();      				// resume la adquisicion de datos
  }
  delay (100);        					// breve demora de 100 ms.
  boton = 19.0;
}
#include <Keyboard.h>
#include <SD.h>

const String PAYLOAD_FILE = "test.txt";

const byte DELAY_CMD = 0xE0;
const byte PRINT_CMD = 0xE1;
const byte PRESS_CMD = 0xE2;
const byte RELEASE_CMD = 0xE3;
const byte WRITE_CMD =	0xE4;
const byte PRINT_FILE_CMD = 0xE5;

const int STRING_BUFFER_SIZE = 256;
char string_buffer[STRING_BUFFER_SIZE];

int read_next_int(File f){
  f.readBytes(string_buffer, 4);
  
  return int((unsigned char)(string_buffer[0]) << 24 |
             (unsigned char)(string_buffer[1]) << 16 |
             (unsigned char)(string_buffer[2]) << 8 |
             (unsigned char)(string_buffer[3]));
}

void read_bytes_to_buffer(File f, int length){
    f.readBytes(string_buffer, length);
    string_buffer[length] = 0; // Null terminater
}

void decode_press(File hex_file){
  byte control_key = hex_file.read();
  Serial.print("PRESS ");
  Serial.println(control_key, HEX);
  //Keyboard.press(control_key);
}

void decode_delay(File hex_file){
  int delay_time = read_next_int(hex_file);
  Serial.print("DELAY "); 
  Serial.println(delay_time); 
  //delay(delay_time);
}

void decode_release(File hex_file){
  Serial.println("RELEASE ");
  //Keyboard.releaseAll();
}

void decode_write(File hex_file){
  byte write_byte = hex_file.read();
  Serial.println("WRITE "+write_byte);
  //Keyboard.write(write_byte);
}

void decode_print(File hex_file){
  int string_length = read_next_int(hex_file);
  
  if(string_length < STRING_BUFFER_SIZE){	
	read_bytes_to_buffer(hex_file, string_length);

    Serial.print("PRINT ");
    Serial.println(string_buffer);
    //Keyboard.print(string_buffer);
  }
}

void decode_print_file(File hex_file){
  int name_length = read_next_int(hex_file);
  
  if(name_length < STRING_BUFFER_SIZE){
	read_bytes_to_buffer(hex_file, name_length);

    File ext_data = SD.open(string_buffer);
    
    while(ext_data.available()){
      int data_length = min(ext_data.available(), STRING_BUFFER_SIZE-1);
	  read_bytes_to_buffer(ext_data, data_length);
      
      Serial.print("PRINT_FILE ");
      Serial.println(string_buffer);
      //Keyboard.print(string_buffer);
    }
  }
}

void setup() {
  Serial.begin(9600);
  //Serial.println(Keyboard.begin(4) ? "Keyboard Initialized" : "Keyboard Failed Initialization");
  Serial.println(SD.begin(4) ? "SD Initialized" : "SD Failed Initialization");
  
  File hex_file = SD.open(PAYLOAD_FILE, FILE_READ);

  while(hex_file.available())
  {
    byte command = hex_file.read();

    if(command==PRESS_CMD)
      decode_press(hex_file);
    if(command==DELAY_CMD)
      decode_delay(hex_file);
    if(command==RELEASE_CMD)
      decode_release(hex_file);
    if(command==WRITE_CMD)
      decode_write(hex_file);
    if(command==PRINT_CMD)
      decode_print(hex_file);  
    if(command==PRINT_FILE_CMD)
      decode_print_file(hex_file);  
  }
}

void loop() {
  // put your main code here, to run repeatedly:
}

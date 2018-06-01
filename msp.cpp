#define TEMPSENSOR 0
int sensor_pin = TEMPSENSOR;
long int sensor_value;
String input = "";
bool input_complete;

void setup() {
    //Called at start
    Serial.begin(9600);
    //Set voltage reference (1.5V)
    analogReference(INTERNAL1V5);
    //Reserve a certain number of bytes for the string
    input.reserve(20);
    //Input is not complete
    input_complete = false;
}

void loop() {
    //Repeatedly called after setup
    if (input_complete) {
        if (input == "getq")
        {
            sensor_value = analogRead(sensor_pin);
            char array[4];
            itoa(sensor_value, array, 10);
            //Padding
            int i = 0;
            while(i < 4 && array[i] != '\0')
            {
                i++;
            }
            while(i < 4) {
                Serial.print('0');
                i++;
            }
            //Value
            i = 0;
            while(i < 4 && array[i] != '\0')
            {
                Serial.print(array[i]);
                i++;
            }
            input = "";
            input_complete = false;
        }
    }
}

void serialEvent() {
    //Called when the serial gets an event
    //Interrupt based
    if (input_complete)
    {
        return;
    }
    while (Serial.available()) {
        char in = (char) Serial.read();
        input += in;
        if (in == 'q')
        {
            input_complete = true;
        }
    }
}

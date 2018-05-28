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
            int iterator = 0;
            while(iterator < 4 && array[iterator] != '\0')
            {
                Serial.print(array[iterator]);
                iterator++;
            }
            input = "";
            input_complete = false;
        }
    }
    sensor_value = analogRead(sensor_pin);
    char array2[4];
    itoa(sensor_value, array2, 10);
    int iteratore = 0;
    while(iteratore < 4 && array2[iteratore] != '\0')
    {
        Serial.print(array2[iteratore]);
        iteratore++;
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

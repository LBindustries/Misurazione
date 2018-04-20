#define TEMPSENSOR 0

int sensor_pin = TEMPSENSOR;
long int sensor_value;
string input;
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
        if (input == "get\n")
        {
            sensor_value = analogRead(sensor_pin);
            Serial.print(sensor_value);
        }
        input = "";
        input_complete = false;
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
        if (in == '\n')
        {
            input_complete = true;
        }
    }
}
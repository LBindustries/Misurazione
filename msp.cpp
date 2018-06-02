int sensor_pin = TEMPSENSOR;
long int sensor_value;
String in_string = "";
char out_chr_array[4];
char* makes_no_sense;

void setup() {
    //Called at start
    Serial.begin(9600);
    //Set voltage reference (1.5V)
    analogReference(INTERNAL1V5);
    //Reserve a certain number of bytes for the string
    in_string.reserve(20);
}

void answerPoll() {
    if (in_string == "get\n")
    {
        sensor_value = analogRead(sensor_pin);
        makes_no_sense = itoa(sensor_value, out_chr_array, 10);
        //Padding
        int i = 0;
        while(i < 4 && makes_no_sense[i] != '\0')
        {
            i++;
        }
        while(i < 4) {
            Serial.print('0');
            i++;
        }
        //Value
        i = 0;
        while(i < 4 && makes_no_sense[i] != '\0')
        {
            Serial.print(makes_no_sense[i]);
            i++;
        }
    }
}

void loop() {
    //loops are for cowards
}

void serialEvent() {
    //Called when the serial gets an event
    //Interrupt based
    while (Serial.available()) {
        char in = (char) Serial.read();
        if (in == '\n')
        {
            answerPoll()
            in_string = ""
        }
        else {
            in_string += in;
        }
    }
}

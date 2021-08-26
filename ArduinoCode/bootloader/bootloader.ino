#define MAX_LENGTH 100;
// enum pinType {
//   A,
//   D
// };
/*
 * 
 */
int baudrate = 115200;
const int analogPins[] = {A0,A1,A2,A3,A4,A5};


void setup(){
    Serial.begin(baudrate);
}

void init()
{
    Serial.begin(baudrate);
    char command[ MAX_LENGTH ];
    readline(command);
}

/*

*/
void loop(){

}

/*
Command String for blink goes like
blink:pin:interval:duration -- it will digitalWrite to pin at specified intervals
<!---- With additional advances I can add variable intervals for on and off ----!>
*/

void blink(char *command,size_t len)
{

    int count = 0;
    int interval = 0;
    int pin = 0;
    int duration = 0;
    char separator[] = ":";
    char *token;
    token = strtok(command,separator);
    while(token != NULL)
    {
         if(count == 1) pin = atoi(token);
         if(count == 2) interval = atoi(token);
         if(count == 3) duration = atoi(token);
        token = strtok(NULL,separator);
        count++;
    }

    int start = miilis();
    while(millis()-start >= duration)
    {
        digitalWrite(pin, HIGH);
        delay(interval);
        digitalWrite(pin, LOW);
        delay(interval);
    }

}

/*
    Interrupt
    
*/
//void InterruptAttach(int pin,int conditon)
//{
//    attachInterrupt(digitalPinToInterrupt(pin), function, mode);
//}

char *readline(char str[MAX_LENGTH])
{
    int count = 0;
    //char str[MAX_LENGTH];
    while(Serial.available())
    {
        char c = Serial.read();
        if(c != '\n' || count <= MAX_LENGTH)
        {
            str[count++] =  c;
        } else {
            break;
        }
    }
}


void writePin(int pin,char *pinType,int pinValue)
{
    pinMode(pin, OUTPUT);
    delay(50);
    (pinType == "A") ? analogWrite(pin, pinValue) : digitalWrite(pin, pinValue);
    Serial.println("OK");
    
}

void readPin(int pin,char *pinType)
{
  pinMode(pin, INPUT);
  delay(50);
  int value = (pinType == "D") ? digitalRead(pin) : analogRead(analogPins[pin]);
  Serial.print("[*] Pin Value: ");
  Serial.println(value);
}

const int trigPinLeft = 7;
const int echoPinLeft = 8;
const int trigPinFront = 9;
const int echoPinFront = 10;
const int trigPinRight = 6;
const int echoPinRight = 5;

// Variables to store the current direction and movement steps
char direction = 'N'; // N = North, S = South, E = East, W = West
int step = 0;

void setup() {
  Serial.begin(9600);

  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  pinMode(trigPinFront, OUTPUT);
  pinMode(echoPinFront, INPUT);
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);
}

long readUltrasonicDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  long distance = duration / 58.2; // Convert the time into distance in cm
  return distance;
}

void loop() {
  long distanceLeft = readUltrasonicDistance(trigPinLeft, echoPinLeft);
  delay(100); // Small delay to avoid interference
  long distanceFront = readUltrasonicDistance(trigPinFront, echoPinFront);
  delay(100); // Small delay to avoid interference
  long distanceRight = readUltrasonicDistance(trigPinRight, echoPinRight);

  // Simulate movement and direction (update this part with real data from RC car controls)
  // Example of updating direction and steps
  // Here we are simulating: step increases every loop, direction changes every 10 steps
  step++;
  if (step % 10 == 0) {
    if (direction == 'N') direction = 'E';
    else if (direction == 'E') direction = 'S';
    else if (direction == 'S') direction = 'W';
    else if (direction == 'W') direction = 'N';
  }

  Serial.print(distanceLeft);
  Serial.print(",");
  Serial.print(distanceFront);
  Serial.print(",");
  Serial.print(distanceRight);
  Serial.print(",");
  Serial.print(direction);
  Serial.print(",");
  Serial.println(step);

  delay(100); // Delay between readings
}

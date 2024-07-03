class Stepper{ 

public: 

Stepper(int dir_pin, int step_pin); 

void step(boolean dir); 

void multiple_steps(int steps, boolean dir); 

void update_pos(boolean dir); 

void set_pos(int new_pos); 

int get_pos();

bool in_movement();

void set_speed(int new_speed); 

void move_to(int pos); 

void set_target_position(int target_position); 

void run(); 

void move(int pos); 

void run_to(); 

int get_target_pos(); 

private: 

int _target_position; 

int _dir_pin; 

int _step_pin; 

int _pos; 

int _speed; 

}; 

Stepper::Stepper(int dir_pin, int step_pin){ 

_dir_pin = dir_pin; 

_step_pin = step_pin; 

_pos = 0; 

_speed = 1; 
pinMode(_dir_pin, OUTPUT);
pinMode(_step_pin, OUTPUT);
pinMode(8, OUTPUT);
digitalWrite(8, LOW);

} 



void Stepper::step(boolean dir){ 
Serial.write(dir);
if (dir){
  digitalWrite(_dir_pin, LOW);
}
else{
  digitalWrite(_dir_pin, HIGH);
}

digitalWrite(_step_pin, HIGH); 

delay(1); 

digitalWrite(_step_pin, LOW); 

update_pos(dir); 

} 

 

void Stepper::multiple_steps(int steps, boolean dir){ 

for(int i = 0; i < steps; i++){ 

step(dir);	 

} 

} 

 

void Stepper::set_target_position(int target_position){ 

_target_position = target_position; 

} 

 

void Stepper::update_pos(boolean dir){ 

if (dir){ 

_pos ++; 

} 

else{ 

_pos --; 

} 

} 

int Stepper::get_pos(){ 

return _pos; 

} 

 

void Stepper::set_pos(int new_pos){ 

_pos = new_pos; 

} 

 

void Stepper::set_speed(int new_speed){ 

_speed = new_speed; 

} 

 

void Stepper::move_to(int pos){ 

_target_position = pos; 

}	 

 

void Stepper::run(){ 

if (_pos < _target_position){ 

step(true); 

} 

else if ( _pos > _target_position){ 

step(false); 

} 

} 

 

void Stepper::move(int pos){ 

_target_position += pos; 

} 

 

void Stepper::run_to(){ 

while(get_pos() != get_target_pos()){ 

run(); 

} 

} 

 

int Stepper::get_target_pos(){ 

return _target_position; 

} 
bool Stepper::in_movement(){
  if (_pos == _target_position){
    return false;
  }
  return true;
}

 

Stepper stepper2 = Stepper(5, 2); 
Stepper stepper1 = Stepper(6, 3);
Stepper stepper3 = Stepper(7, 4);
void setup() {
  delay(5000);
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);
  //digitalWrite(5, HIGH);
  //digitalWrite(2, HIGH);
  
}

void loop() {
  stepper1.move_to(300); // Die Zahl ändern, falls es nicht weit genug oder zu weit fährt, war mir nicht mehr sicher
  stepper2.move_to(-300);
  stepper3.move_to(300);
  while(stepper1.in_movement()){
    stepper1.run();
    stepper2.run();
    stepper3.run();
    
  }
  delay(5000);
  stepper1.move_to(-300); // Die Zahl ändern, falls es nicht weit genug oder zu weit fährt, war mir nicht mehr sicher
  stepper2.move_to(300);
  stepper3.move_to(-300);
  while(stepper1.in_movement()){
    stepper2.run();
    stepper1.run();
    stepper3.run();
  }
  delay(5000);
}

float circle_diameter = 700;
float cutter_diameter = 16.35;
float tab_width = 16.35;
float off_set = (circle_diameter  - cutter_diameter) / 2.0;
float gap_radians = (cutter_diameter + tab_width) / off_set;
int circ = (int)(1.1 * circle_diameter);

void setup() {
  size(circ, circ);
  background(255);
}

void draw() {
  translate(circ / 2, circ / 2);
  scale(1, -1);

//  grid lines
  stroke(180);
  line(-circle_diameter, 0, circle_diameter, 0);
  line(0, -circle_diameter, 0, circle_diameter);
  
//  point(-100,0);
  noFill();
  noSmooth();
  // desired path
  arc(0, 0, circle_diameter, circle_diameter, 0, TWO_PI);

  stroke(0);
//  fill(0);

  // first incremental G0 move
  float x = -off_set;
  float y = 0;
  // arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
  
  // move to end of first tab, also G0
  x = x + ((1 - cos(gap_radians)) * off_set);
  y = y + (sin(gap_radians) * off_set);
  arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
  
  // move to start of second tab, #1 cut with G2
  stroke(255,0,0);
  fill(255,0,0);
  // draws a line from current point to arc center (by offset)
  float i = x + (cos(gap_radians) * off_set);
  float j = y - (sin(gap_radians) * off_set);
  line(x, y, i, j);
  x = x + ((cos(gap_radians) + cos(PI / 3.0)) * off_set);
  y = y + ((- sin(gap_radians) + sin(TWO_PI / 3.0)) * off_set);
  // draws the location of the ending point (by offset)
  arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
  
  // move to end of second tab, #2 non-cut with G2
  stroke(0,255,0);
  fill(0,255,0);
  i = x + (- cos(PI / 3.0) * off_set);
  j = y - (sin(PI / 3.0) * off_set);
  line(x, y, i, j);
  x = x + ((cos((PI / 3.0) - gap_radians) - cos(PI / 3.0))* off_set);
  y = y + ((sin((PI / 3.0) - gap_radians) - sin(PI / 3.0))* off_set);
  arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
  
  // move to start of third tab, #3 cut with G2
  stroke(0,0,255);
  fill(0,0,255);
  i = x + (- cos((PI / 3.0) - gap_radians) * off_set);
  j = y - (sin((PI / 3.0) - gap_radians) * off_set);
  line(x, y, i, j);
  x = x;
  y = y - 2 * ((sin((PI / 3.0) - gap_radians))* off_set);
  arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
  
  // move to end third tab, #4 non-cut with G2
  stroke(255,0,0);
  fill(255,0,0);
  i = x - (cos((PI / 3.0) - gap_radians) * off_set);
  j = y + (sin((PI / 3.0) - gap_radians) * off_set);
  line(x, y, i, j);
  x = x - ((cos((PI / 3.0) - gap_radians) - cos(PI / 3.0))* off_set);
  y = y + ((sin((PI / 3.0) - gap_radians) - sin(PI / 3.0))* off_set);
  arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
  
  // move to start first tab, #5 cut with G2
  stroke(0,255,0);
  fill(0,255,0);
  i = x - (cos(PI / 3.0) * off_set);
  j = y + (sin(PI / 3.0) * off_set);
  line(x, y, i, j);
  x = x - ((1 + cos(PI / 3.0)) * off_set);
  y = y + (sin(PI / 3.0) * off_set);
  arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
  
}

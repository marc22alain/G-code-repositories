float HCD = 350;
float num_holes = 6.0;
float radians_increment = TWO_PI / num_holes;
float cutter_diameter = 6.35;
float x = 0;
float y = 0;


int circ = (int)(1.2 * HCD);

void setup() {
  size(circ, circ);
  background(255);
}

void draw() {
  translate(circ / 2, circ / 2);
  scale(1, -1);

//  grid lines
  stroke(180);
  line(-HCD, 0, HCD, 0);
  line(0, -HCD, 0, HCD);
  stroke(255,0,0);
  fill(255,0,0);
  // initial hole
  x = cos(0) * HCD / 2;
  y = sin(0) * HCD / 2;
  arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
  int i;
  for (i = 1; i < num_holes; i++) {
    x = x - (cos((i - 1) * radians_increment) * HCD / 2) + (cos(i * radians_increment) * HCD / 2);
    y = y - (sin((i - 1) * radians_increment) * HCD / 2) + (sin(i * radians_increment) * HCD / 2);
    arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
    println(x,y);
  }
  
  // returning to origin
  stroke(0,255,0);
  fill(0,255,0);
  x = x - (cos((num_holes - 1) * radians_increment) * HCD / 2);
  y = y - (sin((num_holes - 1) * radians_increment) * HCD / 2);
  arc(x, y, cutter_diameter, cutter_diameter, 0, TWO_PI);
}

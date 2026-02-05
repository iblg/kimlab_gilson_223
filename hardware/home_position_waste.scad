///////////////////////////////////////////////////////////////
// MAIN MODULE
///////////////////////////////////////////////////////////////
color([1,0,0]){
    liquid_cone();
    hole_for_adapter();
}

color([1,1,0]){
inst();
bar();
}
///////////////////////////////////////////////////////////////
// PARAMS
// ALL UNITS IN MM
///////////////////////////////////////////////////////////////
$fn = 100;
wall_width = 2;
gap_y = 16.6; // gap in y between bar and instrument

bar_z_offset = 6.6; // the height of the instrument wall with respect to the top of the bar


bar_hole_diam = 7.05;

bar_x = 100; // arbitrarily large
bar_y = 12.4;
bar_z = 12.4;

inst_x = bar_x;
inst_y = 1.6;
inst_z = 100; //arbitrary height


outlet_hole_diam = 6.3;
outlet_hole_height = 9;

clearance_above_bar = 4.6;
epsilon = 0.2; // extra length so renders differences visibly
bar_hole_x = 20;


cone_top_diam = gap_y - 3*wall_width;
cone_bottom_diam = outlet_hole_diam;
cone_height = 2*bar_z;
///////////////////////////////////////////////////////////////
// SUB MODULES
///////////////////////////////////////////////////////////////

module liquid_cone(){
    cylinder(d2 = cone_top_diam, d1 = cone_bottom_diam, h=cone_height);
}

module hole_for_adapter(){
    translate([0,0, -outlet_hole_height + epsilon]){
    cylinder(d = outlet_hole_diam, h=outlet_hole_height);
    }
}

module bar_hole(){
    translate([bar_hole_x, bar_y/2, -epsilon])
    cylinder(d=bar_hole_diam, h=bar_z + 2*epsilon);
}

module bar(){
    
    translate([0,gap_y, -bar_z]){
    difference(){
    cube([bar_x, bar_y, bar_z]);
    bar_hole();
    }
}
}


module inst(){
    translate([0,-inst_y,-inst_z]){ // offset to origin
    translate([0, 0, bar_z_offset]){ // offset so that inst wall is above
    cube([inst_x, inst_y, inst_z]);
}}}
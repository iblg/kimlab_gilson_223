///////////////////////////////////////////////////////////////
// MAIN MODULE
///////////////////////////////////////////////////////////////
color([1,0,0]){
//    liquid_cone();
    drain();
   
}
color([0,0,1]){
    top_cube();
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
wall_width = 1;
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

catchment_x = gap_y - epsilon;
catchment_y = gap_y + bar_y;
catchment_z = clearance_above_bar - 2;

cone_top_diam = gap_y - 3*wall_width;
cone_bottom_diam = outlet_hole_diam;
cone_height = 2*bar_z;
///////////////////////////////////////////////////////////////
// SUB MODULES
///////////////////////////////////////////////////////////////

module hook() {
//    cube([catchment_x, 2*wall_width, bar_z_offset+2*wall_width]);
    difference(){
    translate([0,-2*wall_width-inst_y,0])
      cube([catchment_x, 4*wall_width+inst_y, bar_z_offset+2*wall_width]);
        scale([1,1.05,1])
      inst();
    }

}
module top_cube(){
    union(){
    translate([bar_hole_x - catchment_x/2, 0, 0]){
    hook();
    cube([catchment_x, catchment_y, catchment_z]);
    }
    translate([bar_hole_x, gap_y + bar_y/2, -bar_z + epsilon]) bar_hole_plug();
    }
}
module bar_hole_plug(){
    scale([0.95, 0.95, 1]) cylinder(d=bar_hole_diam, h=bar_z + 2*epsilon);
;
}
module drain() {
    difference(){
        translate([0,0,-outlet_hole_height])
        cylinder(h=cone_height + outlet_hole_height-3*epsilon, d2=cone_top_diam*1.1, d1=cone_top_diam);
        translate([0,0,-2*epsilon])
        liquid_cone();
        hole_for_adapter();
    }
    
}
module liquid_cone(){
    cylinder(d2 = cone_top_diam, d1 = cone_bottom_diam, h=cone_height);
    hole_for_adapter();

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
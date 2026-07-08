bar_x = 16 + 8;
bar_y = 12.86 + 0.5;
bar_z = 3.28 + 0.5;
d_1428 = 5.271;
hole_x_translation=3.12 + d_1428/2;
K=0.01;
$fn=60;

wall_thickness = 1;
guide_x = bar_x;
guide_y = bar_y + 2*wall_thickness; 
guide_z = bar_z + 2*wall_thickness;

x_between_wells = 19.5;
needle_diameter = 3;
module needle_guide(){
        cube([guide_x, guide_y, guide_z]);

}

hole_translation = [hole_x_translation, guide_y/2, 0];
module bar(){
    difference(){
        union(){
            translate([-3*x_between_wells, 0,0]) cube([3*x_between_wells, guide_y, guide_z]);
            difference(){
                translate([-1,K,K]) needle_guide();
                translate([0, wall_thickness, wall_thickness]) cube([bar_x, bar_y, bar_z]);
                translate(hole_translation) hole_1428();
                }
            }
            holes_for_needles();

        }
    }
module hole_for_needle(){
        
                rotate([0,0,0]){
                    translate(hole_translation) translate([0,0, -guide_z/2]) cylinder(h=2*guide_z, d=needle_diameter);
                    }
   
    }

module holes_for_needles(){
    for(i=[0:3]){
//        echo(i*x_between_wells)
        translate([-i*x_between_wells,0,0]) {
            hole_for_needle();
            }
            
        }
}

module hole_1428(){
    cylinder(d=d_1428, h = 5*bar_z);
}

bar(); 
//color([1,1,0,0.5]) needle_guide();
//holes_for_needles();
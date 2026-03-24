
$fn=60; //set the number of facets to 60

attachment_x = 11.8; // nominally about 12 mm. In practice a little smaller is needed.
attachment_y = 4;
attachment_z = 52;

attachment_hole_length = 5*attachment_y;

x_between_wells = 19.5;

thumbscrew_diameter = 3.7;
epsilon = 0.01; 

module attachment_module(){
    difference(){
        cube([attachment_x, attachment_y, attachment_z]);
        translate([attachment_x/2,attachment_hole_length*0.7,attachment_z-12]){
            hole_for_thumbscrew();
        }
    }
}
    
module hole_for_thumbscrew(){
    rotate([90,0,0]){
        cylinder(h=attachment_hole_length, d=thumbscrew_diameter);
        }
    }


holder_x = 4*x_between_wells;
holder_y = 13;
holder_z = 15;


module needle_holder_body(){    
    translate([0,attachment_y, 0]){
        color([0,0,1]){
            cube([holder_x, holder_y, holder_z]);
        }
    }
}

module hole_for_needle(height=2*holder_z, needle_diameter = 2){
        
    translate([11.4,attachment_y + holder_y/2,-height+epsilon+holder_z]){
//        color([0,1,0]){
                rotate([0,0,0]){
                    cylinder(h=height, d=needle_diameter);
                    }
//                }
        }
    }

module holes_for_needles(){
    for(i=[0:3]){
//        echo(i*x_between_wells)
        translate([i*x_between_wells,0,0]) {
            hole_for_needle();
            }
            
        }
}

module thumbscrews_for_needles(){
    translate([11.4,attachment_hole_length + attachment_y + 1,holder_z/2]){
    for(i=[0:3]){
        translate([i*x_between_wells,0,0]) {
            hole_for_thumbscrew();
            }    
            }
        }
    }

module needle_holder(){
   
    difference(){
//        holes_for_needles();
        union(){
            needle_holder_body();
            guide_for_needles();

        }
        holes_for_needles();

        thumbscrews_for_needles();
        }
    }

module guide_for_needles(){
      for(i=[0:3]){
          height = 110;
//        echo(i*x_between_wells)
        translate([i*x_between_wells,0,0]) {
            difference(){
                hole_for_needle(height = height, needle_diameter=6);
               
                translate([0,0,epsilon])
                hole_for_needle(height= 1.01 * height + epsilon, needle_diameter=1.5);
            }
        }
            
        }
}

union(){
    attachment_module();
    needle_holder();
//    thumbscrews_for_needles();

}
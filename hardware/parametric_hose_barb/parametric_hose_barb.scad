// ============================================================
// Parametric Hose Barb
// ============================================================
// All measurements are in millimeters

// --- Main Parameters ---
barb_count        = 2;      // Number of barb rings
hose_id           = 10;      // Inner diameter of the hose (mm)
wall_thickness    = 1.8;    // Wall thickness of the barb tube
barb_height       = 1.5;    // How tall/sharp each barb protrusion is
barb_spacing      = 6;      // Distance between barb rings (center to center)
barb_angle        = 30;     // Angle of the barb taper (degrees, lower = sharper)
body_length_extra = 5;      // Extra straight tube length beyond last barb

// --- Fitting End Parameters (e.g., NPT or push-fit stub) ---
fitting_od        = 14;     // Outer diameter of the fitting end
fitting_length    = 12;     // Length of the fitting end
fitting_thread    = false;  // Set to true to add a simple thread placeholder

// --- Thread Parameters (used only if fitting_thread = true) ---
thread_pitch      = 1.5;    // Thread pitch in mm
thread_depth      = 0.8;    // Depth of thread grooves

// --- General ---
$fn               = 64;     // Smoothness of circles
taper_lead_in     = 3;      // Length of tapered lead-in tip at barb end

// ============================================================
// Derived Values
// ============================================================
barb_od       = hose_id + (wall_thickness * 2);           // Outer diameter of tube
total_barb_len = (barb_count * barb_spacing) + body_length_extra;

// ============================================================
// Module: Single Barb Ring
// ============================================================
module barb_ring(tube_od, barb_h, b_angle) {
    barb_tip_r  = (tube_od / 2) + barb_h;
    barb_base_r = tube_od / 2;
    barb_width  = barb_h / tan(b_angle);

    rotate_extrude(angle = 360) {
        polygon(points = [
            [barb_base_r, 0],
            [barb_tip_r,  barb_width],
            [barb_base_r, barb_width * 2.5],
            [barb_base_r, 0]
        ]);
    }
}

// ============================================================
// Module: Barb Tube Section
// ============================================================
module barb_tube() {
    union() {
        // Main tube body
        cylinder(h = total_barb_len, d = barb_od);

        // Barb rings
        translate([0,0,-5])
        for (i = [0 : barb_count - 1]) {
            translate([0, 0, taper_lead_in + (i * barb_spacing)])
                barb_ring(barb_od, barb_height, barb_angle);
        }

        // Tapered lead-in tip
        cylinder(h = taper_lead_in, d1 = barb_od * 0.6, d2 = barb_od);
    }
}

// ============================================================
// Module: Fitting End
// ============================================================
module fitting_end() {
    difference() {
        cylinder(h = fitting_length, d = fitting_od);

        // Thread grooves (simple visual representation)
        if (fitting_thread) {
            for (i = [0 : floor(fitting_length / thread_pitch)]) {
                translate([0, 0, i * thread_pitch])
                    rotate_extrude(angle = 360)
                        translate([(fitting_od / 2) - thread_depth, 0, 0])
                            circle(r = thread_depth * 0.7);
            }
        }
    }
}

// ============================================================
// Module: Hex Collar / Flange (optional grip feature)
// ============================================================
hex_collar       = true;    // Set to false to disable
hex_collar_size  = fitting_od * 1.3;  // Across-flats size
hex_collar_h     = 4;

module hex_collar() {
    if (hex_collar) {
        cylinder(h = hex_collar_h, d = hex_collar_size, $fn = 6);
    }
}

// ============================================================
// Final Assembly
// ============================================================
module hose_barb() {
    difference() {
        union() {
            // Barb end (tip points down at Z=0)
            barb_tube();

            // Hex collar sits on top of barb tube
            translate([0, 0, total_barb_len])
                hex_collar();

            // Fitting end on top of collar
            translate([0, 0, total_barb_len + (hex_collar ? hex_collar_h : 0)])
                fitting_end();
        }

        // Hollow through-bore
        total_height = total_barb_len + (hex_collar ? hex_collar_h : 0) + fitting_length;
        translate([0, 0, -0.1])
            cylinder(
                h = total_height + 0.2,
                d = hose_id
            );
    }
}

// ============================================================
// Render
// ============================================================
hose_barb();
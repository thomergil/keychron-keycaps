// Keycap for the Keychron K3 Ultra 8K (MX-stem low-profile switch), any width in u.
// Models the LSA outline: rounded rectangle, straight walls tapering from skirt to top,
// a top that slopes down toward the back, and a shallow spherical dish
// (dish_depth = 0 for a flat top). The stem extends below the skirt by stem_drop.
// Defaults are estimates. Measure a stock cap with calipers and override.
//
// Export one part:
//   openscad -D 'part="cap"' -D 'legend="U"' -D 'homing="dot"' -o u.stl keycap.scad
//   openscad -D 'part="cap"' -D 'units=2' -D 'stab=11.938' -D 'legend="backspace"' -o bs.stl keycap.scad
//   openscad -D 'part="inlay"' -D 'legend="U"' -o u_inlay.stl keycap.scad
//   openscad -D 'part="coupons"' -o coupons.stl keycap.scad
// "cap" and "inlay" share coordinates: load both as parts of one object
// and assign a filament to each for a two-color legend.

/* [Part] */
part = "cap";          // "cap" | "inlay" (legend fill) | "coupons" | "probe" (one legend line, flat)
legend = "U";          // "" for blank; "@win", "@up", "@down", "@left", "@right" for drawn symbols;
                       // the lower line when legend2 is set
legend2 = "";          // upper line: shifted symbol or Fn-row icon
probe_line = 1;        // part="probe": 1 = legend, 2 = legend2
homing = "none";        // "none" | "dot" | "groove"
print_top_down = false; // true: top on the bed (needs dish_depth = 0, no dot)

/* [Key size] */
units = 1;         // width in u
pitch = 19.05;     // switch spacing; each extra u adds this to the length
stab = 0;          // stabilizer stem distance from the switch stem; 0 = no stabilizer

/* [Outline, measure from a stock cap] */
bottom_w = 17.8;   // 1u skirt footprint, square; also the depth of every key
top_w = 14.0;      // 1u top width at mid-depth; the sloped top makes it slightly trapezoidal
h_front = 4.6;     // skirt bottom to top edge, user side
h_back = 3.7;      // skirt bottom to top edge, far side
dish_depth = 0.4;  // spherical dish depth below the top plane at the center
r_top = 2.5;       // corner radius, top
r_bottom = 1.2;    // corner radius, skirt

/* [Shell] */
wall = 1.2;
roof = 1.2;        // below the lowest top edge

/* [Stem socket, tune with coupons] */
stem_d = 5.5;
cross_l = 4.15;    // Cherry: 4.1 +0.05; FDM shrinks holes
cross_w = 1.27;    // Cherry: 1.17 +-0.02
socket_depth = 3.8;
stem_drop = 2.0;   // stem bottom below skirt bottom (negative = recessed)

/* [Legend and homing] */
legend_size = 4;
legend_depth = 0.6;  // 3 layers at 0.2 mm, enough for light on dark
legend_font = "DejaVu Sans:style=Book";
legend_dx = 0;       // shift so the glyph ink, not its advance box, is centered (set by build.py)
legend_dy = 0;
legend2_size = 3;
legend2_font = "DejaVu Sans:style=Book";
legend2_dx = 0;
legend2_dy = 0;
line_gap = 2.6;      // two-line legends: each line's center above or below the top center
stock_dot_d = 1.5;   // stock homing dot diameter where it meets the surface
stock_dot_h = 0.3;   // stock homing dot height
bump_scale = 1.1;    // homing dot size relative to stock
dot_d = stock_dot_d * bump_scale;
dot_h = stock_dot_h * bump_scale;
bar_l = 4;         // groove
bar_w = 1.0;
bar_h = 0.35;      // groove depth
bar_from_front = 1.6;  // homing mark center distance from the front top edge

/* [Coupons] */
coupon_lengths = [4.05, 4.10, 4.15, 4.20, 4.25];  // rows A-E
coupon_widths = [1.17, 1.22, 1.27, 1.32, 1.37];   // columns 1-5
coupon_pitch = 12;

$fn = 48;
eps = 0.01;

// Top plane through the front and back edges: z = height - slope * y (front is -y).
height = (h_front + h_back) / 2;
slope = (h_front - h_back) / top_w;
tilt = -atan(slope);

// Footprint and top length along x; wider keys grow by one pitch per extra u.
bottom_l = bottom_w + (units - 1) * pitch;
top_l = top_w + (units - 1) * pitch;
stems = stab > 0 ? [-stab, 0, stab] : [0];

// Sphere through the top edge midpoints, dish_depth below the top plane at the center,
// stretched along x by dish_sx so wide keys get the same depth.
dish_r = dish_depth > 0 ? (pow(top_w / 2, 2) + pow(dish_depth, 2)) / (2 * dish_depth) : 0;
dish_sx = top_l / top_w;
ceiling = min(h_front, h_back) - roof;
assert(socket_depth <= ceiling + stem_drop, "socket breaks through the roof");
assert(stab == 0 || stab + stem_d / 2 < bottom_l / 2 - wall, "stabilizer stem outside the cavity");
assert(!print_top_down || (dish_depth == 0 && slope == 0 && homing != "dot"), "top-down print needs a flat, level top");

function surface_z(x, y) = height - slope * y + (dish_depth > 0
    ? dish_r - sqrt(pow(dish_r, 2) - pow(x / dish_sx, 2) - y * y) - dish_depth
    : 0);

// Everything above the top surface (sloped plane, then dish), lowered by `off`.
module above_surface(off = 0) {
    translate([0, 0, height]) rotate([tilt, 0, 0]) {
        translate([-bottom_l, -bottom_w, -off]) cube([2 * bottom_l, 2 * bottom_w, 10]);
        if (dish_depth > 0)
            translate([0, 0, dish_r - dish_depth]) scale([dish_sx, 1, 1]) sphere(r = dish_r + off, $fn = 160);
    }
}

module rrect(l, w, r, h = eps) {
    linear_extrude(h) offset(r) square([l - 2 * r, w - 2 * r], center = true);
}

// Outer length, width and corner radius at height z, tapering linearly from skirt to top.
function length_at(z) = bottom_l + (top_l - bottom_l) * z / height;
function width_at(z) = bottom_w + (top_w - bottom_w) * z / height;
function radius_at(z) = r_bottom + (r_top - r_bottom) * z / height;

// Middle of the top face in plan; the lower back edge sits farther out than the front.
top_center_y = (width_at(h_back) - width_at(h_front)) / 4;

// Straight-walled frustum inset by `inset`, cut flat at z1.
module frustum(inset, z1) {
    hull() {
        rrect(bottom_l - 2 * inset, bottom_w - 2 * inset, max(r_bottom - inset, 0.3));
        translate([0, 0, z1 - eps])
            rrect(length_at(z1) - 2 * inset, width_at(z1) - 2 * inset, max(radius_at(z1) - inset, 0.3));
    }
}

// Outer shape: walls at a constant angle, cut by the sloped, dished top.
module body() {
    difference() {
        frustum(0, max(h_front, h_back) + 1);
        above_surface();
    }
}

module socket(l, w, depth) {
    translate([0, 0, -eps]) {
        translate([-l / 2, -w / 2, 0]) cube([l, w, depth]);
        translate([-w / 2, -l / 2, 0]) cube([w, l, depth]);
    }
}

bar_y = -width_at(h_front) / 2 + bar_from_front;

// Homing dot: a spherical cap dot_d wide and dot_h tall, standing normal to the top
// surface. The sphere is clipped just below the surface so it cannot reach the cavity.
dot_tilt = atan((surface_z(0, bar_y + 0.01) - surface_z(0, bar_y - 0.01)) / 0.02);
dot_r = (pow(dot_d / 2, 2) + pow(dot_h, 2)) / (2 * dot_h);
module homing_dot() {
    translate([0, bar_y, surface_z(0, bar_y)]) rotate([dot_tilt, 0, 0])
        intersection() {
            translate([0, 0, dot_h - dot_r]) sphere(r = dot_r, $fn = 64);
            translate([-dot_r, -dot_r, -0.3]) cube([2 * dot_r, 2 * dot_r, dot_h + 0.3]);
        }
}

// Groove outline from z0 to z1, centered on the front of the top face.
module homing_bar(z0, z1) {
    translate([0, bar_y, z0])
        hull() for (x = [-1, 1] * (bar_l - bar_w) / 2)
            translate([x, 0, 0]) cylinder(d = bar_w, h = z1 - z0, $fn = 24);
}

module legend_line(n) {
    t = n == 1 ? legend : legend2;
    size = n == 1 ? legend_size : legend2_size;
    if (t == "@win")
        win_logo(size);
    else if (t == "@up" || t == "@down" || t == "@left" || t == "@right")
        chevron(size, t == "@up" ? 0 : t == "@left" ? 90 : t == "@down" ? 180 : 270);
    else
        text(t, size = size, font = n == 1 ? legend_font : legend2_font, halign = "center", valign = "center");
}

// Arrow key: an open chevron of two straight strokes, pointing up when rotated by 0.
module chevron(size, angle) {
    w = size * 0.75;
    stroke = size * 0.12;
    rotate(angle) for (x = [-1, 1])
        hull() {
            translate([x * w / 2, -w / 4]) circle(d = stroke, $fn = 16);
            translate([0, w / 4]) circle(d = stroke, $fn = 16);
        }
}

// Windows key: four squares, `size` wide.
module win_logo(size) {
    gap = size / 10;
    for (x = [-1, 1], y = [-1, 1])
        translate([x * (size + gap) / 4, y * (size + gap) / 4])
            offset(r = gap / 2) square((size - gap) / 2 - gap, center = true);
}

// Both legend lines in plan, centered on the top face.
module legend_2d() {
    gap = legend2 == "" ? 0 : line_gap;
    if (legend != "") translate([legend_dx, legend_dy - gap]) legend_line(1);
    if (legend2 != "") translate([legend2_dx, legend2_dy + gap]) legend_line(2);
}

// Legend recess: the glyphs from the top surface down to legend_depth below it.
module legend_recess() {
    intersection() {
        translate([0, top_center_y, ceiling])
            linear_extrude(h_front + 1 - ceiling) legend_2d();
        above_surface(legend_depth);
    }
}

// Legend fill: the recess up to the top surface.
module legend_inlay() {
    difference() {
        legend_recess();
        above_surface();
    }
}

module cap() {
    difference() {
        union() {
            difference() {
                body();
                translate([0, 0, -eps]) frustum(wall, ceiling);
            }
            for (x = stems)
                translate([x, 0, -stem_drop]) cylinder(d = stem_d, h = ceiling + stem_drop + eps);
            if (homing == "dot") homing_dot();
        }
        for (x = stems)
            translate([x, 0, -stem_drop]) socket(cross_l, cross_w, socket_depth);
        if (legend != "" || legend2 != "")
            legend_recess();
        if (homing == "groove")
            homing_bar(surface_z(0, bar_y) - bar_h, h_front + 1);
    }
}

// Socket test pieces: a stem on a labeled tab. Press each onto a switch, keep the snug one.
module coupon(l, w, label) {
    tab = [coupon_pitch - 1, 4.5, 1.2];
    difference() {
        union() {
            translate([-tab[0] / 2, -stem_d / 2 - tab[1] + 1, 0]) cube(tab);
            cylinder(d = stem_d, h = socket_depth + 1.2);
        }
        translate([0, 0, socket_depth + 1.2 + eps]) mirror([0, 0, 1]) socket(l, w, socket_depth);
        translate([0, -stem_d / 2 - tab[1] / 2 + 1, tab[2] - 0.4])
            linear_extrude(1) text(label, size = 2.8, font = legend_font, halign = "center", valign = "center");
    }
}

module coupons() {
    rows = "ABCDE";
    for (i = [0 : len(coupon_lengths) - 1], j = [0 : len(coupon_widths) - 1])
        translate([j * coupon_pitch, -i * coupon_pitch, 0])
            coupon(coupon_lengths[i], coupon_widths[j], str(rows[i], j + 1));
}

module print_pose() {
    if (print_top_down && homing != "dot")
        translate([0, 0, height]) rotate([180, 0, 0]) children();
    else
        translate([0, 0, max(stem_drop, 0)]) children();
}

if (part == "cap") {
    print_pose() cap();
} else if (part == "inlay") {
    print_pose() legend_inlay();
} else if (part == "coupons") {
    coupons();
} else if (part == "probe") {
    linear_extrude(1) legend_line(probe_line);
}

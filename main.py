import cadquery as cq

# === Parameters ===
plate_width = 100.0  # mm
plate_length = 120.0  # mm
plate_thickness = 5.0  # mm
corner_radius = 10.0  # rounded corners

mount_hole_spacing_x = 50  # mm
mount_hole_spacing_y = 101.3   # mm
mount_hole_diameter = 5.5  # mm (M5 clearance)

profile_width = 40.0  # mm (4040 profile)
clamp_plate_thickness = 6.0  # mm
clamp_plate_length = 80.0  # mm
clamp_plate_height = 40.0  # mm
clamp_hole_diameter = 8.5  # mm (M8 clearance)
clamp_hole_z_pos = 20.0

# === Main Mounting Plate ===
# plate = cq.Workplane("XY").box(plate_width, plate_length, plate_thickness)
plate = (
    cq.Workplane("XY")
    .rect(plate_width, plate_length)
    .extrude(plate_thickness)
    .edges("|Z").fillet(corner_radius)  # Fillet vertical edges
)

# Drill Joystick Mount Holes
for x in [-mount_hole_spacing_x / 2, mount_hole_spacing_x / 2]:
    for y in [-mount_hole_spacing_y / 2, mount_hole_spacing_y / 2]:
        plate = plate.faces(">Z").workplane().pushPoints([(x, y)]).hole(mount_hole_diameter)


# === Clamp Plate Generator ===
def create_clamp_plate(x_offset):
    sign = 1 if x_offset > 0 else -1

    clamp = (
        cq.Workplane("XY")
        .box(clamp_plate_thickness, clamp_plate_length, clamp_plate_height)
        .translate((x_offset + sign * (clamp_plate_thickness / 2 + 1), 0, plate_thickness + clamp_plate_height / 2))
    )

    # Horizontal slot: 50mm long x 8.5mm wide
    hole_pos = (x_offset + clamp_plate_thickness / 2 + 1, 0, clamp_hole_z_pos + plate_thickness)
    slot_profile = (
        cq.Workplane("YZ", origin=hole_pos)
        .slot2D(length=50.0, diameter=clamp_hole_diameter)
        .extrude(clamp_plate_thickness + 10, both=True)
    )

    return clamp.cut(slot_profile)


# Generate side clamps
clamp1 = create_clamp_plate(profile_width / 2)
clamp2 = create_clamp_plate(-profile_width / 2)

# Combine all parts
mount = plate.union(clamp1).union(clamp2)

# Export
cq.exporters.export(mount, "files/joystick_mount.step")
cq.exporters.export(mount, "files/joystick_mount.stl")
cq.exporters.export(mount, "images/joystick_mount.svg")

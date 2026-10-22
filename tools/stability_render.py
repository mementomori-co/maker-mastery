r"""stability_render.py - runs INSIDE Blender (headless); called by stability_check.py --render.

What it does: imports the STLs, draws the centre of mass and the support polygon, and renders three orthographic views.
  "<blender_exe>" --background --factory-startup -noaudio --python-exit-code 1 --python tools\\stability_render.py -- job.json
Input: job.json written by stability_check.py:
  {"objects":[{"path": stl, "color":[r,g,b]}...], "hull":[[x,y]...], "floor_z": z, "com":[x,y,z],
   "bbox":[[xmin,ymin,zmin],[xmax,ymax,zmax]], "out_prefix": "..."}
Outputs: <out_prefix>-front.png (camera at -Y looking +Y, +X right), -side.png (camera at +X looking -X, +Y right),
-top.png (camera above). Workbench, studio light, cavity, object colours, X-ray so the CoM sphere shows through the part.
CoM: red sphere + red plumb line to the floor + two red cross-bars at CoM height spanning the bounding box.
Support polygon: blue slab 1.0 mm thick directly under the floor plane (stability_check.py passes it buffered 1 mm outward).
Written for the Blender 5.x Python API (bpy.ops.wm.stl_import); not tested on older versions.
Example: .venv\Scripts\python.exe tools\stability_check.py part.stl --render work\renders\part
"""
import json
import math
import sys

import bmesh  # noqa: F401  (import check only)
import bpy
import mathutils

job = json.load(open(sys.argv[sys.argv.index("--") + 1], encoding="utf-8"))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def link(ob):
    sc.collection.objects.link(ob)
    return ob


def mesh_obj(name, verts, faces, color):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.color = tuple(color) + (1.0,)
    return link(ob)


def box(name, c, size, color):
    x, y, z = c
    sx, sy, sz = [s / 2 for s in size]
    v = [(x - sx, y - sy, z - sz), (x + sx, y - sy, z - sz), (x + sx, y + sy, z - sz), (x - sx, y + sy, z - sz),
         (x - sx, y - sy, z + sz), (x + sx, y - sy, z + sz), (x + sx, y + sy, z + sz), (x - sx, y + sy, z + sz)]
    f = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_obj(name, v, f, color)


for o in job["objects"]:
    bpy.ops.wm.stl_import(filepath=o["path"])
    ob = bpy.context.selected_objects[0]
    ob.color = tuple(o["color"]) + (1.0,)

bb = job["bbox"]
ext = [bb[1][i] - bb[0][i] for i in range(3)]
H = max(ext)
floor = job["floor_z"]
com = job["com"]
RED = (0.9, 0.05, 0.05)
BLUE = (0.1, 0.35, 0.95)

# support polygon slab under the floor
hull = job["hull"]
if hull and len(hull) >= 4:
    pts = hull[:-1] if hull[0] == hull[-1] else hull
    n = len(pts)
    verts = [(p[0], p[1], floor - 1.0) for p in pts] + [(p[0], p[1], floor - 0.02) for p in pts]
    faces = [tuple(range(n)), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    mesh_obj("hull", verts, faces, BLUE)

# CoM markers
r = max(0.025 * H, 1.0)
bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=com, segments=32, ring_count=16)
sph = bpy.context.active_object
sph.color = RED + (1.0,)
sph.name = "com"
t = max(0.004 * H, 0.3)
box("plumb", (com[0], com[1], (com[2] + floor) / 2), (t, t, com[2] - floor), RED)
pad = 0.15 * H
box("bar_x", (com[0], com[1], com[2]), (ext[0] + 2 * pad, t, t), RED)
box("bar_y", (com[0], com[1], com[2]), (t, ext[1] + 2 * pad, t), RED)

# render settings
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "STUDIO"
sh.color_type = "OBJECT"
sh.show_cavity = True
sh.cavity_type = "BOTH"
sh.show_shadows = False
try:
    sh.show_xray = True
    sh.xray_alpha = 0.55
except Exception as e:  # noqa: BLE001
    print("xray not available:", e)
try:
    sh.background_type = "WORLD"
except Exception:  # noqa: BLE001
    pass
w = bpy.data.worlds.new("w")
w.color = (0.9, 0.91, 0.93)
sc.world = w
sc.render.resolution_x = 1400
sc.render.resolution_y = 1400
sc.render.film_transparent = False
cd = bpy.data.cameras.new("c")
cam = link(bpy.data.objects.new("c", cd))
sc.camera = cam
cd.clip_end = 20000
cd.type = "ORTHO"
centre = mathutils.Vector([(bb[0][i] + bb[1][i]) / 2 for i in range(3)])
centre.z = (floor - 1.0 + bb[1][2]) / 2
scale = 1.35 * max(ext[0] + 2 * pad, ext[1] + 2 * pad, bb[1][2] - floor + 1.0)
shots = [("front", (0, -1, 0)), ("side", (1, 0, 0)), ("top", (0, 0, 1))]
for name, d in shots:
    d = mathutils.Vector(d).normalized()
    cd.ortho_scale = scale
    cam.location = centre + d * (3 * H + 500)
    if name == "top":
        cam.rotation_euler = (0.0, 0.0, 0.0)
    else:
        cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = job["out_prefix"] + f"-{name}.png"
    bpy.ops.render.render(write_still=True)
    print("wrote", sc.render.filepath)

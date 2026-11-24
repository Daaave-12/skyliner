"""Skyliner Renderings (Blender 4.2 bis 5.3): OBJ je Werkstoff laden, Studio-Licht, Cycles (GPU wenn vorhanden).
Aufruf am PC:  blender.exe -b -P render.py -- mesh_dir shots.json out_dir [samples] [nur_shot1,shot2]
Speichert die Szene als Skyliner_Render_vNN.blend (Zwischenversionen) in out_dir."""
import bpy, sys, json, os, math
from mathutils import Vector
A = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
mesh, shots, out = A[0], A[1], A[2]; SAMPLES = int(A[3]) if len(A) > 3 else 96
ONLY = set(A[4].split(',')) if len(A) > 4 and A[4] else None
VER = os.environ.get('SKY_VER', 'v90')
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
def node_mat(name, base, rough=0.5, metal=0.0, trans=0.0, wood=None, ior=1.45, alpha=1.0):
    m = bpy.data.materials.new(name)
    try: m.use_nodes = True
    except Exception: pass
    nt = m.node_tree; b = nt.nodes.get('Principled BSDF')
    if b is None:
        b = nt.nodes.new('ShaderNodeBsdfPrincipled'); o_ = next((n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'), None) or nt.nodes.new('ShaderNodeOutputMaterial')
        nt.links.new(b.outputs[0], o_.inputs['Surface'])
    b.inputs['Base Color'].default_value = (*base, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    b.inputs['Transmission Weight'].default_value = trans; b.inputs['IOR'].default_value = ior
    if wood:      # Maserung: gestreckte Wellen + Rauschen entlang der Faser (Z bzw. X)
        c1, c2, sx = wood
        tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = sx
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; nz.inputs['Detail'].default_value = 8; nz.inputs['Distortion'].default_value = 4.0
        wv = nt.nodes.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = 2.5; wv.inputs['Distortion'].default_value = 6.0; wv.inputs['Detail'].default_value = 6
        ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = (*c1, 1); ramp.color_ramp.elements[1].color = (*c2, 1)
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], wv.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
        mix = nt.nodes.new('ShaderNodeMath'); mix.operation = 'MULTIPLY_ADD'; mix.inputs[1].default_value = 0.6
        nt.links.new(wv.outputs['Fac'], mix.inputs[0]); nt.links.new(nz.outputs['Fac'], mix.inputs[2])
        nt.links.new(mix.outputs[0], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    return m
MATS = {
 'nuss': node_mat('nuss', (0.12, 0.06, 0.03), 0.45, wood=((0.07, 0.035, 0.018), (0.2, 0.1, 0.05), (6, 6, 0.8))),
 'ahorn': node_mat('ahorn', (0.85, 0.72, 0.52), 0.5, wood=((0.62, 0.45, 0.27), (0.8, 0.63, 0.42), (6, 6, 0.8))),
 'kante': node_mat('kante', (0.75, 0.6, 0.4), 0.55, wood=((0.4, 0.26, 0.14), (0.7, 0.53, 0.33), (1.2, 1.2, 8))),
 'birke': node_mat('birke', (0.88, 0.78, 0.6), 0.55),
 'messing': node_mat('messing', (0.85, 0.62, 0.28), 0.22, 1.0),
 'stahl': node_mat('stahl', (0.75, 0.76, 0.78), 0.3, 1.0),
 'alu': node_mat('alu', (0.86, 0.87, 0.88), 0.35, 1.0),
 'bronze': node_mat('bronze', (0.55, 0.38, 0.2), 0.3, 1.0),
 'glas': node_mat('glas', (0.9, 0.97, 0.95), 0.0, trans=1.0, ior=1.5),
 'deko_glas': node_mat('deko_glas', (0.95, 0.97, 0.97), 0.0, trans=1.0, ior=1.5),
 'flasche': node_mat('flasche', (0.05, 0.12, 0.06), 0.05, trans=0.85, ior=1.5),
 'kunststoff': node_mat('kunststoff', (0.12, 0.12, 0.12), 0.6),
 'schwarz': node_mat('schwarz', (0.04, 0.04, 0.04), 0.5),
}
objs = {}
for f in sorted(os.listdir(mesh)):
    if not f.endswith('.obj'): continue
    k = f[:-4]; bpy.ops.wm.obj_import(filepath=os.path.join(mesh, f), forward_axis='Y', up_axis='Z')
    o = bpy.context.selected_objects[0]; o.name = k; o.data.materials.clear(); o.data.materials.append(MATS.get(k.split('_', 1)[1], MATS['schwarz']))
    bpy.context.view_layer.objects.active = o
    for poly in o.data.polygons: poly.use_smooth = False
    mod = o.modifiers.new('ws', 'WEIGHTED_NORMAL') if False else None
    objs[k] = o
# Boden / Hohlkehle
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -0.1505)); fl = bpy.context.object; fl.data.materials.append(node_mat('boden', (0.75, 0.75, 0.74), 0.8))
# Welt + Licht
w = bpy.data.worlds.new('w'); sc.world = w
try: w.use_nodes = True
except Exception: pass
bg = w.node_tree.nodes.get('Background')
if bg is None:
    bg = w.node_tree.nodes.new('ShaderNodeBackground'); wo = next((n for n in w.node_tree.nodes if n.type == 'OUTPUT_WORLD'), None) or w.node_tree.nodes.new('ShaderNodeOutputWorld')
    w.node_tree.links.new(bg.outputs[0], wo.inputs['Surface'])
bg.inputs['Color'].default_value = (1, 1, 1, 1); bg.inputs['Strength'].default_value = 0.35
def area(loc, size, energy):
    bpy.ops.object.light_add(type='AREA', location=loc); L = bpy.context.object; L.data.size = size; L.data.energy = energy
    d = Vector((0, 0, 0.9)) - Vector(loc); L.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return L
area((-2.5, -3.0, 3.0), 2.5, 500); area((3.0, -2.0, 1.5), 3.0, 150); area((0.5, 3.0, 3.5), 2.0, 200); area((0.0, -1.8, 0.2), 2.0, 60)
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
try:      # GPU, wenn vorhanden
    cp = bpy.context.preferences.addons['cycles'].preferences
    for t in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI', 'METAL'):
        try:
            cp.compute_device_type = t; cp.get_devices(); devs = [d for d in cp.devices if d.type == t]
            if devs:
                for d in cp.devices: d.use = d.type == t
                sc.cycles.device = 'GPU'; print('GPU:', t, [d.name for d in devs], flush=True); break
        except Exception: pass
except Exception as e: print('kein GPU', e)
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'AgX - Base Contrast' if False else 'None'
sc.render.film_transparent = False; sc.view_settings.exposure = -1.5
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
def save(tag):
    try: bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(os.path.join(out, f'Skyliner_Render_{VER}{tag}.blend')), copy=True); print('gespeichert', tag, flush=True)
    except Exception as e: print('speichern fehlgeschlagen', e, flush=True)
save('_szene')
for s in json.load(open(shots)):
    if ONLY and s['name'] not in ONLY: continue
    sc.render.resolution_x, sc.render.resolution_y = s.get('res', (1000, 800)); sc.render.resolution_percentage = 100
    t = Vector(s['target']); d = Vector(s['dir']).normalized(); cam.location = t - d*s.get('dist', 3.0)
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = s.get('lens', 70); cam.data.clip_start = 0.005
    hide = set(s.get('hide', []))
    for k, o in objs.items(): o.hide_render = any(k == h or k.startswith(h + '_') for h in hide)
    sc.render.filepath = os.path.abspath(os.path.join(out, s['name'] + '.png')); bpy.ops.render.render(write_still=True); print('rendered', s['name'], flush=True)
    c2 = cam.copy(); c2.data = cam.data.copy(); c2.name = s['name']; sc.collection.objects.link(c2)   # Kamera je Bild in der .blend
save('')

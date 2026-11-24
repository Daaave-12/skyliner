"""Modell (model.bin + parts.json) triangulieren -> OBJ je Werkstoff für Blender. Aufruf: python3 render/export_mesh.py out_dir"""
import sys, os, json, numpy as np
sys.path.insert(0, os.getcwd())
from parts import load_model
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
S, M = load_model(); P = json.load(open('parts.json'))
def mat_of(p, nf):
    m = p['mat']; k = p['kat']
    if k in ('skip', 'wand'): return None
    if m in ('3SP_NA', '3SP_NA30'):
        n = np.array(p['n'])
        if nf is not None and nf.dot(n) > 0.9: return 'nuss'
        return 'ahorn' if nf is not None and nf.dot(n) < -0.9 else 'kante'
    if m in ('3SP_A',): return 'ahorn'
    if m == 'MH_NB': return 'nuss'
    if m == 'MPX_BI': return 'birke'
    if m == 'GLAS': return 'glas'
    if m == 'MES': return 'messing'
    if m == 'ALU' and 'hebel' in p['bez'].lower(): return 'bronze'
    if m == 'ALU': return 'alu'
    if m in ('EST', 'ST'): return 'stahl'
    if m == 'KST': return 'kunststoff'
    if k == 'deko': return 'deko_glas' if 'glas' in p['bez'].lower() else 'flasche'
    return 'schwarz'
def grp_of(p):
    b = p['bez']; n = p['name']
    if 'Synchronisierung v8' in n or b == 'Glasboden unter der Synchronisierung': return 'sync'
    if b.startswith('Tür ') or b in ('Türband Messing', 'Griffeinlage'): return 'tuer'
    if b == 'Deckelblende vorne': return 'blende'
    if b == 'Deckel': return 'deckel'
    if b.startswith(('Lade ', 'Formeinsatz', 'Humidor', 'Gitter', 'Glas Humidor', 'Innenlade')): return 'lade'
    if p['kat'] == 'deko': return 'deko'
    return 'korpus'
buf = {}
for p in P:
    i = p['i']; sh = S[i]
    BRepMesh_IncrementalMesh(sh, 0.3, False, 0.3, True)
    ex = TopExp_Explorer(sh, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face(ex.Current()); loc = TopLoc_Location(); tri = BRep_Tool.Triangulation_s(f, loc)
        nf = None; a = BRepAdaptor_Surface(f)
        if a.GetType() == GeomAbs_Plane:
            d = a.Plane().Axis().Direction(); nf = np.array([d.X(), d.Y(), d.Z()])
            if f.Orientation().name == 'TopAbs_REVERSED': nf = -nf
        m = mat_of(p, nf)
        if tri is not None and m:
            T = loc.Transformation(); V = []
            for k in range(1, tri.NbNodes()+1):
                q = tri.Node(k).Transformed(T); V.append((q.X(), q.Y(), q.Z()))
            F = []
            rev = f.Orientation().name == 'TopAbs_REVERSED'
            for k in range(1, tri.NbTriangles()+1):
                a1, b1, c1 = tri.Triangle(k).Get(); F.append((a1, c1, b1) if rev else (a1, b1, c1))
            buf.setdefault(grp_of(p) + '_' + m, []).append((V, F, i))
            if p.get('pos') and p['kat'] == 'holz' and p['pos'] <= 47: buf.setdefault(f"p{p['pos']}-{i}_" + m, []).append((V, F, i))
        ex.Next()
for m, L in buf.items():
    with open(f'{out}/{m}.obj', 'w') as fo:
        off = 0
        for V, F, i in L:
            for v in V: fo.write('v %.3f %.3f %.3f\n' % (v[0]/1000, v[1]/1000, v[2]/1000))
            for a1, b1, c1 in F: fo.write(f'f {a1+off} {b1+off} {c1+off}\n')
            off += len(V)
print({m: len(L) for m, L in buf.items()})

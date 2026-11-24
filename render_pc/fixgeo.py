"""Alte Teile der früheren Synchronisierung aus dem Modell entfernen (Wunsch des Nutzers 24.11.2026):
Tasche 5 tief mit 4 Bohrungen Ø8/12 an der Innenseite der beiden oberen Türen (ohne Beschlag im Modell Skyliner v89)."""
import numpy as np
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRepAlgoAPI import BRepAlgoAPI_Defeaturing
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
OLD = {6: (229.5, -75.6, 1612.6), 24: (-229.5, -75.6, 1612.6)}      # Mitte der alten Tasche
GEOV = 'ohne_alte_sync_tasche'
def bbox(f):
    b = Bnd_Box(); BRepBndLib.Add_s(f, b)
    return b.CornerMin(), b.CornerMax()
def clean(S):
    for i, c in OLD.items():
        if i >= len(S): continue
        c = np.array(c); df = BRepAlgoAPI_Defeaturing(); df.SetShape(S[i]); n = 0
        ex = TopExp_Explorer(S[i], TopAbs_FACE)
        while ex.More():
            f = TopoDS.Face(ex.Current()); a, b = bbox(f)
            lo = np.array([a.X(), a.Y(), a.Z()]); hi = np.array([b.X(), b.Y(), b.Z()])
            if np.linalg.norm((lo + hi)/2 - c) < 40 and max(hi - lo) < 70: df.AddFaceToRemove(f); n += 1
            ex.Next()
        df.Build()
        if df.IsDone() and n: S[i] = df.Shape()
    return S

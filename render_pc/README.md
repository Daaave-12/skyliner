# Skyliner Renderings (Blender 5.3)

Modell: Skyliner v89 / Sync v8, Pos. 47 Glasboden 6 mm. Einheiten m, Z oben.

1. `Skyliner_mesh_v90.zip` nach `mesh90/` entpacken (OBJ je Gruppe_Werkstoff).
2. `blender.exe -b -P render.py -- mesh90 shots90.json out 256`
3. Ergebnis: 22 PNG in `out/`, dazu `Skyliner_Render_v90_szene.blend` und `Skyliner_Render_v90.blend` (eine Kamera je Bild).

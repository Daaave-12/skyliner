# Skyliner Renderings (Blender 5.3)

Modell: Skyliner v89 mit Synchronisierung v8, Netz-Export v90, Pos. 47 Glasboden 6 mm. Einheiten m, Z oben.

1. `Skyliner_mesh_v90.zip` nach `mesh90/` entpacken (OBJ je Gruppe_Werkstoff).
2. `blender.exe -b -P render.py -- mesh90 shots90.json out 256`
3. Ergebnis: 22 PNG in `out/`, dazu `Skyliner_Render_v90_szene.blend` und `Skyliner_Render_v90.blend` (eine Kamera je Bild).

## Netz v95 (24.11.2026)

`Skyliner_mesh_v95.zip` ersetzt mesh90/93/94 (gleiche Dateinamen, gleiche Gruppen):
- Koordinaten mit 6 Nachkommastellen in m (vorher 3, also auf 1 mm gerundet: Knicke in ebenen Flächen, wellige runde Teile).
- Feinere Tessellierung (Sehnenfehler 0,05 mm, Winkel 0,12 rad) für runde Teile.
- Alte Synchronisierungstasche entfernt: Tasche 5 tief mit 4 Bohrungen Ø8/12 an der Innenseite der oberen Türen (Pos. 10, 11), ohne Beschlag im Modell (`fixgeo.py`).
- Enthält Gesamtmodell (Gruppe_Werkstoff), Schnittmodelle (xA, xK, xG12, xG34, xG58) und Einzelteile (p<Pos>-<Nr>).
- Punkte sind je Fläche getrennt (scharfe Kanten). Für runde Teile in Blender "Merge by Distance" 0,00001 m und "Shade Auto Smooth" verwenden.

# Skyliner-Webseite

Scroll-Seite zum Meisterstück. Beim Scrollen fährt die Kamera die 11 Punkte der Blender-Kamerafahrt ab (R01 bis R10, am Schluss zurück zur offenen Hero-Ansicht), zu jedem Punkt blendet ein Text ein. Darunter folgen die Entstehung (1:10-Modell) und ein paar Eckdaten.

## Dateien

| Datei | Inhalt |
| --- | --- |
| `index.html` | Seite mit allen Texten. Die Texte stehen in den `<article class="cap">`-Blöcken und lassen sich direkt ändern. |
| `style.css` | Gestaltung |
| `main.js` | Scroll-Logik, Standbilder oder Bildsequenz |
| `frames/d/` | Kamerafahrt, 401 Bilder für Desktop (1080 × 1350, ca. 16 MB) |
| `frames/m/` | dieselbe Fahrt fürs Handy (720 × 900, ca. 9 MB) |
| `img/` | Modellfotos für die Entstehung |
| `qr_skyliner.png` / `.svg` | QR-Code auf `https://daaave-12.github.io/skyliner/` |

## Auf GitHub Pages stellen

1. Auf github.com ein neues, öffentliches Repository mit dem Namen `skyliner` anlegen.
2. Den Inhalt dieses Ordners hochladen (Add file → Upload files, alles hineinziehen, Commit).
3. Settings → Pages → Source: „Deploy from a branch“, Branch `main`, Ordner `/ (root)`, Save.
4. Nach ein bis zwei Minuten ist die Seite unter `https://daaave-12.github.io/skyliner/` erreichbar.

Der QR-Code zeigt genau auf diese Adresse. Heißt das Repository anders, muss der QR-Code neu erzeugt werden.

## Kamerafahrt

Die Kamerafahrt ist fertig gerendert und eingeschaltet (`SEQUENCE.enabled = true` in `main.js`). Sie stammt aus `Skyliner_Webseite.blend`: dunkle Szene mit Wand dahinter, das LED-Dreieck auf der Rückseite strahlt an die Wand, die Türen öffnen sich und der Drehteller mit den Weinflaschen dreht sich.

Neu rendern, falls sich am Modell etwas ändert:

1. Kamera `Skyliner_ScrollCam` aktiv lassen, Frames 1 bis 1201, Frame Step 3 (ergibt 401 Bilder), Format WebP, Qualität ca. 75.
2. Desktop 1080 × 1350 nach `frames/d/####.webp`. Blender nummeriert 0001, 0004, 0007 … 1201, genau so liest die Seite sie ein.
3. Die Handy-Bilder in `frames/m/` sind dieselben Bilder auf 720 × 900 verkleinert.

Die Seite lädt zuerst jedes 32. Bild und füllt dann auf, sodass sie sofort benutzbar ist. Wird die Sequenz ausgeschaltet, überblendet die Seite stattdessen die 11 Kamerapunkte als Standbilder.

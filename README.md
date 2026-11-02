# Skyliner-Webseite

Scroll-Seite zum Meisterstück. Beim Scrollen fährt die Kamera die 11 Punkte der Blender-Kamerafahrt ab (R01 bis R10, am Schluss zurück zur offenen Hero-Ansicht), zu jedem Punkt blendet ein Text ein. Darunter folgen die Entstehung (1:10-Modell) und ein paar Eckdaten.

## Dateien

| Datei | Inhalt |
| --- | --- |
| `index.html` | Seite mit allen Texten. Die Texte stehen in den `<article class="cap">`-Blöcken und lassen sich direkt ändern. |
| `style.css` | Gestaltung |
| `main.js` | Scroll-Logik, Standbilder oder Bildsequenz |
| `frames/d/` | Kamerafahrt, 401 Bilder für Desktop (1440 × 1800, ca. 31 MB) |
| `frames/m/` | dieselbe Fahrt fürs Handy (900 × 1125, ca. 14 MB) |
| `frames/s/` | 11 scharfe 4K-Standbilder (2160 × 2700), je eins pro Kamerapunkt |
| `img/` | Modellfotos für die Entstehung |
| `qr_skyliner.png` / `.svg` | QR-Code auf `https://daaave-12.github.io/skyliner/` |

## Auf GitHub Pages stellen

1. Auf github.com ein neues, öffentliches Repository mit dem Namen `skyliner` anlegen.
2. Den Inhalt dieses Ordners hochladen (Add file → Upload files, alles hineinziehen, Commit).
3. Settings → Pages → Source: „Deploy from a branch“, Branch `main`, Ordner `/ (root)`, Save.
4. Nach ein bis zwei Minuten ist die Seite unter `https://daaave-12.github.io/skyliner/` erreichbar.

Der QR-Code zeigt genau auf diese Adresse. Heißt das Repository anders, muss der QR-Code neu erzeugt werden.

## Kamerafahrt

Die Fahrt stammt aus `Skyliner_Webseite.blend` und wurde in 4K (2160 × 2700) ohne Motion Blur gerendert, die Originale liegen auf dem PC im Ordner `frames4k`. Die 11 Kamerapunkte (Frame 1, 121, 241 … 1201):

0 Start von rechts auf 1,85 m · 1 linke Seite · 2 Material · 3 Griff · 4 Sockel · 5 Öffnen · 6 Innenraum · 7 Andenken · 8 Wein und Whisky · 9 Schubladen von schräg oben · 10 Schluss frontal

An jedem Punkt ersetzt die Seite genau dieses eine Bild durch das 4K-Standbild aus `frames/s/`, ohne Überblendung. Dazwischen laufen die verkleinerten Bilder aus `frames/d` (Computer) bzw. `frames/m` (Handy).

Neu rendern: Frames 1 bis 1201, Frame Step 3, WebP. Desktop- und Handy-Bilder sind die 4K-Bilder verkleinert, die Standbilder sind die 4K-Bilder der Frames 1 + 120 × Punkt.

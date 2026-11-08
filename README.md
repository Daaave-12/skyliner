# Skyliner-Webseite

Scroll-Seite zum Meisterstück. Beim Scrollen fährt die Kamera die 13 Punkte der Blender-Kamerafahrt ab (vom geschlossenen Turm über das Öffnen bis zu den drei Laden, am Schluss zurück zur offenen Frontansicht), zu jedem Punkt blendet ein Text ein. Darunter folgen die Entstehung (1:10-Modell) und ein paar Eckdaten.

## Dateien

| Datei | Inhalt |
| --- | --- |
| `index.html` | Seite mit allen Texten. Die Texte stehen in den `<article class="cap">`-Blöcken und lassen sich direkt ändern. |
| `style.css` | Gestaltung |
| `main.js` | Scroll-Logik, Standbilder oder Bildsequenz |
| `frames/d/` | Kamerafahrt, 481 Bilder für Desktop (1440 × 1800) |
| `frames/m/` | dieselbe Fahrt fürs Handy (900 × 1125) |
| `frames/s/` | 13 scharfe 4K-Standbilder (2160 × 2700), je eins pro Kamerapunkt |
| `img/` | Modellfotos für die Entstehung |
| `qr_derskyliner.png` / `.svg` | QR-Code auf `https://derskyliner.at` |
| `qr_skyliner.png` / `.svg` | alter QR-Code auf `https://daaave-12.github.io/skyliner/`, leitet automatisch auf derskyliner.at weiter |
| `CNAME` | eigene Domain für GitHub Pages |

## Auf GitHub Pages stellen

1. Auf github.com ein neues, öffentliches Repository mit dem Namen `skyliner` anlegen.
2. Den Inhalt dieses Ordners hochladen (Add file → Upload files, alles hineinziehen, Commit).
3. Settings → Pages → Source: „Deploy from a branch“, Branch `main`, Ordner `/ (root)`, Save.
4. Nach ein bis zwei Minuten ist die Seite unter `https://daaave-12.github.io/skyliner/` erreichbar.

Der QR-Code zeigt genau auf diese Adresse. Heißt das Repository anders, muss der QR-Code neu erzeugt werden.

## Kamerafahrt

Die Fahrt stammt aus `Skyliner_Webseite_v2.blend` (neues Modell v40) und wurde in 4K (2160 × 2700) ohne Motion Blur gerendert, die Originale liegen auf dem PC im Ordner `frames4k_v2`. Die 13 Kamerapunkte (Frame 1, 121, 241 … 1441):

0 Start von rechts auf 1,85 m · 1 linke Seite · 2 Material · 3 Griff · 4 Sockel · 5 Öffnen (Türen schwingen bis 129° auf, Innenlicht geht an) · 6 Innenraum · 7 Andenken · 8 Wein (Drehteller dreht 72°) · 9 Lade 1 Bar · 10 Lade 2 Humidor · 11 Lade 3 Gläser · 12 Schluss frontal

Die Laden öffnen jeweils einzeln um 30 cm, ihr LED-Licht geht dabei an und beim Schließen wieder aus.

An jedem Punkt ersetzt die Seite genau dieses eine Bild durch das 4K-Standbild aus `frames/s/`, ohne Überblendung. Dazwischen laufen die verkleinerten Bilder aus `frames/d` (Computer) bzw. `frames/m` (Handy).

Neu rendern: Frames 1 bis 1441, Frame Step 3, WebP. Desktop- und Handy-Bilder sind die 4K-Bilder verkleinert, die Standbilder sind die 4K-Bilder der Frames 1 + 120 × Punkt.

## Eigene Domain derskyliner.at

Die Domain liegt bei hosttech. DNS: vier A-Einträge für `derskyliner.at` auf 185.199.108.153, .109.153, .110.153, .111.153 und ein CNAME `www` auf `daaave-12.github.io`. Die Datei `CNAME` im Repository sagt GitHub Pages, dass die Seite unter derskyliner.at läuft; die alte github.io-Adresse leitet automatisch dorthin weiter.

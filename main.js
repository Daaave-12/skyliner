// Skyliner – scroll-gekoppelte Kamerafahrt
//
// Der Scroll-Fortschritt wählt das Bild der Blender-Kamerafahrt (481 Bilder, 13 Kamerapunkte).
// An jedem Kamerapunkt wird genau dieses eine Bild durch ein scharfes 4K-Standbild ersetzt.

const SEQUENCE = {
  enabled: true,
  count: 481,                       // Blender Frame 1–1441 mit Frame Step 3
  src: (i) => `frames/${window.innerWidth < 760 ? "m" : "d"}/${String(1 + 3 * i).padStart(4, "0")}.webp`,
};

const WAYPOINTS = 13;

// Scharfe 4K-Standbilder: an jedem Kamerapunkt ersetzt genau ein Bild der Fahrt (ohne Überblendung)
const STEP = (SEQUENCE.count - 1) / (WAYPOINTS - 1);   // 40 Bilder zwischen zwei Punkten
const stillImgs = [];
function loadStills() {
  for (let w = 0; w < WAYPOINTS; w++) {
    const im = new Image();
    im.decoding = "async";
    im.onload = () => { stillImgs[w] = im; lastDrawn = -1; update(); };
    im.src = `frames/s/${String(w).padStart(2, "0")}.webp`;
  }
}

const tour = document.getElementById("tour");
const stage = tour.querySelector(".stage");
const stills = [...tour.querySelectorAll(".stills img")];
const caps = [...tour.querySelectorAll(".cap")];
const dotsNav = tour.querySelector(".dots");
const canvas = tour.querySelector(".sequence");

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const smooth = (a, b, v) => { const t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };

// Fortschritt 0 … WAYPOINTS-1 über die Höhe der Tour-Sektion
// Jeder Abschnitt zwischen zwei Punkten: an beiden Enden ein kurzer Stopp (je 5 Bilder),
// dazwischen läuft die Fahrt mit weicher Beschleunigung. Die Bildanzahl bleibt gleich.
const HOLD_FRAMES = 5;
const HOLD = HOLD_FRAMES / (STEP + 2 * HOLD_FRAMES);           // Anteil eines Abschnitts pro Stopp
const ease = (t) => 0.5 - 0.5 * Math.cos(Math.PI * t);          // sanft an- und auslaufen

function progress() {
  const r = tour.getBoundingClientRect();
  const span = tour.offsetHeight - window.innerHeight;
  const s = clamp(-r.top / span, 0, 1) * (WAYPOINTS - 1);
  const k = Math.min(Math.floor(s), WAYPOINTS - 2);
  const t = clamp((s - k - HOLD) / (1 - 2 * HOLD), 0, 1);
  return k + ease(t);
}

function scrollToWaypoint(i) {
  const span = tour.offsetHeight - window.innerHeight;
  const y = tour.offsetTop + (i / (WAYPOINTS - 1)) * span;
  if (lenis) lenis.scrollTo(y, { duration: 1.6 });
  else window.scrollTo({ top: y, behavior: "smooth" });
}

// Kapitel-Punkte
const dots = caps.map((cap, i) => {
  const b = document.createElement("button");
  b.type = "button";
  b.setAttribute("aria-label", cap.querySelector("h1, h2").textContent);
  b.addEventListener("click", () => scrollToWaypoint(i));
  dotsNav.appendChild(b);
  return b;
});

// ---------- Standbilder ----------
function renderStills(p) {
  const fadeIn = (i) => (i === 0 ? 1 : smooth(i - 0.5, i - 0.08, p));
  stills.forEach((img, i) => {
    const covered = i < stills.length - 1 && fadeIn(i + 1) >= 1;
    img.style.opacity = covered ? 0 : fadeIn(i);
    // leichtes Heranfahren an jeden Punkt
    const s = 1.035 - 0.035 * smooth(i - 0.6, i + 0.4, p);
    img.style.transform = `scale(${s.toFixed(4)})`;
  });
}

// ---------- Bildsequenz ----------
const frames = [];
let lastDrawn = -1;

function loadSequence() {
  const order = [];
  for (let step = 32; step >= 1; step = Math.floor(step / 2)) {
    for (let i = 0; i < SEQUENCE.count; i += step) if (!order.includes(i)) order.push(i);
    if (step === 1) break;
  }
  let next = 0;
  const pump = () => {
    if (next >= order.length) return;
    const i = order[next++];
    const img = new Image();
    img.decoding = "async";
    img.onload = () => { frames[i] = img; if (lastDrawn < 0) drawFrame(i); pump(); };
    img.onerror = pump;
    img.src = SEQUENCE.src(i);
  };
  for (let k = 0; k < 6; k++) pump();
}

function sizeCanvas() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = canvas.clientWidth * dpr;
  canvas.height = canvas.clientHeight * dpr;
  lastDrawn = -1;
}

function drawFrame(i) {
  // nächsten bereits geladenen Frame nehmen
  let j = -1;
  for (let d = 0; d < SEQUENCE.count; d++) {
    if (frames[i - d]) { j = i - d; break; }
    if (frames[i + d]) { j = i + d; break; }
  }
  const wp = i / STEP;
  const still = Number.isInteger(wp) ? stillImgs[wp] : null;
  if (j < 0 && !still) return;
  const key = still ? "s" + wp : j;
  if (key === lastDrawn) return;
  const img = still || frames[j];
  const ctx = canvas.getContext("2d");
  const cw = canvas.width, ch = canvas.height;
  const s = Math.min(cw / img.width, ch / img.height);
  const w = img.width * s, h = img.height * s;
  const mobile = window.innerWidth < 760;
  const x = (cw - w) * (mobile ? 0.5 : 0.62);
  const y = (ch - h) * (mobile ? 0.18 : 0.5);
  ctx.save();
  ctx.clearRect(0, 0, cw, ch);
  ctx.globalCompositeOperation = "source-over";
  ctx.drawImage(img, x, y, w, h);
  // Bildränder weich in den dunklen Hintergrund auslaufen lassen
  const g = mobile ? ctx.createLinearGradient(0, y, 0, y + h) : ctx.createLinearGradient(x, 0, x + w, 0);
  const a = mobile ? 0.06 : 0.16, b = mobile ? 0.22 : 0.16;
  g.addColorStop(0, "rgba(0,0,0,0)");
  g.addColorStop(a, "rgba(0,0,0,1)");
  g.addColorStop(1 - b, "rgba(0,0,0,1)");
  g.addColorStop(1, "rgba(0,0,0,0)");
  ctx.globalCompositeOperation = "destination-in";
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, cw, ch);
  ctx.restore();
  lastDrawn = key;
}

// ---------- Texte und Punkte ----------
function renderCaptions(p) {
  caps.forEach((cap, i) => {
    const d = p - i;
    const o = i === 0 ? 1 - smooth(0.12, 0.38, d) : 1 - smooth(0.16, 0.4, Math.abs(d));
    cap.style.opacity = o.toFixed(3);
    cap.style.visibility = o > 0.01 ? "visible" : "hidden";
    const shift = clamp(-d * 40, -40, 40);
    cap.style.translate = `0 ${shift.toFixed(1)}px`;
  });
  const active = Math.round(p);
  dots.forEach((b, i) => b.classList.toggle("on", i === active));
}

function update() {
  const p = progress();
  if (SEQUENCE.enabled) drawFrame(Math.round((p / (WAYPOINTS - 1)) * (SEQUENCE.count - 1)));
  else renderStills(p);
  renderCaptions(p);
}

// ---------- Start ----------
let lenis = null;
const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (SEQUENCE.enabled) {
  stage.classList.add("use-sequence");
  sizeCanvas();
  loadSequence();
  loadStills();
  window.addEventListener("resize", () => { sizeCanvas(); update(); });
}

if (window.Lenis && !reduced) {
  lenis = new Lenis({ lerp: 0.1, smoothWheel: true, wheelMultiplier: 1.1, touchMultiplier: 1.4 });
  lenis.on("scroll", update);
  const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
} else {
  window.addEventListener("scroll", () => requestAnimationFrame(update), { passive: true });
}
window.addEventListener("resize", update);
update();

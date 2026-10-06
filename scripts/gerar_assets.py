"""Gera os SVGs do perfil (banner, árvore de sakura, terminal, cards, títulos).

Uso: python scripts/gerar_assets.py   -> reescreve os arquivos em assets/
Edite os textos aqui (nome, frases, projetos) e rode de novo.
"""
import math
import random
import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent) / "assets"
OUT.mkdir(parents=True, exist_ok=True)

PINKS = ["#e4eaff", "#d1dbff", "#bfccfb", "#aabbf7", "#9baef1", "#899fe8"]
SERIF = "'Cormorant Garamond', 'Playfair Display', Georgia, 'Times New Roman', serif"
SANS = "'Segoe UI', 'Inter', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'DejaVu Sans Mono', monospace"
JP = "'Noto Serif JP', 'Yu Mincho', 'Hiragino Mincho ProN', 'IPAMincho', 'Noto Sans JP', 'IPAGothic', serif"

PETAL = "M0 10 C-7 4 -8 -4 -3 -9 L0 -6 L3 -9 C8 -4 7 4 0 10Z"


def f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def petal_defs():
    return f"""
    <path id="petal" d="{PETAL}"/>
    <g id="flower">
      {''.join(f'<use href="#petal" transform="rotate({a}) translate(0 -9)"/>' for a in range(0, 360, 72))}
      <circle r="3.2" fill="#f3f6ff"/>
      <circle r="1.6" fill="#6a86e8"/>
    </g>"""


def falling_petals(rng, n, w, h, colors=PINKS, scale=(0.6, 1.2), dur=(9, 16)):
    out = []
    for _ in range(n):
        x = rng.uniform(-40, w + 40)
        d = rng.uniform(*dur)
        begin = -rng.uniform(0, d)
        s = rng.uniform(*scale)
        sway = rng.uniform(25, 70)
        drift = rng.uniform(40, 160)
        pts = []
        for k in range(6):
            t = k / 5
            px = x + drift * t + sway * math.sin(t * math.pi * 2 + rng.uniform(0, 1))
            py = -30 + (h + 60) * t
            pts.append(f"{f(px)} {f(py)}")
        spin = rng.choice([360, -360])
        color = rng.choice(colors)
        op = rng.uniform(0.65, 0.95)
        out.append(
            f'<g opacity="{op:.2f}"><animateTransform attributeName="transform" type="translate" '
            f'values="{";".join(pts)}" dur="{d:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<use href="#petal" fill="{color}" transform="scale({s:.2f})">'
            f'<animateTransform attributeName="transform" type="rotate" from="0" to="{spin}" '
            f'dur="{rng.uniform(3, 6):.1f}s" begin="{begin:.1f}s" repeatCount="indefinite" additive="sum"/>'
            f"</use></g>"
        )
    return "\n".join(out)


def stars(rng, n, w, h):
    out = []
    for i in range(n):
        x, y = rng.uniform(0, w), rng.uniform(0, h) ** 1.0
        r = rng.choice([0.6, 0.8, 1, 1, 1.3, 1.7])
        op = rng.uniform(0.35, 0.95)
        if i % 3 == 0:
            d = rng.uniform(2, 5)
            out.append(
                f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="#fff" opacity="{op:.2f}">'
                f'<animate attributeName="opacity" values="{op:.2f};0.1;{op:.2f}" dur="{d:.1f}s" '
                f'begin="{-rng.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>'
            )
        else:
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="#fff" opacity="{op:.2f}"/>')
    return "\n".join(out)


def branch_blossoms(rng, segments, density, size=(0.55, 1.05)):
    """Flores e botões espalhados ao longo de uma lista de segmentos (x1,y1,x2,y2)."""
    out = []
    for (x1, y1, x2, y2) in segments:
        n = max(1, int(math.hypot(x2 - x1, y2 - y1) / density))
        for _ in range(n):
            t = rng.random()
            x = x1 + (x2 - x1) * t + rng.uniform(-14, 14)
            y = y1 + (y2 - y1) * t + rng.uniform(-14, 14)
            if rng.random() < 0.7:
                s = rng.uniform(*size)
                out.append(
                    f'<use href="#flower" fill="{rng.choice(PINKS)}" '
                    f'transform="translate({f(x)} {f(y)}) rotate({rng.randint(0, 72)}) scale({s:.2f})"/>'
                )
            else:
                out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{rng.uniform(2.5, 5):.1f}" fill="{rng.choice(PINKS[2:])}"/>')
    return "\n".join(out)


# --------------------------------------------------------------------------- banner
def banner():
    rng = random.Random(7)
    W, H = 1280, 440

    # galho no canto superior esquerdo
    main = "M-20 40 C80 60 150 50 230 95 C290 128 330 120 390 150"
    sub = [
        "M120 58 C140 30 170 20 205 12",
        "M230 95 C250 70 275 62 300 58",
        "M300 125 C320 160 340 175 370 190",
        "M60 52 C70 80 90 100 115 120",
    ]
    segs = [(-20, 40, 230, 95), (230, 95, 390, 150), (120, 58, 205, 12), (230, 95, 300, 58),
            (300, 125, 370, 190), (60, 52, 115, 120)]
    blossoms = branch_blossoms(rng, segs, 26)

    # galho no canto superior direito (menor)
    r_main = "M1300 18 C1240 30 1210 24 1160 48 C1130 62 1105 58 1075 70"
    r_segs = [(1300, 18, 1160, 48), (1160, 48, 1075, 70), (1200, 30, 1180, 0)]
    r_blossoms = branch_blossoms(rng, r_segs, 28, size=(0.45, 0.85))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Diego S. Souza">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#040a0f"/>
      <stop offset=".45" stop-color="#0f2133"/>
      <stop offset=".75" stop-color="#1f334f"/>
      <stop offset="1" stop-color="#44588a"/>
    </linearGradient>
    <radialGradient id="moon" cx=".42" cy=".4" r=".7">
      <stop offset="0" stop-color="#fafbff"/>
      <stop offset=".6" stop-color="#e3e9ff"/>
      <stop offset="1" stop-color="#c1cdf6"/>
    </radialGradient>
    <radialGradient id="halo">
      <stop offset="0" stop-color="#d1dbff" stop-opacity=".55"/>
      <stop offset=".35" stop-color="#a6b8f4" stop-opacity=".18"/>
      <stop offset="1" stop-color="#a6b8f4" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="fuji" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2a425c"/>
      <stop offset="1" stop-color="#122336"/>
    </linearGradient>
    <linearGradient id="snow" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f2f5fd"/>
      <stop offset="1" stop-color="#b6c4d8"/>
    </linearGradient>
    <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#d6dfff"/>
      <stop offset=".5" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#aabbf7"/>
    </linearGradient>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#162940"/>
      <stop offset="1" stop-color="#070e16"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft"><feGaussianBlur stdDeviation="14"/></filter>
    <linearGradient id="shoot" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff"/>
    </linearGradient>
    {petal_defs()}
  </defs>

  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <g>{stars(rng, 140, W, 300)}</g>

  <!-- estrela cadente -->
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.04;.1;1" dur="9s" begin="2s" repeatCount="indefinite"/>
    <line x1="0" y1="0" x2="120" y2="0" stroke="url(#shoot)" stroke-width="2" stroke-linecap="round">
      <animateTransform attributeName="transform" type="translate" values="420 40;700 150;700 150" keyTimes="0;.1;1" dur="9s" begin="2s" repeatCount="indefinite"/>
    </line>
  </g>

  <!-- lua -->
  <circle cx="1085" cy="128" r="230" fill="url(#halo)">
    <animate attributeName="r" values="220;240;220" dur="8s" repeatCount="indefinite"/>
  </circle>
  <circle cx="1085" cy="128" r="70" fill="url(#moon)"/>
  <g fill="#b9c6f2" opacity=".35">
    <circle cx="1062" cy="110" r="10"/><circle cx="1104" cy="146" r="13"/><circle cx="1096" cy="102" r="5"/><circle cx="1068" cy="152" r="6"/>
  </g>

  <!-- monte Fuji -->
  <path d="M700 360 L935 248 Q955 238 975 248 L1250 360 Z" fill="url(#fuji)"/>
  <path d="M899 265 L935 248 Q955 238 975 248 L1012 266 L998 274 L984 265 L970 278 L955 267 L941 279 L928 268 L914 275 Z" fill="url(#snow)"/>

  <!-- névoa -->
  <g filter="url(#soft)" opacity=".55">
    <ellipse cx="500" cy="330" rx="420" ry="26" fill="#8b9cc9">
      <animate attributeName="cx" values="460;560;460" dur="22s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="1050" cy="345" rx="360" ry="22" fill="#7a8cb5">
      <animate attributeName="cx" values="1080;980;1080" dur="26s" repeatCount="indefinite"/>
    </ellipse>
  </g>

  <!-- colinas -->
  <path d="M0 330 C140 300 260 318 380 312 C520 305 600 340 760 336 C900 332 1040 318 1280 330 L1280 440 L0 440 Z" fill="#101f30"/>

  <!-- pagode -->
  <g fill="#0a1624" transform="translate(1195 232)">
    <rect x="-3" y="-34" width="6" height="40"/>
    <path d="M-30 18 Q0 8 30 18 L24 22 L-24 22 Z"/><rect x="-18" y="22" width="36" height="14"/>
    <path d="M-38 42 Q0 30 38 42 L30 46 L-30 46 Z"/><rect x="-22" y="46" width="44" height="16"/>
    <path d="M-46 68 Q0 54 46 68 L37 72 L-37 72 Z"/><rect x="-26" y="72" width="52" height="18"/>
    <path d="M-54 96 Q0 80 54 96 L44 100 L-44 100 Z"/><rect x="-30" y="100" width="60" height="30"/>
    <rect x="-5" y="112" width="10" height="18" fill="#aabbf7" opacity=".55"/>
  </g>

  <!-- água com reflexo da lua -->
  <rect x="0" y="372" width="{W}" height="68" fill="url(#water)"/>
  <g fill="#d1dbff">
    <rect x="1050" y="380" width="70" height="2.5" rx="1.2" opacity=".55"><animate attributeName="width" values="70;40;70" dur="4s" repeatCount="indefinite"/></rect>
    <rect x="1063" y="392" width="44" height="2" rx="1" opacity=".4"><animate attributeName="x" values="1063;1073;1063" dur="5s" repeatCount="indefinite"/></rect>
    <rect x="1072" y="404" width="26" height="2" rx="1" opacity=".3"/>
    <rect x="1078" y="415" width="14" height="1.6" rx=".8" opacity=".2"/>
  </g>

  <!-- penhasco + samurai -->
  <path d="M0 440 L0 300 C40 292 90 296 120 300 C160 306 190 312 215 322 C240 334 262 352 300 372 C320 384 330 410 340 440 Z" fill="#04090f"/>
  <g transform="translate(150 300)" fill="#04090f">
    <path d="M-34 -96 Q0 -116 34 -96 Q0 -90 -34 -96 Z"/>
    <circle cx="0" cy="-88" r="9"/>
    <path d="M-14 -80 L14 -80 L22 -40 L18 -4 L-18 -4 L-22 -40 Z"/>
    <path d="M-10 -6 L-14 2 L-4 2 L-2 -6 Z M10 -6 L14 2 L4 2 L2 -6 Z"/>
    <line x1="-34" y1="-62" x2="44" y2="-38" stroke="#04090f" stroke-width="3.2" stroke-linecap="round"/>
    <line x1="18" y1="-45" x2="44" y2="-38" stroke="#2a375a" stroke-width="3.2" stroke-linecap="round"/>
    <path fill="#6a86e8" opacity=".85">
      <animate attributeName="d" dur="3s" repeatCount="indefinite"
        values="M-8 -78 C-30 -80 -50 -74 -72 -82 C-60 -70 -40 -68 -10 -70 Z;
                M-8 -78 C-30 -86 -52 -86 -76 -76 C-58 -66 -40 -72 -10 -70 Z;
                M-8 -78 C-30 -80 -50 -74 -72 -82 C-60 -70 -40 -68 -10 -70 Z"/>
    </path>
  </g>

  <!-- galhos de sakura -->
  <g>
    <animateTransform attributeName="transform" type="rotate" values="0 -20 40;1.2 -20 40;0 -20 40" dur="7s" repeatCount="indefinite"/>
    <path d="{main}" fill="none" stroke="#0f141d" stroke-width="9" stroke-linecap="round"/>
    {''.join(f'<path d="{d}" fill="none" stroke="#0f141d" stroke-width="4.5" stroke-linecap="round"/>' for d in sub)}
    {blossoms}
  </g>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="0 1300 18;-1.4 1300 18;0 1300 18" dur="8s" repeatCount="indefinite"/>
    <path d="{r_main}" fill="none" stroke="#0f141d" stroke-width="7" stroke-linecap="round"/>
    <path d="M1200 30 C1192 18 1186 8 1180 0" fill="none" stroke="#0f141d" stroke-width="3.5" stroke-linecap="round"/>
    {r_blossoms}
  </g>

  <!-- nome -->
  <g text-anchor="middle">
    <text x="640" y="78" font-family="{JP}" font-size="19" letter-spacing="12" fill="#aabbf7" opacity=".9">ディエゴ・ソウザ</text>
    <text x="640" y="156" font-family="{SERIF}" font-size="74" font-weight="600" letter-spacing="6" fill="url(#title)" filter="url(#glow)">Diego S. Souza</text>
    <line x1="480" y1="184" x2="800" y2="184" stroke="#aabbf7" stroke-width="1" opacity=".6"/>
    <use href="#flower" fill="#aabbf7" transform="translate(640 184) scale(.7)"/>
    <text x="640" y="220" font-family="{SANS}" font-size="16" letter-spacing="5" fill="#dbe1f3">DESENVOLVEDOR FULL STACK  ·  IA  ·  BRASIL</text>
  </g>

  <g>{falling_petals(rng, 34, W, H)}</g>
</svg>
"""
    (OUT / "banner.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------- árvore
def tree():
    rng = random.Random(21)
    W, H = 1200, 520
    branches, tips = [], []

    def grow(x, y, ang, length, width, depth):
        x2 = x + math.cos(ang) * length
        y2 = y - math.sin(ang) * length
        bend = rng.uniform(-0.25, 0.25) * length
        cx = (x + x2) / 2 + math.cos(ang + math.pi / 2) * bend
        cy = (y + y2) / 2 - math.sin(ang + math.pi / 2) * bend
        branches.append((f"M{f(x)} {f(y)} Q{f(cx)} {f(cy)} {f(x2)} {f(y2)}", width))
        if depth == 0 or length < 18:
            tips.append((x2, y2))
            return
        if depth <= 2:
            tips.append((x2, y2))
        n = 2 if depth > 3 else rng.choice([2, 3])
        spread = rng.uniform(0.75, 1.0) if depth >= 7 else rng.uniform(0.5, 0.8)
        for i in range(n):
            a = ang + spread * (i - (n - 1) / 2) * 1.1 + rng.uniform(-0.2, 0.2)
            # mantém a copa larga e arredondada
            a = max(0.12, min(math.pi - 0.12, a))
            grow(x2, y2, a, length * rng.uniform(0.7, 0.8) * (1.15 if depth >= 7 else 1), width * 0.68, depth - 1)

    grow(600, 478, math.pi / 2 + 0.03, 105, 40, 8)

    canopy = []
    for (x, y) in tips:
        for _ in range(rng.randint(5, 8)):
            cx, cy = x + rng.gauss(0, 18), y + rng.gauss(0, 14)
            canopy.append(
                f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{rng.uniform(5, 12):.1f}" '
                f'fill="{rng.choice(PINKS[1:])}" opacity="{rng.uniform(.7, .95):.2f}"/>'
            )
    flowers = []
    for (x, y) in rng.sample(tips, min(len(tips), 220)):
        flowers.append(
            f'<use href="#flower" fill="{rng.choice(PINKS[:4])}" '
            f'transform="translate({f(x + rng.gauss(0, 14))} {f(y + rng.gauss(0, 12))}) '
            f'rotate({rng.randint(0, 72)}) scale({rng.uniform(.5, .95):.2f})"/>'
        )
    ground_petals = "".join(
        f'<use href="#petal" fill="{rng.choice(PINKS)}" opacity="{rng.uniform(.5, .9):.2f}" '
        f'transform="translate({f(rng.uniform(80, 1120))} {f(rng.uniform(470, 515))}) '
        f'rotate({rng.randint(0, 360)}) scale({rng.uniform(.4, .8):.2f}) scale(1 .5)"/>'
        for _ in range(110)
    )
    fireflies = "".join(
        f'<circle cx="{f(rng.uniform(100, 1100))}" cy="{f(rng.uniform(260, 460))}" r="2" fill="#ffe9a8">'
        f'<animate attributeName="opacity" values="0;.9;0" dur="{rng.uniform(3, 6):.1f}s" '
        f'begin="{-rng.uniform(0, 6):.1f}s" repeatCount="indefinite"/>'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;{rng.randint(-20, 20)} {rng.randint(-25, -5)};0 0" '
        f'dur="{rng.uniform(6, 10):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(16)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Cerejeira">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#081420"/>
      <stop offset=".6" stop-color="#172c45"/>
      <stop offset="1" stop-color="#3a4a6e"/>
    </linearGradient>
    <radialGradient id="moon2" cx=".45" cy=".4" r=".7">
      <stop offset="0" stop-color="#fafbff"/><stop offset="1" stop-color="#c1cdf6"/>
    </radialGradient>
    <radialGradient id="halo2">
      <stop offset="0" stop-color="#d1dbff" stop-opacity=".5"/>
      <stop offset="1" stop-color="#d1dbff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bark" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#161c2a"/><stop offset=".5" stop-color="#22293d"/><stop offset="1" stop-color="#0f131e"/>
    </linearGradient>
    <filter id="bloom" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="40"/></filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    {petal_defs()}
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <g>{stars(rng, 90, W, 260)}</g>
    <circle cx="600" cy="210" r="210" fill="url(#halo2)"/>
    <circle cx="600" cy="210" r="120" fill="url(#moon2)" opacity=".95"/>
    <path d="M0 470 C200 440 400 452 600 448 C800 444 1000 440 1200 462 L1200 520 L0 520 Z" fill="#0b1622"/>

    <!-- lanternas de pedra -->
    <g fill="#070f18">
      <g transform="translate(250 470)">
        <rect x="-6" y="-46" width="12" height="46"/><path d="M-24 -46 L24 -46 L14 -58 L-14 -58 Z"/>
        <rect x="-14" y="-78" width="28" height="20"/><path d="M-28 -78 L0 -96 L28 -78 Z"/><circle cy="-100" r="5"/>
        <rect x="-7" y="-74" width="14" height="12" fill="#ffcf8a"><animate attributeName="opacity" values=".7;1;.75;.95;.7" dur="3s" repeatCount="indefinite"/></rect>
      </g>
      <g transform="translate(950 466)">
        <rect x="-6" y="-46" width="12" height="46"/><path d="M-24 -46 L24 -46 L14 -58 L-14 -58 Z"/>
        <rect x="-14" y="-78" width="28" height="20"/><path d="M-28 -78 L0 -96 L28 -78 Z"/><circle cy="-100" r="5"/>
        <rect x="-7" y="-74" width="14" height="12" fill="#ffcf8a"><animate attributeName="opacity" values=".8;.65;1;.75;.8" dur="3.4s" repeatCount="indefinite"/></rect>
      </g>
    </g>

    <g transform="translate(600 478) scale(.84) translate(-600 -478)"><g>
      <animateTransform attributeName="transform" type="rotate" values="0 600 470;.6 600 470;0 600 470;-.5 600 470;0 600 470" dur="10s" repeatCount="indefinite"/>
      {''.join(f'<path d="{d}" fill="none" stroke="url(#bark)" stroke-width="{w:.1f}" stroke-linecap="round"/>' for d, w in branches)}
      <ellipse cx="600" cy="170" rx="360" ry="130" fill="#a6b8f4" opacity=".22" filter="url(#bloom)"/>
      {''.join(canopy)}
      {''.join(flowers)}
    </g></g>
    {ground_petals}
    {fireflies}
    {falling_petals(rng, 40, W, H, scale=(.5, 1.0), dur=(8, 14))}
  </g>
</svg>
"""
    (OUT / "sakura-tree.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------- divisória
def divider():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 44" width="800" height="44">
  <defs>
    <linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#6a86e8" stop-opacity="0"/><stop offset="1" stop-color="#6a86e8"/></linearGradient>
    <linearGradient id="r" x1="1" x2="0"><stop offset="0" stop-color="#6a86e8" stop-opacity="0"/><stop offset="1" stop-color="#6a86e8"/></linearGradient>
    {petal_defs()}
  </defs>
  <rect x="120" y="21.5" width="240" height="1.4" fill="url(#l)"/>
  <rect x="440" y="21.5" width="240" height="1.4" fill="url(#r)"/>
  <use href="#petal" fill="#9baef1" transform="translate(372 22) rotate(-90) scale(.55)"/>
  <use href="#petal" fill="#9baef1" transform="translate(428 22) rotate(90) scale(.55)"/>
  <g transform="translate(400 22)">
    <use href="#flower" fill="#a6b8f4" transform="scale(.95)">
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="18s" repeatCount="indefinite" additive="sum"/>
    </use>
  </g>
</svg>
"""
    (OUT / "divider.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------- títulos
SECTIONS = {
    "sobre": ("Sobre Mim", "自己紹介"),
    "foco": ("Foco Atual", "現在"),
    "tech": ("Tecnologias", "技術"),
    "projetos": ("Projetos", "作品"),
    "stats": ("Estatísticas", "統計"),
    "atividade": ("Atividade", "活動"),
    "sakura": ("Cerejeira", "桜"),
    "estudos": ("Estudando Agora", "学習中"),
    "filosofia": ("Filosofia", "武士道"),
}


def titles():
    for key, (pt, jp) in SECTIONS.items():
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 110" width="800" height="110" role="img" aria-label="{escape(pt)}">
  <defs>
    <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#5776d9"/><stop offset=".5" stop-color="#7e98ee"/><stop offset="1" stop-color="#6b94d6"/></linearGradient>
    {petal_defs()}
  </defs>
  <text x="400" y="88" text-anchor="middle" font-family="{JP}" font-size="84" fill="#6a86e8" opacity=".13">{jp}</text>
  <text x="400" y="62" text-anchor="middle" font-family="{SERIF}" font-size="40" font-weight="600" letter-spacing="3" fill="url(#g)">{escape(pt)}</text>
  <use href="#flower" fill="#9baef1" transform="translate({400 - 30 - len(pt) * 11.5} 50) scale(.55)"/>
  <use href="#flower" fill="#9baef1" transform="translate({400 + 30 + len(pt) * 11.5} 50) scale(.55)"/>
  <text x="400" y="96" text-anchor="middle" font-family="{JP}" font-size="15" letter-spacing="8" fill="#6b82c8">{jp}</text>
</svg>
"""
        (OUT / f"title-{key}.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------- terminal
def terminal():
    P = '<tspan fill="#aabbf7">diego</tspan><tspan fill="#8b949e">@</tspan><tspan fill="#a6c8f2">sakura</tspan><tspan fill="#8b949e">:~$ </tspan>'
    lines = [
        (P + '<tspan fill="#e6edf3">whoami</tspan>', 0.6),
        ('<tspan fill="#d6dfff" font-weight="700">Diego S. Souza</tspan><tspan fill="#8b949e"> — desenvolvedor full stack · Brasil</tspan>', 0.3),
        ("", 0),
        (P + '<tspan fill="#e6edf3">cat sobre.txt</tspan>', 0.6),
        ('<tspan fill="#6a86e8">❀ </tspan><tspan fill="#e6edf3">Construo sistemas web de ponta a ponta: API, banco de dados e interface</tspan>', 0.5),
        ('<tspan fill="#6a86e8">❀ </tspan><tspan fill="#e6edf3">Faço sistemas de gestão de verdade — vendas, estoque, e-commerce</tspan>', 0.5),
        ('<tspan fill="#6a86e8">❀ </tspan><tspan fill="#e6edf3">Estudo IA aplicada: GANs, dados sintéticos e PyTorch</tspan>', 0.5),
        ('<tspan fill="#6a86e8">❀ </tspan><tspan fill="#e6edf3">Guardo tudo que aprendo num cofre do Obsidian (segundo cérebro)</tspan>', 0.5),
        ("", 0),
        (P + '<tspan fill="#e6edf3">echo $LEMA</tspan>', 0.6),
        ('<tspan fill="#a5d6ff">"Supere quem você foi ontem."</tspan><tspan fill="#aabbf7" font-family="' + JP.replace("'", "&apos;") + '">  昨日の自分を超える</tspan>', 0.4),
    ]
    W, top, lh = 880, 74, 26
    H = top + lh * len(lines) + 46
    body, t = [], 0.4
    for i, (content, dur) in enumerate(lines):
        y = top + i * lh
        if not content:
            continue
        body.append(
            f'<clipPath id="c{i}"><rect x="28" y="{y - 19}" width="0" height="{lh}">'
            f'<animate attributeName="width" from="0" to="{W - 56}" begin="{t:.1f}s" dur="{dur:.1f}s" fill="freeze"/>'
            f"</rect></clipPath>"
            f'<text x="32" y="{y}" clip-path="url(#c{i})">{content}</text>'
        )
        t += dur + 0.25
    cy = top + lh * len(lines)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sobre mim">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#101f30"/></linearGradient>
    <linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="#6a86e8"/><stop offset="1" stop-color="#6b9bd6"/></linearGradient>
  </defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#bg)" stroke="url(#bd)" stroke-opacity=".7"/>
  <path d="M1 15 Q1 1 15 1 L{W - 15} 1 Q{W - 1} 1 {W - 1} 15 L{W - 1} 40 L1 40 Z" fill="#161b22"/>
  <circle cx="26" cy="21" r="6.5" fill="#ff5f57"/><circle cx="48" cy="21" r="6.5" fill="#febc2e"/><circle cx="70" cy="21" r="6.5" fill="#28c840"/>
  <text x="{W / 2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8b949e">diego@sakura — zsh — 桜</text>
  <g font-family="{MONO}" font-size="15.5" xml:space="preserve">
    {''.join(body)}
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.1f}s" dur=".01s" fill="freeze"/>
      <text x="32" y="{cy}">{P}</text>
      <rect x="{32 + 16 * 9.35:.0f}" y="{cy - 15}" width="9" height="19" fill="#aabbf7">
        <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/>
      </rect>
    </g>
  </g>
</svg>
"""
    (OUT / "terminal.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------- cards de projeto
LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Markdown": "#ffffff",
}


def card(slug, title, jp, desc_lines, tags, lang, icon):
    W, H = 430, 190
    tag_svg, x = [], 24
    for tg in tags:
        w = len(tg) * 7.4 + 20
        tag_svg.append(
            f'<rect x="{x:.0f}" y="138" width="{w:.0f}" height="24" rx="12" fill="#6a86e8" fill-opacity=".13" stroke="#6a86e8" stroke-opacity=".45"/>'
            f'<text x="{x + w / 2:.0f}" y="154.5" text-anchor="middle" font-size="12" fill="#c2d0ff">{escape(tg)}</text>'
        )
        x += w + 8
    desc = "".join(
        f'<text x="24" y="{86 + i * 21}" font-size="14" fill="#c9d1d9">{escape(l)}</text>' for i, l in enumerate(desc_lines)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(title)}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#122233"/></linearGradient>
    <linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="#6a86e8"/><stop offset="1" stop-color="#6b9bd6"/></linearGradient>
    {petal_defs()}
  </defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#bg)" stroke="url(#bd)" stroke-opacity=".75"/>
  <text x="{W - 20}" y="{H - 22}" text-anchor="end" font-family="{JP}" font-size="64" fill="#6a86e8" opacity=".08">{jp}</text>
  <use href="#flower" fill="#9baef1" opacity=".9" transform="translate({W - 30} 30) scale(.75)">
    <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="20s" repeatCount="indefinite" additive="sum"/>
  </use>
  <g font-family="{SANS}">
    <text x="24" y="44" font-size="22">{icon}</text>
    <text x="56" y="44" font-size="20" font-weight="700" fill="#d6dfff">{escape(title)}</text>
    <text x="57" y="61" font-size="11.5" letter-spacing="1.5" fill="#8b949e">github.com/Di20232/{escape(slug)}</text>
    {desc}
    {''.join(tag_svg)}
    <circle cx="{W - 98}" cy="{H - 16}" r="5" fill="{LANG_COLORS[lang]}"/>
    <text x="{W - 88}" y="{H - 12}" font-size="12" fill="#8b949e">{lang}</text>
  </g>
</svg>
"""
    (OUT / f"card-{slug}.svg").write_text(svg, encoding="utf-8")


def cards():
    card("byteShop", "ByteShop", "店",
         ["E-commerce de peças de PC e periféricos:", "catálogo, carrinho, checkout, login com JWT."],
         ["FastAPI", "React", "TypeScript", "SQLite", "Tailwind"], "Python", "🛒")
    card("mercadinho-seu-joao-2", "Contro Vend", "商",
         ["Vendas e estoque para pequeno comércio: caixa,", "previsão de esgotamento e alertas de validade."],
         ["Node.js", "Express", "PostgreSQL", "Prisma"], "JavaScript", "🏪")
    card("obsidian_v1", "Cofre Obsidian", "脳",
         ["Meu segundo cérebro: notas de Python, IA,", "GANs, segurança web e bancos de dados."],
         ["Obsidian", "Markdown", "Knowledge Base"], "Markdown", "🧠")
    card("exercises_python", "Exercícios Python", "練",
         ["Cada exercício em duas versões (dados x objetos)", "e um script que prova que as saídas são iguais."],
         ["Python", "POO", "Testes"], "Python", "🐍")


banner()
tree()
divider()
titles()
terminal()
cards()
print("ok", sorted(p.name for p in OUT.iterdir()))

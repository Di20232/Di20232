"""Gera os SVGs do perfil no tema hacker (azul em degradê).

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

BG0, BG1 = "#020611", "#071634"
CYAN, SKY, BLUE, INDIGO, ICE = "#22d3ee", "#38bdf8", "#3b82f6", "#6366f1", "#e0f7ff"
TEXT, MUTED = "#c9d6ea", "#6f86ad"
MONO = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, 'DejaVu Sans Mono', monospace"

GRAD = f"""<linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{BLUE}"/><stop offset="1" stop-color="{INDIGO}"/>
    </linearGradient>"""


def f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def lerp(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(a[i] + (b[i] - a[i]) * t):02x}" for i in range(3))


def grad_at(t):
    return lerp(CYAN, BLUE, t * 2) if t < 0.5 else lerp(BLUE, INDIGO, (t - 0.5) * 2)


CHARS = "01010101ABCDEF23456789<>/{}[]();=+*#$%&"


# --------------------------------------------------------------------------- banner
def banner():
    rng = random.Random(42)
    W, H, STEP, LH = 1280, 400, 20, 18
    cols = []
    for c in range(W // STEP + 1):
        x = c * STEP + 4
        n = rng.randint(7, 17)
        speed = rng.uniform(55, 130)
        dur = (H + n * LH) / speed
        base = grad_at(x / W)
        chars = []
        for i in range(n):
            ch = rng.choice(CHARS).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if i == n - 1:
                fill, op = ICE, 1
            else:
                fill, op = base, 0.1 + 0.62 * (i / (n - 1)) ** 1.7
            chars.append(f'<tspan x="{x}" dy="{LH}" fill="{fill}" fill-opacity="{op:.2f}">{ch}</tspan>')
        cols.append(
            f'<g><animateTransform attributeName="transform" type="translate" from="0 {-n * LH}" to="0 {H}" '
            f'dur="{dur:.1f}s" begin="{-rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/>'
            f'<text y="0">{"".join(chars)}</text></g>'
        )

    glitch = lambda color, vals, op: (
        f'<text x="640" y="214" text-anchor="middle" font-size="72" font-weight="700" fill="{color}" opacity="{op}" '
        f'textLength="606" lengthAdjust="spacingAndGlyphs">Diego S. Souza'
        f'<animateTransform attributeName="transform" type="translate" values="{vals}" '
        f'keyTimes="0;.88;.9;.93;.96;1" dur="5s" repeatCount="indefinite"/></text>'
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Diego S. Souza — desenvolvedor full stack, IA e segurança web">
  <defs>
    {GRAD}
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="#04112b"/></linearGradient>
    <radialGradient id="dim" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{BG0}" stop-opacity=".92"/><stop offset=".55" stop-color="{BG0}" stop-opacity=".72"/><stop offset="1" stop-color="{BG0}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".28"/></pattern>
    <filter id="glow" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <g font-family="{MONO}" font-size="16">{''.join(cols)}</g>
    <ellipse cx="640" cy="205" rx="560" ry="150" fill="url(#dim)"/>
    <rect width="{W}" height="{H}" fill="url(#vig)"/>
    <rect width="{W}" height="{H}" fill="url(#scan)"/>

    <g font-family="{MONO}" text-anchor="middle">
      <text x="640" y="132" font-size="17" fill="{SKY}" letter-spacing="2">root@diego:~# whoami</text>
      {glitch(CYAN, "0 0;0 0;5 0;-4 1;0 0;0 0", .55)}
      {glitch(INDIGO, "0 0;0 0;-5 0;4 -1;0 0;0 0", .55)}
      <text x="640" y="214" font-size="72" font-weight="700" fill="url(#g)" filter="url(#glow)" textLength="606" lengthAdjust="spacingAndGlyphs">Diego S. Souza</text>
      <rect x="958" y="204" width="34" height="8" fill="{SKY}" filter="url(#glow)"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
      <text x="640" y="262" font-size="18" fill="{ICE}" letter-spacing="5">[ FULL STACK · IA · SEGURANÇA WEB ]</text>
    </g>

    <line x1="40" y1="352" x2="{W - 40}" y2="352" stroke="url(#g)" stroke-opacity=".55"/>
    <g font-family="{MONO}" font-size="13" fill="{MUTED}">
      <circle cx="46" cy="373" r="4.5" fill="{CYAN}"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></circle>
      <text x="58" y="378" fill="{SKY}">ONLINE</text>
      <text x="640" y="378" text-anchor="middle">acesso root concedido · conexão criptografada</text>
      <text x="{W - 40}" y="378" text-anchor="end">Brasil · UTC-3</text>
    </g>
    <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="url(#g)" stroke-width="2" stroke-opacity=".8"/>
  </g>
</svg>
"""
    (OUT / "banner.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------- divisória
def divider():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 36" width="800" height="36">
  <defs>
    <linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".25" stop-color="{CYAN}"/><stop offset=".6" stop-color="{BLUE}"/><stop offset="1" stop-color="{INDIGO}" stop-opacity="0"/></linearGradient>
    <filter id="gl" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <rect x="40" y="17.2" width="720" height="1.6" fill="url(#l)"/>
  <g fill="none" stroke="{SKY}" stroke-opacity=".7"><circle cx="160" cy="18" r="4"/><circle cx="640" cy="18" r="4"/></g>
  <path d="M400 8 L410 18 L400 28 L390 18Z" fill="none" stroke="{BLUE}" stroke-width="1.6"/>
  <circle cx="400" cy="18" r="2.6" fill="{ICE}"/>
  <g font-family="{MONO}" font-size="9" fill="{BLUE}" opacity=".7"><text x="300" y="14" text-anchor="end">0101</text><text x="500" y="14">1010</text></g>
  <circle r="3.2" cy="18" fill="{ICE}"><animate attributeName="cx" values="60;740" dur="4s" repeatCount="indefinite"/></circle>
  <circle r="7" cy="18" fill="{CYAN}" opacity=".55" filter="url(#gl)"><animate attributeName="cx" values="60;740" dur="4s" repeatCount="indefinite"/></circle>
</svg>
"""
    (OUT / "divider.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------- títulos
SECTIONS = {
    "sobre": ("01", "SOBRE_MIM", "quem sou eu"),
    "foco": ("02", "FOCO_ATUAL", "no que estou trabalhando"),
    "tech": ("03", "STACK", "ferramentas do dia a dia"),
    "projetos": ("04", "PROJETOS", "o que já construí"),
    "rede": ("05", "REDE", "tudo conectado"),
    "stats": ("06", "ESTATÍSTICAS", "números do GitHub"),
    "atividade": ("07", "ATIVIDADE", "commits e constância"),
    "estudos": ("08", "EM_ESTUDO", "aprendendo agora"),
    "manifesto": ("09", "MANIFESTO", "princípios"),
}


def titles():
    for key, (num, title, sub) in SECTIONS.items():
        label = f"[ {num} ] {title}"
        half = len(label) * 8.9 + 26
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 74" width="800" height="74" role="img" aria-label="{escape(title)}">
  <defs>
    {GRAD}
    <linearGradient id="ll" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
    <linearGradient id="lr" x1="0" x2="1"><stop offset="0" stop-color="{INDIGO}"/><stop offset="1" stop-color="{INDIGO}" stop-opacity="0"/></linearGradient>
    <filter id="gl" x="-10%" y="-60%" width="120%" height="220%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x="30" y="29" width="{400 - half - 30:.0f}" height="1.6" fill="url(#ll)"/>
  <rect x="{400 + half:.0f}" y="29" width="{400 - half - 30:.0f}" height="1.6" fill="url(#lr)"/>
  <path d="M{400 - half - 8:.0f} 22 v14 M{400 + half + 8:.0f} 22 v14" stroke="{SKY}" stroke-width="2"/>
  <text x="400" y="38" text-anchor="middle" font-family="{MONO}" font-size="25" font-weight="700" letter-spacing="1.5" fill="url(#g)" filter="url(#gl)">{escape(label)}</text>
  <text x="400" y="64" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">// {escape(sub)}<tspan fill="{SKY}">_<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></tspan></text>
</svg>
"""
        (OUT / f"title-{key}.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------- terminal
def terminal():
    P = f'<tspan fill="{SKY}">diego</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{INDIGO}">hacker</tspan><tspan fill="{MUTED}">:~$ </tspan>'
    PLUS = f'<tspan fill="{CYAN}">[+] </tspan>'
    lines = [
        (P + '<tspan fill="#e6edf3">whoami</tspan>', 0.6),
        (f'<tspan fill="{ICE}" font-weight="700">Diego S. Souza</tspan><tspan fill="{MUTED}"> — desenvolvedor full stack · Brasil</tspan>', 0.3),
        ("", 0),
        (P + '<tspan fill="#e6edf3">cat sobre.txt</tspan>', 0.6),
        (PLUS + f'<tspan fill="{TEXT}">Construo sistemas web de ponta a ponta: API, banco de dados e interface</tspan>', 0.5),
        (PLUS + f'<tspan fill="{TEXT}">Faço sistemas de gestão de verdade — vendas, estoque, e-commerce</tspan>', 0.5),
        (PLUS + f'<tspan fill="{TEXT}">Estudo IA aplicada: GANs, dados sintéticos e PyTorch</tspan>', 0.5),
        (PLUS + f'<tspan fill="{TEXT}">Levo segurança a sério: JWT, rate limit, validação e logs de auditoria</tspan>', 0.5),
        ("", 0),
        (P + '<tspan fill="#e6edf3">echo $LEMA</tspan>', 0.6),
        (f'<tspan fill="#a5d6ff">"Supere quem você foi ontem."</tspan>', 0.4),
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
    {GRAD}
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050b1a"/><stop offset="1" stop-color="#0a1a3a"/></linearGradient>
  </defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#bg)" stroke="url(#g)" stroke-opacity=".85" stroke-width="1.5"/>
  <path d="M1 15 Q1 1 15 1 L{W - 15} 1 Q{W - 1} 1 {W - 1} 15 L{W - 1} 40 L1 40 Z" fill="#0b1630"/>
  <circle cx="26" cy="21" r="6.5" fill="{CYAN}"/><circle cx="48" cy="21" r="6.5" fill="{BLUE}"/><circle cx="70" cy="21" r="6.5" fill="{INDIGO}"/>
  <text x="{W / 2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">diego@hacker — bash — 80×24</text>
  <g font-family="{MONO}" font-size="15.5" xml:space="preserve">
    {''.join(body)}
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.1f}s" dur=".01s" fill="freeze"/>
      <text x="32" y="{cy}">{P}</text>
      <rect x="{32 + 16 * 9.35:.0f}" y="{cy - 15}" width="9" height="19" fill="{SKY}">
        <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/>
      </rect>
    </g>
  </g>
</svg>
"""
    (OUT / "terminal.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------- cards de projeto
LANG_COLORS = {"Python": "#3572A5", "JavaScript": "#f1e05a", "Markdown": "#ffffff"}


def card(slug, title, desc_lines, tags, lang):
    W, H = 430, 196
    tag_svg, x = [], 24
    for tg in tags:
        w = len(tg) * 7.6 + 18
        tag_svg.append(
            f'<rect x="{x:.0f}" y="150" width="{w:.0f}" height="24" rx="5" fill="{BLUE}" fill-opacity=".13" stroke="{SKY}" stroke-opacity=".5"/>'
            f'<text x="{x + w / 2:.0f}" y="166" text-anchor="middle" font-size="12" fill="{ICE}">{escape(tg)}</text>'
        )
        x += w + 8
    desc = "".join(
        f'<text x="24" y="{114 + i * 20}" font-size="13.5" fill="{TEXT}">{escape(l)}</text>' for i, l in enumerate(desc_lines)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(title)}">
  <defs>
    {GRAD}
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050b1a"/><stop offset="1" stop-color="#0a1a3a"/></linearGradient>
  </defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="url(#bg)" stroke="url(#g)" stroke-width="1.5" stroke-opacity=".85"/>
  <path d="M1 13 Q1 1 13 1 L{W - 13} 1 Q{W - 1} 1 {W - 1} 13 L{W - 1} 32 L1 32 Z" fill="#0b1630"/>
  <circle cx="20" cy="17" r="4.5" fill="{CYAN}"/><circle cx="36" cy="17" r="4.5" fill="{BLUE}"/><circle cx="52" cy="17" r="4.5" fill="{INDIGO}"/>
  <text x="{W - 16}" y="21" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">~/projetos/{escape(slug)}</text>
  <g font-family="{MONO}">
    <text x="24" y="58" font-size="12" fill="{MUTED}">$ cat README.md</text>
    <text x="24" y="90" font-size="22" font-weight="700" fill="url(#g)">{escape(title)}</text>
    {desc}
    {''.join(tag_svg)}
    <circle cx="{W - 96}" cy="{H - 14}" r="4.5" fill="{LANG_COLORS[lang]}"/>
    <text x="{W - 86}" y="{H - 10}" font-size="12" fill="{MUTED}">{lang}</text>
  </g>
</svg>
"""
    (OUT / f"card-{slug}.svg").write_text(svg, encoding="utf-8")


def cards():
    card("byteShop", "ByteShop", ["E-commerce de peças de PC e periféricos:", "catálogo, carrinho, checkout, login com JWT."],
         ["FastAPI", "React", "TypeScript", "SQLite"], "Python")
    card("mercadinho-seu-joao-2", "Contro Vend", ["Vendas e estoque para pequeno comércio: caixa,", "previsão de esgotamento e alertas de validade."],
         ["Node.js", "Express", "PostgreSQL", "Prisma"], "JavaScript")
    card("obsidian_v1", "Cofre Obsidian", ["Meu segundo cérebro: notas de Python, IA,", "GANs, segurança web e bancos de dados."],
         ["Obsidian", "Markdown", "Knowledge Base"], "Markdown")
    card("exercises_python", "Exercícios Python", ["Cada exercício em duas versões (dados x objetos)", "e um script que prova que as saídas são iguais."],
         ["Python", "POO", "Testes"], "Python")


# --------------------------------------------------------------------------- rede
def rede():
    rng = random.Random(9)
    W, H = 1200, 420
    cx, cy = 600, 210
    labels = ["API", "DB", "UI", "IA", "GAN", "DOCKER", "JWT", "PYTORCH", "REACT", "FASTAPI", "NODE", "SQL"]
    nodes = []
    for i, lb in enumerate(labels):
        ang = i / len(labels) * 2 * math.pi + rng.uniform(-.12, .12)
        ring = 1.0 if i % 2 == 0 else 0.62
        nodes.append((cx + math.cos(ang) * 470 * ring + rng.uniform(-14, 14), cy + math.sin(ang) * 168 * ring + rng.uniform(-10, 10), lb))
    extra = [rng.uniform(0, 1) for _ in range(0)]
    edges = [(cx, cy, x, y) for x, y, _ in nodes]
    for i in range(len(nodes)):
        a, b = nodes[i], nodes[(i + 1) % len(nodes)]
        edges.append((a[0], a[1], b[0], b[1]))
    base = "".join(f'<line x1="{f(a)}" y1="{f(b)}" x2="{f(c)}" y2="{f(d)}"/>' for a, b, c, d in edges)
    packets = "".join(
        f'<line x1="{f(a)}" y1="{f(b)}" x2="{f(c)}" y2="{f(d)}" stroke-dasharray="7 {int(math.hypot(c - a, d - b))}" stroke-dashoffset="0">'
        f'<animate attributeName="stroke-dashoffset" from="{int(math.hypot(c - a, d - b)) + 7}" to="0" dur="{rng.uniform(2.2, 4.6):.1f}s" begin="{-rng.uniform(0, 4):.1f}s" repeatCount="indefinite"/></line>'
        for a, b, c, d in edges
    )
    pts = []
    for i, (x, y, lb) in enumerate(nodes):
        d = rng.uniform(2.2, 3.8)
        anchor, dx = ("start", 14) if x >= cx else ("end", -14)
        pts.append(
            f'<g><circle cx="{f(x)}" cy="{f(y)}" r="6" fill="none" stroke="{SKY}"><animate attributeName="r" values="6;22" dur="{d:.1f}s" begin="{-rng.uniform(0, d):.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".7;0" dur="{d:.1f}s" begin="{-rng.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="6.5" fill="{BG0}" stroke="{grad_at(i / len(nodes))}" stroke-width="2.2"/>'
            f'<text x="{f(x + dx)}" y="{f(y + 4.5)}" text-anchor="{anchor}" font-family="{MONO}" font-size="13" fill="{ICE}" letter-spacing="1">{lb}</text></g>'
        )
    hexpts = " ".join(f"{f(cx + 36 * math.cos(math.pi / 3 * k + math.pi / 6))},{f(cy + 36 * math.sin(math.pi / 3 * k + math.pi / 6))}" for k in range(6))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.3"/>' for x in range(30, W, 40) for y in range(30, H, 40))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Rede de tecnologias conectadas">
  <defs>
    {GRAD}
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#030816"/><stop offset="1" stop-color="#0a1a3a"/></linearGradient>
    <radialGradient id="core"><stop offset="0" stop-color="{BLUE}" stop-opacity=".55"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
    <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".85" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{ICE}" stop-opacity=".5"/></linearGradient>
    <clipPath id="fr"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#fr)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <g fill="{BLUE}" opacity=".25">{dots}</g>
    <circle cx="{cx}" cy="{cy}" r="230" fill="url(#core)"/>
    <rect x="-160" y="0" width="160" height="{H}" fill="url(#sweep)"><animate attributeName="x" values="-160;{W}" dur="7s" repeatCount="indefinite"/></rect>
    <g stroke="{BLUE}" stroke-opacity=".38" stroke-width="1.2">{base}</g>
    <g stroke="{ICE}" stroke-width="3" stroke-linecap="round">{packets}</g>
    {''.join(pts)}
    <polygon points="{hexpts}" fill="{BG0}" stroke="url(#g)" stroke-width="3">
      <animate attributeName="stroke-opacity" values="1;.55;1" dur="2.4s" repeatCount="indefinite"/></polygon>
    <polygon points="{hexpts}" fill="none" stroke="{CYAN}" stroke-opacity=".5" transform="translate({cx} {cy}) scale(1.35) translate({-cx} {-cy})"/>
    <text x="{cx}" y="{cy + 10}" text-anchor="middle" font-family="{MONO}" font-size="30" font-weight="700" fill="url(#g)">D</text>
    <g font-family="{MONO}" font-size="12" fill="{MUTED}"><text x="26" y="{H - 22}">nós: {len(nodes) + 1}</text><text x="{W - 26}" y="{H - 22}" text-anchor="end">tráfego: criptografado</text></g>
    <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="url(#g)" stroke-opacity=".6" stroke-width="1.5"/>
  </g>
</svg>
"""
    (OUT / "rede.svg").write_text(svg, encoding="utf-8")


banner()
divider()
titles()
terminal()
cards()
rede()
print("ok", sorted(p.name for p in OUT.iterdir()))

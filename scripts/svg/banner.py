from svg.document import SHARED_KEYFRAMES, background, escapeText, svgText, windowDots, wrapSvg
from svg.theme import ACCENTS, BORDER, FONT_MONO, FONT_SANS, MONO_CHAR_RATIO, MUTED, PANEL, TEXT

WIDTH = 1000
HEIGHT = 340
PANEL_Y = 24
PANEL_WIDTH = 468
PANEL_HEIGHT = 220
TERMINAL_X = 24
VIEWPORT_X = 508
FONT_SIZE = 15
CHAR_WIDTH = round(FONT_SIZE * MONO_CHAR_RATIO, 2)
LINE_X = 48
TEXT_X = round(LINE_X + 2 * CHAR_WIDTH, 2)
FIRST_LINE_Y = 90
LINE_HEIGHT = 30
TYPE_SECONDS_PER_CHAR = 0.07
CURSOR_START = 3.9
SYS, SYS_ALT = ACCENTS['sys']
MEDIA, MEDIA_ALT = ACCENTS['media']

# (prompt, texto, color, segundo de inicio, si se escribe carácter a carácter)
TERMINAL_LINES = (
  ('$', 'whoami', TEXT, 0.4, True),
  ('>', 'software_engineer', SYS, 1.4, False),
  ('$', './build --prod', TEXT, 2.0, True),
  ('✓', 'build passed · multimedia module loaded', SYS_ALT, 3.3, False),
)

# Octaedro low-poly ya proyectado; las aristas traseras van punteadas.
SHAPE_POINTS = {
  'top': (742, 64), 'bottom': (742, 206), 'left': (672, 138),
  'right': (812, 138), 'front': (722, 156), 'back': (768, 120),
}
BACK_EDGES = (('top', 'back'), ('back', 'right'), ('back', 'left'), ('back', 'bottom'))
# (vértices, color, opacidad final): la luz viene de arriba a la derecha.
FRONT_FACES = (
  (('top', 'left', 'front'), MEDIA, 0.55),
  (('top', 'front', 'right'), MEDIA_ALT, 0.75),
  (('bottom', 'front', 'left'), MEDIA, 0.3),
  (('bottom', 'right', 'front'), MEDIA_ALT, 0.45),
)

BANNER_KEYFRAMES = (
  '@keyframes draw { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }'
  '@keyframes shade { from { fill-opacity: 0; } }'
  '@keyframes glow { 50% { opacity: 0.7; } }'
)


def renderBanner(profile):
  terminal, typingCss = renderTerminal()
  content = background(WIDTH, HEIGHT) + renderSplit() + terminal + renderViewport() + renderIdentity(profile)
  title = f"{profile['name']} — {profile['title']}"
  return wrapSvg(WIDTH, HEIGHT, title, content, SHARED_KEYFRAMES + BANNER_KEYFRAMES + typingCss)


def panel(x, title):
  return (
    f'<rect x="{x}" y="{PANEL_Y}" width="{PANEL_WIDTH}" height="{PANEL_HEIGHT}" rx="12" '
    f'fill="{PANEL}" stroke="{BORDER}"/>'
    + svgText(x + PANEL_WIDTH / 2, PANEL_Y + 24, title, MUTED, 12, anchor='middle')
  )


def renderTerminal():
  rendered = [renderTerminalLine(index, line) for index, line in enumerate(TERMINAL_LINES)]
  markup = ''.join(lineMarkup for lineMarkup, _ in rendered)
  css = ''.join(lineCss for _, lineCss in rendered)
  chrome = panel(TERMINAL_X, 'nicolas@cali: ~') + windowDots(TERMINAL_X + 22, PANEL_Y + 20)
  return chrome + markup + renderCursor(), css


def renderTerminalLine(index, line):
  prompt, text, color, start, typed = line
  y = FIRST_LINE_Y + LINE_HEIGHT * index
  promptColor = MUTED if prompt == '>' else SYS_ALT
  markup = (
    f'<g style="animation: appear 0.1s linear {start}s both">'
    + svgText(LINE_X, y, prompt, promptColor, FONT_SIZE)
    + svgText(TEXT_X, y, text, color, FONT_SIZE)
  )
  if not typed:
    return markup + '</g>', ''
  return markup + typingCover(index, text, y, start) + '</g>', typingKeyframes(index, text)


def typingWidth(text):
  return round(len(text) * CHAR_WIDTH + 4, 1)


def typingCover(index, text, y, start):
  # Un rectángulo del color del panel tapa el texto y se corre a saltos, uno por
  # carácter; su posición base (ya corrido) es el fotograma final sin animación.
  width = typingWidth(text)
  duration = round(len(text) * TYPE_SECONDS_PER_CHAR, 2)
  return (
    f'<rect x="{TEXT_X}" y="{y - FONT_SIZE}" width="{width}" height="{FONT_SIZE + 6}" fill="{PANEL}" '
    f'transform="translate({width} 0)" '
    f'style="animation: type-{index} {duration}s steps({len(text)}) {start}s both"/>'
  )


def typingKeyframes(index, text):
  width = typingWidth(text)
  return (
    f'@keyframes type-{index} {{ from {{ transform: translateX(0); }} '
    f'to {{ transform: translateX({width}px); }} }}'
  )


def renderCursor():
  y = FIRST_LINE_Y + LINE_HEIGHT * len(TERMINAL_LINES)
  return (
    f'<g style="animation: appear 0.1s linear {CURSOR_START}s both">'
    + svgText(LINE_X, y, '$', SYS_ALT, FONT_SIZE)
    + f'<rect x="{TEXT_X}" y="{y - FONT_SIZE + 2}" width="{CHAR_WIDTH}" height="{FONT_SIZE + 2}" fill="{SYS}" '
    f'style="animation: blink 1s steps(1) {CURSOR_START + 0.5}s infinite"/></g>'
  )


def renderViewport():
  faces = ''.join(renderFace(index, face) for index, face in enumerate(FRONT_FACES))
  return panel(VIEWPORT_X, '▶ viewport · render') + renderBackEdges() + faces + renderProgress()


def renderBackEdges():
  return ''.join(
    f'<line x1="{SHAPE_POINTS[start][0]}" y1="{SHAPE_POINTS[start][1]}" '
    f'x2="{SHAPE_POINTS[end][0]}" y2="{SHAPE_POINTS[end][1]}" stroke="{MEDIA}" '
    'stroke-opacity="0.45" stroke-dasharray="3 4" style="animation: appear 0.8s ease 0.2s both"/>'
    for start, end in BACK_EDGES
  )


def renderFace(index, face):
  # pathLength="1" normaliza el perímetro para animar el trazo sin medir cada cara.
  corners, color, opacity = face
  points = ' '.join(f'{SHAPE_POINTS[corner][0]},{SHAPE_POINTS[corner][1]}' for corner in corners)
  drawStart = round(0.4 + 0.2 * index, 2)
  shadeStart = round(1.8 + 0.35 * index, 2)
  return (
    f'<polygon points="{points}" fill="{color}" fill-opacity="{opacity}" stroke="{MEDIA}" '
    'stroke-width="1.5" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" '
    f'style="animation: draw 1s ease {drawStart}s both, shade 0.6s ease {shadeStart}s both"/>'
  )


def renderProgress():
  x = VIEWPORT_X + 40
  y = 226
  width = PANEL_WIDTH - 80
  return (
    svgText(x, y - 8, 'render', MUTED, 11)
    + svgText(x + width, y - 8, '100%', MEDIA_ALT, 11, anchor='end', style='animation: appear 0.3s ease 4s both')
    + f'<rect x="{x}" y="{y}" width="{width}" height="4" rx="2" fill="{BORDER}"/>'
    + f'<rect class="grow" x="{x}" y="{y}" width="{width}" height="4" rx="2" fill="{MEDIA_ALT}" '
    'style="animation: grow 2.4s ease-in-out 1.6s both"/>'
  )


def renderSplit():
  x = WIDTH / 2
  top = PANEL_Y
  bottom = PANEL_Y + PANEL_HEIGHT
  line = f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="url(#split)" stroke-linecap="round"'
  # Una línea vertical tiene caja de ancho cero: el degradado necesita userSpaceOnUse.
  gradient = (
    f'<defs><linearGradient id="split" gradientUnits="userSpaceOnUse" x1="{x}" y1="{top}" x2="{x}" y2="{bottom}">'
    f'<stop offset="0" stop-color="{SYS}"/><stop offset="1" stop-color="{MEDIA}"/></linearGradient></defs>'
  )
  return (
    gradient
    + f'{line} stroke-width="8" opacity="0.25" style="animation: glow 3s ease-in-out infinite"/>'
    + f'{line} stroke-width="2"/>'
  )


def renderIdentity(profile):
  center = WIDTH / 2
  name = svgText(center, 292, profile['name'].upper(), TEXT, 34, font=FONT_SANS, weight=700, anchor='middle')
  subtitle = (
    f'<text x="{center}" y="322" font-family="{FONT_MONO}" font-size="15" text-anchor="middle">'
    f'<tspan fill="{SYS}">[SYS]</tspan>'
    f'<tspan fill="{MUTED}"> {escapeText(profile["title"])} </tspan>'
    f'<tspan fill="{MEDIA}">[MEDIA]</tspan></text>'
  )
  return name + subtitle

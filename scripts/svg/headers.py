from svg.document import SHARED_KEYFRAMES, background, escapeText, svgText, wrapSvg
from svg.theme import ACCENTS, BORDER, FONT_MONO, FONT_SANS, MUTED, TEXT

WIDTH = 1000
HEIGHT = 88
CONTENT_LEFT = 28
CONTENT_RIGHT = WIDTH - 28
HEADERS = {
  'sys': {'label': 'PRIMARY OS', 'title': 'Software Systems', 'detail': '/mnt/software · mounted'},
  'media': {'label': 'SECOND PARTITION', 'title': 'Multimedia', 'detail': '/mnt/multimedia · rendering'},
}
TRACK_WIDTH = 340
TRACK_X = CONTENT_RIGHT - TRACK_WIDTH
TRACK_Y = 26
SWEEP_KEYFRAMES = (
  f'@keyframes sweep {{ from {{ transform: translateX(-{TRACK_WIDTH}px); }} '
  'to { transform: translateX(0); } }'
)


def renderHeader(category):
  header = HEADERS[category]
  accent, accentAlt = ACCENTS[category]
  content = background(WIDTH, HEIGHT, 12) + heading(header, accent)
  title = f"{header['label']} — {header['title']}"
  if category == 'sys':
    return wrapSvg(WIDTH, HEIGHT, title, content + bootStatus(accentAlt))
  return wrapSvg(WIDTH, HEIGHT, title, content + timeline(accent, accentAlt), SHARED_KEYFRAMES + SWEEP_KEYFRAMES)


def heading(header, accent):
  return (
    f'<text x="{CONTENT_LEFT}" y="44" font-family="{FONT_MONO}" font-size="24" font-weight="700">'
    f'<tspan fill="{accent}">▸ {escapeText(header["label"])}</tspan>'
    f'<tspan fill="{TEXT}" font-family="{FONT_SANS}" font-weight="400"> — {escapeText(header["title"])}</tspan>'
    '</text>'
    + svgText(CONTENT_LEFT, 70, header['detail'], MUTED, 13)
  )


def bootStatus(color):
  return (
    svgText(CONTENT_RIGHT, 44, '[ OK ]', color, 16, anchor='end', style='animation: appear 0.3s ease 1.1s both')
    + f'<rect class="grow" x="{CONTENT_LEFT}" y="78" width="{CONTENT_RIGHT - CONTENT_LEFT}" height="2" '
    f'fill="{color}" opacity="0.6" style="animation: grow 1s ease-out 0.2s both"/>'
  )


def timeline(accent, accentAlt):
  ticks = ''.join(
    f'<line x1="{TRACK_X + step}" y1="{TRACK_Y}" x2="{TRACK_X + step}" '
    f'y2="{TRACK_Y + (8 if step % 100 == 0 else 4)}" stroke="{MUTED}"/>'
    for step in range(0, TRACK_WIDTH + 1, 20)
  )
  clips = (
    f'<rect x="{TRACK_X}" y="{TRACK_Y + 14}" width="{TRACK_WIDTH}" height="20" rx="4" fill="{BORDER}"/>'
    f'<rect x="{TRACK_X + 4}" y="{TRACK_Y + 17}" width="150" height="14" rx="3" fill="{accent}" opacity="0.75"/>'
    f'<rect x="{TRACK_X + 162}" y="{TRACK_Y + 17}" width="174" height="14" rx="3" fill="{accentAlt}" opacity="0.75"/>'
  )
  # El cabezal se dibuja en su posición final (fin de la pista); la animación lo trae desde el inicio.
  playheadX = TRACK_X + TRACK_WIDTH
  playhead = (
    '<g style="animation: sweep 2.2s ease-in-out 0.3s both">'
    f'<path d="M{playheadX - 5} {TRACK_Y - 6}h10l-5 6z" fill="{TEXT}"/>'
    f'<line x1="{playheadX}" y1="{TRACK_Y}" x2="{playheadX}" y2="{TRACK_Y + 38}" stroke="{TEXT}" stroke-width="2"/>'
    '</g>'
  )
  return ticks + clips + playhead

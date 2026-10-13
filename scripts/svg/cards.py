import textwrap

from svg.document import background, svgText, windowDots, wrapSvg
from svg.logos import logoTile
from svg.theme import ACCENTS, BORDER, FONT_SANS, MUTED, PANEL, TEXT

WIDTH = 480
HEIGHT = 200
RADIUS = 12
BAR_HEIGHT = 34
PADDING_X = 24
DESCRIPTION_CHARS = 56
MAX_DESCRIPTION_LINES = 3
LOGO_SIZE = 34
LOGO_GAP = 8
LOGO_Y = 150
MAX_LOGOS = 7
RECORDING_RED = '#ff5f57'


def renderCard(project):
  accent = ACCENTS[project['category']][0]
  content = (
    cardFrame()
    + titleBar(project)
    + svgText(PADDING_X, 72, project['title'], TEXT, 22, font=FONT_SANS, weight=700)
    + descriptionLines(project)
    + logoRow(project)
    + svgText(WIDTH - PADDING_X, LOGO_Y + 22, cardTag(project), accent, 12, anchor='end')
    + cardBorder(project, accent)
  )
  return wrapSvg(WIDTH, HEIGHT, f"{project['title']} — {project['description']}", content)


def cardFrame():
  bar = (
    f'M0 {RADIUS}a{RADIUS} {RADIUS} 0 0 1 {RADIUS}-{RADIUS}h{WIDTH - 2 * RADIUS}'
    f'a{RADIUS} {RADIUS} 0 0 1 {RADIUS} {RADIUS}v{BAR_HEIGHT - RADIUS}h-{WIDTH}z'
  )
  return (
    background(WIDTH, HEIGHT, RADIUS)
    + f'<path d="{bar}" fill="{PANEL}"/>'
    + f'<line x1="0" y1="{BAR_HEIGHT}" x2="{WIDTH}" y2="{BAR_HEIGHT}" stroke="{BORDER}"/>'
  )


def titleBar(project):
  textY = BAR_HEIGHT / 2 + 4
  if project['category'] == 'sys':
    return (
      windowDots(20, BAR_HEIGHT / 2)
      + svgText(72, textY, f"~/{project['repo']}", MUTED, 12)
      + svgText(WIDTH - 16, textY, 'git:main', MUTED, 11, anchor='end')
    )
  # Las tarjetas multimedia imitan la barra de un editor: el archivo toma la
  # extensión de la herramienta principal (primer logo), p. ej. ".unity".
  return (
    svgText(18, textY, '▶', ACCENTS['media'][1], 12)
    + svgText(36, textY, f"{project['repo']}.{project['logos'][0]}", MUTED, 12)
    + svgText(WIDTH - 30, textY, '00:00:24:12', MUTED, 11, anchor='end')
    + f'<circle cx="{WIDTH - 18}" cy="{BAR_HEIGHT / 2}" r="4" fill="{RECORDING_RED}" '
    'style="animation: blink 1.6s steps(1) infinite"/>'
  )


def descriptionLines(project):
  lines = textwrap.wrap(project['description'], DESCRIPTION_CHARS)
  if len(lines) > MAX_DESCRIPTION_LINES:
    raise ValueError(
      f"Description of '{project['repo']}' needs {len(lines)} lines; "
      f'a card fits {MAX_DESCRIPTION_LINES}. Shorten it in profile.json'
    )
  return ''.join(svgText(PADDING_X, 98 + 20 * index, line, MUTED, 14, font=FONT_SANS) for index, line in enumerate(lines))


def logoRow(project):
  if len(project['logos']) > MAX_LOGOS:
    raise ValueError(f"Project '{project['repo']}' lists {len(project['logos'])} logos; a card fits {MAX_LOGOS}")
  step = LOGO_SIZE + LOGO_GAP
  return ''.join(
    logoTile(name, PADDING_X + step * index, LOGO_Y, LOGO_SIZE, 'card')
    for index, name in enumerate(project['logos'])
  )


def cardTag(project):
  label = 'SYS × MEDIA' if project.get('bridge') else project['category'].upper()
  return f"[{label}] · {project['year']}"


def cardBorder(project, accent):
  inset = f'x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="{RADIUS}" fill="none"'
  if not project.get('bridge'):
    return f'<rect {inset} stroke="{accent}" stroke-opacity="0.45"/>'
  # El proyecto puente (ambas carreras) lleva el borde partido cian → magenta.
  sysColor = ACCENTS['sys'][0]
  mediaColor = ACCENTS['media'][0]
  return (
    '<defs><linearGradient id="bridge" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{sysColor}"/><stop offset="1" stop-color="{mediaColor}"/></linearGradient></defs>'
    f'<rect {inset} stroke="url(#bridge)" stroke-width="2"/>'
  )

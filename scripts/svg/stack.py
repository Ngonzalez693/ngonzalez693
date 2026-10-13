from svg.document import background, svgText, wrapSvg
from svg.logos import logoTile
from svg.theme import ACCENTS, BORDER, MONO_CHAR_RATIO, PANEL, TEXT

WIDTH = 1000
LABEL_X = 28
ITEMS_X = 200
TOP_PADDING = 20
TILE_SIZE = 40
ROW_PITCH = 56
GAP = 10
CHIP_HEIGHT = 28
CHIP_FONT_SIZE = 12
STACK_TITLES = {'sys': 'Software stack', 'media': 'Multimedia stack'}


def renderStack(groups, category):
  accent = ACCENTS[category][0]
  height = TOP_PADDING * 2 + ROW_PITCH * (len(groups) - 1) + TILE_SIZE
  rows = ''.join(renderRow(index, group, category, accent) for index, group in enumerate(groups))
  return wrapSvg(WIDTH, height, STACK_TITLES[category], background(WIDTH, height, 12) + rows)


def renderRow(index, group, category, accent):
  y = TOP_PADDING + ROW_PITCH * index
  idPrefix = f'{category}-{index}'
  parts = [svgText(LABEL_X, y + 25, group['label'], accent, 13)]
  x = ITEMS_X
  for column, logo in enumerate(group['logos']):
    # Retraso escalonado por fila y columna: los logos "cargan" como módulos.
    delay = round(0.05 * (index * 8 + column), 2)
    parts.append(f'<g style="animation: appear 0.4s ease {delay}s both">{logoTile(logo, x, y, TILE_SIZE, idPrefix)}</g>')
    x += TILE_SIZE + GAP
  for extra in group['extras']:
    chip, chipWidth = renderChip(extra, x, y + (TILE_SIZE - CHIP_HEIGHT) / 2)
    parts.append(chip)
    x = round(x + chipWidth + GAP, 1)
  if x - GAP > WIDTH - LABEL_X:
    raise ValueError(f"Stack row '{group['label']}' is wider than {WIDTH}px; move items to another group")
  return ''.join(parts)


def renderChip(text, x, y):
  width = round(len(text) * CHIP_FONT_SIZE * MONO_CHAR_RATIO + 24, 1)
  chip = (
    f'<rect x="{x}" y="{y}" width="{width}" height="{CHIP_HEIGHT}" rx="{CHIP_HEIGHT / 2}" '
    f'fill="{PANEL}" stroke="{BORDER}"/>'
    + svgText(round(x + width / 2, 1), y + 18, text, TEXT, CHIP_FONT_SIZE, anchor='middle')
  )
  return chip, width

import re
from pathlib import Path

from svg.theme import TILE

LOGOS_DIR = Path(__file__).resolve().parents[2] / 'assets' / 'logos'
ROOT_TAG = re.compile(r'<svg\b([^>]*)>(.*)</svg>', re.DOTALL)
# El SVG anidado recibe su propia posición y tamaño; estos atributos del original sobran.
DROPPED_ATTRS = re.compile(r'\s(?:xmlns|version|width|height)="[^"]*"')
ID_ATTR = re.compile(r'\bid="([^"]+)"')
TILE_PADDING_RATIO = 0.18
TILE_RADIUS_RATIO = 0.22


def logoPath(name):
  return LOGOS_DIR / f'{name}.svg'


def inlineLogo(name, x, y, size, idPrefix):
  source = logoPath(name).read_text(encoding='utf-8')
  match = ROOT_TAG.search(source)
  if match is None:
    raise ValueError(f"Logo '{name}' in assets/logos is not a valid SVG file")
  attrs = DROPPED_ATTRS.sub('', match.group(1))
  inner = prefixIds(match.group(2), f'{idPrefix}-{name}')
  return f'<svg x="{x}" y="{y}" width="{size}" height="{size}"{attrs}>{inner}</svg>'


def prefixIds(markup, prefix):
  # Varios íconos traen degradados con id propio; al incrustarlos juntos en un
  # mismo SVG chocarían, así que cada id y sus referencias llevan prefijo.
  for oldId in set(ID_ATTR.findall(markup)):
    newId = f'{prefix}-{oldId}'
    markup = markup.replace(f'id="{oldId}"', f'id="{newId}"')
    markup = markup.replace(f'url(#{oldId})', f'url(#{newId})')
    markup = markup.replace(f'href="#{oldId}"', f'href="#{newId}"')
  return markup


def logoTile(name, x, y, size, idPrefix):
  # Fondo claro para que los logos oscuros (Unity, Django) se vean sobre el tema oscuro.
  padding = round(size * TILE_PADDING_RATIO, 1)
  radius = round(size * TILE_RADIUS_RATIO, 1)
  logoSize = round(size - 2 * padding, 1)
  return (
    f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{radius}" fill="{TILE}"/>'
    + inlineLogo(name, round(x + padding, 1), round(y + padding, 1), logoSize, idPrefix)
  )

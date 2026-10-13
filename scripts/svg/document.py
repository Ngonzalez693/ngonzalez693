from xml.sax.saxutils import escape

from svg.theme import BG, FONT_MONO

# Sin animaciones cada elemento queda en su estilo base, que siempre es el
# fotograma final: las animaciones solo definen de dónde parten.
REDUCED_MOTION = '@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }'

SHARED_KEYFRAMES = (
  '@keyframes appear { from { opacity: 0; } to { opacity: 1; } }'
  '@keyframes blink { 50% { opacity: 0; } }'
  '@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }'
  '.grow { transform-box: fill-box; transform-origin: left center; }'
)

WINDOW_DOT_COLORS = ('#ff5f57', '#febc2e', '#28c840')


def escapeText(text):
  return escape(str(text), {'"': '&quot;'})


def wrapSvg(width, height, title, content, css=SHARED_KEYFRAMES):
  return (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}" role="img">'
    f'<title>{escapeText(title)}</title>'
    f'<style>{css}{REDUCED_MOTION}</style>{content}</svg>\n'
  )


def background(width, height, radius=16):
  return f'<rect width="{width}" height="{height}" rx="{radius}" fill="{BG}"/>'


def svgText(x, y, text, color, size, font=FONT_MONO, weight=400, anchor='start', style=''):
  styleAttr = f' style="{style}"' if style else ''
  return (
    f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" '
    f'font-weight="{weight}" text-anchor="{anchor}"{styleAttr}>{escapeText(text)}</text>'
  )


def windowDots(x, y):
  return ''.join(
    f'<circle cx="{x + 16 * index}" cy="{y}" r="5" fill="{color}"/>'
    for index, color in enumerate(WINDOW_DOT_COLORS)
  )

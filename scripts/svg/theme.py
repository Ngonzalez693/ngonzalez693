# Paleta y tipografía compartidas por todos los SVG generados.
BG = '#0b0f17'
PANEL = '#111827'
BORDER = '#1f2937'
TEXT = '#e6edf3'
MUTED = '#8b949e'
TILE = '#f0f3f6'

# Cada mitad del "dual-boot" tiene un acento principal y uno secundario.
ACCENTS = {
  'sys': ('#22d3ee', '#4ade80'),
  'media': ('#e879f9', '#fb923c'),
}

# Los SVG servidos como <img> no pueden cargar fuentes web: solo fuentes del sistema.
FONT_MONO = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', monospace"
FONT_SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

# Ancho estimado de un carácter monoespaciado respecto al tamaño de fuente; se
# redondea hacia arriba para que el efecto de tipeo nunca deje letras tapadas.
MONO_CHAR_RATIO = 0.62

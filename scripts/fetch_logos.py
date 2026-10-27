import sys
import urllib.request

from profile_data import ProfileError, loadProfile, referencedLogos
from svg.logos import LOGOS_DIR

# Versión fija: una actualización de Devicon no debe cambiar los logos sin que lo decidamos.
DEVICON_BASE = 'https://cdn.jsdelivr.net/npm/devicon@2.17.0/icons'
# Logos que no existen en un set abierto: el archivo se agrega a mano y no se descarga.
LOCAL_SOURCE = 'local'
TIMEOUT_SECONDS = 15


def sourceUrl(source):
  # Una URL completa (p. ej. Simple Icons con versión fija) se usa tal cual; lo demás es una ruta de Devicon.
  if source.startswith('https://'):
    return source
  return f'{DEVICON_BASE}/{source}.svg'


def downloadLogo(name, source):
  url = sourceUrl(source)
  with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
    content = response.read().decode('utf-8')
  if '<svg' not in content:
    raise ValueError(f'{url} did not return an SVG')
  (LOGOS_DIR / f'{name}.svg').write_text(content, encoding='utf-8', newline='\n')


def main():
  try:
    profile = loadProfile()
  except ProfileError as error:
    print(f'error: {error}', file=sys.stderr)
    return 1
  LOGOS_DIR.mkdir(parents=True, exist_ok=True)
  failures = []
  for name in sorted(referencedLogos(profile)):
    if profile['logoSources'][name] == LOCAL_SOURCE:
      print(f'skip  {name} (local file)')
      continue
    try:
      downloadLogo(name, profile['logoSources'][name])
      print(f'ok    {name}')
    except (OSError, ValueError) as error:
      # URLError/HTTPError (p. ej. un 404) heredan de OSError.
      failures.append(name)
      print(f'fail  {name}: {error}', file=sys.stderr)
  if failures:
    print(f'error: {len(failures)} logo(s) failed: {", ".join(failures)}', file=sys.stderr)
    return 1
  return 0


if __name__ == '__main__':
  sys.exit(main())

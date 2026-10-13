import sys
from pathlib import Path

from profile_data import checkLogoFiles, loadProfile
from svg.banner import renderBanner
from svg.cards import renderCard
from svg.headers import renderHeader
from svg.stack import renderStack

OUTPUT_DIR = Path(__file__).resolve().parents[1] / 'assets' / 'generated'


def buildAssets(profile):
  assets = {
    'banner.svg': renderBanner(profile),
    'header-software.svg': renderHeader('sys'),
    'header-multimedia.svg': renderHeader('media'),
    'stack-software.svg': renderStack(profile['stacks']['sys'], 'sys'),
    'stack-multimedia.svg': renderStack(profile['stacks']['media'], 'media'),
  }
  for project in profile['projects']:
    assets[f"card-{project['repo'].lower()}.svg"] = renderCard(project)
  return assets


def writeAssets(assets):
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  # Un proyecto quitado de profile.json no debe dejar su tarjeta vieja publicada.
  for stale in OUTPUT_DIR.glob('*.svg'):
    if stale.name not in assets:
      stale.unlink()
      print(f'removed assets/generated/{stale.name}')
  for fileName, content in assets.items():
    (OUTPUT_DIR / fileName).write_text(content, encoding='utf-8', newline='\n')
    print(f'wrote   assets/generated/{fileName}')


def main():
  try:
    profile = loadProfile()
    checkLogoFiles(profile)
    # Todo se genera en memoria antes de escribir: un error no deja archivos a medias.
    assets = buildAssets(profile)
    writeAssets(assets)
  except (ValueError, OSError) as error:
    print(f'error: {error}', file=sys.stderr)
    return 1
  return 0


if __name__ == '__main__':
  sys.exit(main())

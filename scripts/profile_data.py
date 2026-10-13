import json
from pathlib import Path

from svg.logos import logoPath

PROFILE_PATH = Path(__file__).resolve().parent / 'data' / 'profile.json'
CATEGORIES = ('sys', 'media')
PROFILE_FIELDS = ('name', 'title', 'logoSources', 'stacks', 'projects')
GROUP_FIELDS = ('label', 'logos', 'extras')
PROJECT_FIELDS = ('repo', 'title', 'description', 'category', 'year', 'logos')
PROJECT_TEXT_FIELDS = ('repo', 'title', 'description')


class ProfileError(ValueError):
  pass


def loadProfile(path=PROFILE_PATH):
  try:
    profile = json.loads(Path(path).read_text(encoding='utf-8'))
  except (OSError, json.JSONDecodeError) as error:
    raise ProfileError(f'Cannot read {path}: {error}') from error
  validateProfile(profile)
  return profile


def validateProfile(profile):
  requireKeys(profile, PROFILE_FIELDS, 'profile.json')
  requireKeys(profile['stacks'], CATEGORIES, 'stacks')
  for category in CATEGORIES:
    validateGroups(profile['stacks'][category], f'stacks.{category}')
  requireList(profile['projects'], 'projects')
  for project in profile['projects']:
    validateProject(project)
  requireUniqueRepos(profile['projects'])
  unknown = referencedLogos(profile) - set(profile['logoSources'])
  if unknown:
    raise ProfileError(f'Logos without an entry in logoSources: {", ".join(sorted(unknown))}')


def validateGroups(groups, where):
  requireList(groups, where)
  for group in groups:
    requireKeys(group, GROUP_FIELDS, f'{where} group')
    requireText(group['label'], f'{where} group label')
    requireList(group['logos'], f"{where} '{group['label']}' logos", allowEmpty=True)
    requireList(group['extras'], f"{where} '{group['label']}' extras", allowEmpty=True)


def validateProject(project):
  repo = project.get('repo', '?') if isinstance(project, dict) else '?'
  where = f"project '{repo}'"
  requireKeys(project, PROJECT_FIELDS, where)
  for field in PROJECT_TEXT_FIELDS:
    requireText(project[field], f'{where} {field}')
  # bool es subclase de int en Python: hay que excluirlo explícitamente.
  if not isinstance(project['year'], int) or isinstance(project['year'], bool):
    raise ProfileError(f'{where}: year must be an integer')
  # Un string como "false" sería verdadero y pintaría la tarjeta como puente.
  if not isinstance(project.get('bridge', False), bool):
    raise ProfileError(f'{where}: bridge must be true or false')
  if project['category'] not in CATEGORIES:
    raise ProfileError(f'{where}: category must be one of {", ".join(CATEGORIES)}')
  requireList(project['logos'], f'{where} logos')


def requireUniqueRepos(projects):
  # El archivo de cada tarjeta sale del repo en minúsculas: dos repos iguales se pisarían.
  seen = set()
  for project in projects:
    key = project['repo'].lower()
    if key in seen:
      raise ProfileError(f"Two projects share the repo name '{project['repo']}' (ignoring case)")
    seen.add(key)


def requireKeys(item, keys, where):
  if not isinstance(item, dict):
    raise ProfileError(f'{where} must be a JSON object')
  missing = [key for key in keys if key not in item]
  if missing:
    raise ProfileError(f'{where} is missing: {", ".join(missing)}')


def requireText(value, where):
  if not isinstance(value, str) or not value.strip():
    raise ProfileError(f'{where} must be non-empty text')


def requireList(value, where, allowEmpty=False):
  if not isinstance(value, list):
    raise ProfileError(f'{where} must be a list')
  if not value and not allowEmpty:
    raise ProfileError(f'{where} must not be empty')


def referencedLogos(profile):
  names = {logo for project in profile['projects'] for logo in project['logos']}
  for category in CATEGORIES:
    names.update(logo for group in profile['stacks'][category] for logo in group['logos'])
  return names


def checkLogoFiles(profile):
  missing = sorted(name for name in referencedLogos(profile) if not logoPath(name).is_file())
  if missing:
    raise ProfileError(
      f'Missing logo files in assets/logos: {", ".join(missing)}. '
      'Run: python scripts/fetch_logos.py'
    )

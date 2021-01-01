import re

VALID_CHARS = r'\'a-zA-Z0-9 !_.,\(\)&#-'

TAG_TO_GROUP = {
    '%ARTIST': f'(?P<artist>[{VALID_CHARS}]+)',
    '%ALBUM': f'(?P<album>[{VALID_CHARS}]+)',
    '%YEAR': r'(?P<date>\d+)',
    '%TRACK_NUM': r'(?P<tracknumber>\d+)',
    '%TRACK_TITLE': f'(?P<title>[{VALID_CHARS}]+)',
    '%GENRE': f'(?P<genre>[{VALID_CHARS}]+)',
}


def make_exact(formula: str) -> str:
    return ('^' if not formula.startswith('^') else '') + formula + ('$' if not formula.endswith('$') else '')


def formula_to_regex(formula: str) -> re.Pattern:
    for tag, group in TAG_TO_GROUP.items():
        formula = formula.replace(tag, group)
    return re.compile(make_exact(formula))

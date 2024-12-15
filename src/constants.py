import os
import re

HOME_PATH = os.environ['HOME']
CACHE_PATH = os.path.join(HOME_PATH, '.cache', 'walcord')
KEY_REGEX = re.compile(r'KEY\([^)]*\)', re.IGNORECASE)
KEY_WITH_VALUES_REGEX = re.compile(r'KEY\((\w+)(?:,\s*(\d+(?:\.\d+)?))?\)(\.\w+)?', re.IGNORECASE)
DEFAULT_WAL_COLORS_PATH = os.path.join(HOME_PATH, '.cache', 'wal', 'colors.json')
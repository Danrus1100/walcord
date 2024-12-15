import os
import hashlib
import json
import constants as CONST
from colors import Colors
class ThemeFile():
    def __init__(self, path):
        if "~" in path: path = path.replace("~", CONST.HOME_PATH)
        path = os.path.abspath(os.path.expanduser(path))
        self.path = path
        self.basename = os.path.basename(path)
        self.cache_path = os.path.join(CONST.CACHE_PATH,  f"{self.get_hash(path)[:16]}" + '.json')
        self.text = self.read_file()
        self._cache = {
            "path": self.path,
            "hash": self.get_hash(self.text),
            "lines": []
        }
        self._open_theme_file()
        self.text_lines: list = self.read_file_as_lines()
        self.key_lines: list = self._get_key_lines() 

    def read_file(self):
        with open(self.path, 'r') as f:
            return f.read()
    
    def write_file(self):
        with open(self.path, 'w') as f:
            f.write(self.text)

    def write_file_from_lines(self):
        with open(self.path, 'w') as f:
            f.writelines(self.text_lines)
    
        
    def read_file_as_lines(self):
        with open(self.path, 'r') as f:
            return f.readlines()

    def _write_cache(self):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, 'w') as f:
            json.dump(self._cache, f, indent=2)

    def read_cache(self):
        with open(self.cache_path, 'r') as f:
            self._cache = json.loads(f.read())
    
    def _open_theme_file(self):
        try:
            self.read_cache()
        except Exception:
            self._write_cache()
    
    def _get_lines_with_key(self):
        for n, line in enumerate(self.text_lines):
            if CONST.KEY_REGEX.search(line):
                self._cache["lines"].append({'n':n, 'raw':line, 'past':self.text_lines[n]})
    
    def _get_key_lines(self):
        if self._cache["lines"] == []:
            self._get_lines_with_key()
        self._write_cache()
        return self._cache["lines"]

    def resub_key_lines(self, colors: Colors):
        for n, line in enumerate(self.key_lines):
            new_value = self.replace_key_with_value(line['raw'], colors.remap_key)
            self.text_lines[int(line['n'])] = new_value
            if new_value != line['past']: self.key_lines[n]['past'] = new_value
        self._write_cache()

    
    def get_past_key_lines(self):
        pass

    @staticmethod
    def get_hash(string):
        return hashlib.md5(string.encode()).hexdigest()
    
    @staticmethod
    def replace_key_with_value(text, value):
        return CONST.KEY_WITH_VALUES_REGEX.sub(value, text)
    
# ----------------- Main - Functions-----------------
    
    def compile_theme(self, colors: Colors):
        self.resub_key_lines(colors)
        self.write_file_from_lines()

    def reset_theme(self):
        for line in self.key_lines:
            self.text_lines[int(line['n'])] = line['raw']
        self.write_file_from_lines()

    def check_key_changes(self):
        if self._cache["hash"] == self.get_hash(self.text):
            return
        
        for i in self.key_lines:
            if self.text_lines[int(i['n'])] != i['past']:
                self.key_lines.remove(i)
        for n, line in enumerate(self.text_lines):
            if CONST.KEY_REGEX.search(line):
                self._cache["lines"].append({'n':n, 'raw':line, 'past':self.text_lines[n]})
        self._write_cache()
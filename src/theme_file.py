import os
import hashlib
import json
import constants as CONST
class ThemeFile():
    def __init__(self, path):
        if "~" in path: path = path.replace("~", CONST.HOME_PATH)
        path = os.path.abspath(os.path.expanduser(path))
        self.path = path
        self.basename = os.path.basename(path)
        self.cache_path = os.path.join(CONST.CACHE_PATH,  f"{self.get_hash(path)[:16]}" + '.json')
        self._cache = {
            "path": self.path,
            "lines": []
        }
        self._open_theme_file()
        self.text = self.read_file()
        self.text_lines = self.read_file_as_lines()
        self.raw_key_lines = self._get_key_lines() 

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
            json.dump(self._cache, f)

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
                self._cache["lines"].append({n: line})
    
    def _get_key_lines(self):
        if self._cache["lines"] == []:
            self._get_lines_with_key()
        self._write_cache()
        return self._cache["lines"]
    
    def make_theme(self):
        self.resub_key_lines()
        self.write_file_from_lines()

    def resub_key_lines(self):
        for n, line in enumerate(self.raw_key_lines):
            for key in line:
                self.text_lines[int(key)] = self.replace_key_with_value(self.raw_key_lines[n][key], "test")

    @staticmethod
    def get_hash(string):
        return hashlib.md5(string.encode()).hexdigest()
    
    @staticmethod
    def replace_key_with_value(text, value):
        return CONST.KEY_WITH_VALUES_REGEX.sub(value, text)

import os
import hashlib
import json
import constants as CONST
from colors import Colors
from line import Line
class File():
    def __init__(self, path, colors: Colors) -> None:
        self.path = os.path.abspath(path)
        self.cache_path = os.path.join(CONST.CACHE_PATH, self.get_hash(self.path)[:16]+'.json')
        self.lines: list[Line] = list()
        self.colors = colors
        for n, line in enumerate(self.read()):
            self.lines.append(Line(n, line, colors))

    def read(self) -> list[str]:
        with open(self.path, 'r') as f:
            return f.readlines()
    
    def write(self) -> None:
        with open(self.path, 'w') as f:
            for line in self.lines:
                f.write(line.compiled)

    def save(self) -> None:
        t = ''.join(line.compiled for line in self.lines)
        c = {
            'path': self.path,
            'hash': self.get_hash(t),
            'lines': [line.exported for line in self.lines if line.has_key]
        }
        with open(self.cache_path, 'w') as f:
            f.write(json.dumps(c, indent=2))
    
    def __read_save_file(self):
        with open(self.cache_path, 'r') as f:
            return json.loads(f.read())
        
    def __write_save_file(self, c: dict) -> None:
        with open(self.cache_path, 'w') as f:
            f.write(json.dumps(c, indent=2))

    def load(self) -> None:
        t = ''.join(line.compiled for line in self.lines)
        try:
            c = self.__read_save_file()
            if c['hash'] != self.get_hash(t):
                self.refact_save()
                return
            for n, line in enumerate(self.lines):
                if line.has_key:
                    self.lines[n] = Line(**c['lines'][n])
        except FileNotFoundError:
            raise FileNotFoundError(f"Cache file not found at {self.cache_path}")

    def refact_save(self) -> None:
        try:
            c = self.__read_save_file()
        except FileNotFoundError:
            raise FileNotFoundError(f"Cache file not found at {self.cache_path}")

        current_lines = self.read()
        saved_lines = c['lines']

        # Update existing lines
        for saved_line in saved_lines:
            for n, current_line in enumerate(current_lines):
                if current_line.strip() == saved_line['text'].strip():
                    saved_line['n'] = n
                    line_obj = Line(n=n, text=current_line, colors=self.colors)
                    saved_line['compiled_text'] = line_obj.compiled
                    break

        # add new Lines with KEY
        for n, current_line in enumerate(current_lines):
            if CONST.KEY_REGEX.search(current_line) and not any(line['text'].strip() == current_line.strip() for line in saved_lines):
                new_line = Line(n=n, text=current_line, colors=self.colors)
                saved_lines.append(new_line.exported)

        # save
        c['lines'] = saved_lines
        self.__write_save_file(c)
        
    @staticmethod
    def get_hash(text: str):
        return hashlib.md5(text.encode()).hexdigest()
        
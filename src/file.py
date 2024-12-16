import os
import hashlib
import json
import constants as CONST
from colors import Colors
from line import Line
class File():
    def __init__(self, path, colors: Colors) -> None:
        self.path = os.path.abspath(path)
        self.cache_path = os.path.join(CONST.CACHE_DIR, self.get_hash(self.path)+'.json')
        self.lines: list[Line] = list()
        for n, line in enumerate(self.read()):
            self.lines.append(Line(n, line, colors))

    def read(self) -> list[str]:
        with open(self.path, 'r') as f:
            return f.readlines()
    
    def write(self) -> None:
        with open(self.path, 'w') as f:
            for line in self.lines:
                f.write(line.compiled + '\n')

    def save(self) -> None:
        t = ''.join(line.compiled for line in self.lines)
        c = {
            'path': self.path,
            'hash': self.get_hash(t),
            'lines': [line.exported for line in self.lines]
        }
        with open(self.cache_path, 'w') as f:
            f.write(json.dumps(c, indent=2))
    
    def load(self) -> None:
        t = ''.join(line.compiled for line in self.lines)
        try:
            with open(self.cache_path, 'r') as f:
                c = json.loads(f.read())
                if c['hash'] != self.get_hash(t):
                    self.refact_save()
                    return
                self.lines = [Line(**line) for line in c['lines']]
        except FileNotFoundError:
            raise FileNotFoundError(f"Cache file not found at {self.cache_path}")

    def refact_save(self) -> None:
        pass # TODO: Implement refact_save
        
    @staticmethod
    def get_hash(text: str):
        return hashlib.md5(text.encode()).hexdigest()
        
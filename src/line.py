import constants as CONST
from colors import Colors

class Line():
    def __init__(self, n: int = 0, text: str = "", colors: Colors = Colors(), compiled_text = None, **kwargs) -> None:
        if isinstance(n, dict):
            kwargs = n
            n = kwargs.get('n', 0)
            text = kwargs.get('text', "")
            colors = kwargs.get('colors', Colors())
            compiled_text = kwargs.get('compiled_text', None)
        
        self.n = n
        self.text = text
        self.colors = colors
        self.has_key = False
        if compiled_text is None and CONST.KEY_REGEX.search(text):
            self.compile()
            self.has_key = True
        self.__compiled_text = compiled_text
    
    def __str__(self) -> str:
        return f"Line(n={self.n}, text='{self.text}', has_key={self.has_key})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Line):
            return False
        return self.text == other.text and self.__compiled_text == other.__compiled_text

    def compile(self) -> None:
        self.__compiled_text = CONST.KEY_WITH_VALUES_REGEX.sub(self.colors.remap_key, self.text)
    
    @property
    def compiled(self) -> str:
        self.compile()
        return self.__compiled_text
    
    @property
    def exported(self) -> dict:
        return {
            'n': self.n,
            'text': self.text,
            'compiled_text': self.__compiled_text
        }
        
    
    
import constants as CONST
import json
import re

class Colors:
    def __init__(self, colors_path: str = CONST.DEFAULT_WAL_COLORS_PATH):
        self.colors: dict = self.map_colors(self.get_colors_from_json(colors_path))
        self.MODIFIER_HANDLERS = {
            'DEFAULT': self.return_rgba,
            '.rgba': self.return_rgba,
            '.rgb': self.return_rgb,
            '.hex': self.return_hex,
            '.hsl': self.return_hsl,

            '.rgba_values': self.return_values,
            '.rgb_values': self.return_values_without_opacity,
            '.hex_values': self.return_hex_values,
            '.hsl_values': self.return_hsl_values,

            '.r': self.return_red,
            '.red': self.return_red,

            '.g': self.return_green,
            '.green': self.return_green,

            '.b': self.return_blue,
            '.blue': self.return_blue,

            '.o': self.return_opacity,
            '.opacity': self.return_opacity,

            '.h': self.return_h_from_hsl,
            '.hue': self.return_h_from_hsl,

            '.s': self.return_s_from_hsl,
            '.saturation': self.return_s_from_hsl,

            '.l': self.return_l_from_hsl,
            '.lightness': self.return_l_from_hsl

        }

    def get_colors_from_json(self, path = CONST.DEFAULT_WAL_COLORS_PATH):
        with open(path, 'r') as f:
            return json.loads(f.read())
    


    def remap_key(self, match: re.Match) -> str:
        """
        Remaps the key to the css rgba format.

        :param match: The match object to remap.
        :type match: re.Match
        """

        first_arg = match.group(1).lower()
        first_arg_values = self.colors.get(first_arg)
        if not first_arg_values:
            raise ValueError(f"Color '{first_arg}' not found in the colors dictionary.")
        second_arg = match.group(2) if match.group(2) else "1.0"
        try:
            second_arg = float(second_arg)
            if second_arg < 0.0:
                raise ValueError(f"Opacity value is not a valid: {second_arg} (it should be 0.0-1.0 or 1-100). Opacity will be set to 1.0...")
                opacity = 1.0
            if second_arg > 1.0 and second_arg < 100:
                second_arg = second_arg / 100
            elif second_arg > 100:
                raise ValueError(f"Opacity value is not a valid: {second_arg} (it should be less than 100%). Opacity will be set to 1.0...")
                opacity = 1.0
            opacity = second_arg
        except Exception as e:
            raise ValueError(f"Opacity value is not a valid: {second_arg}. opacity will be set to 1.0")
            opacity = 1.0


        modifier = str(match.group(3)).lower() if match.group(3) else None

        if (first_arg == "wallpaper" or first_arg == "w") and (opacity != 1.0 or modifier):
            raise ValueError(f"You cant use opacity or modifier with wallpaper key.")
        if modifier and modifier in self.MODIFIER_HANDLERS:
            return self.MODIFIER_HANDLERS[modifier](first_arg_values, opacity)
        return self.MODIFIER_HANDLERS['DEFAULT'](first_arg_values, opacity)



#------------------------------- STATIC METHODS ----------------------------------#
    @staticmethod
    def map_colors(colors: dict):
        """
        Maps the given colors to list.

        :param colors: The colors to map to the theme file.
        :type colors: dict
        """
        return {
            "wallpaper": colors["wallpaper"],
            "background": colors["special"]["background"],
            "foreground": colors["special"]["foreground"],
            "0": colors["colors"]["color0"],
            "1": colors["colors"]["color1"],
            "2": colors["colors"]["color2"],
            "3": colors["colors"]["color3"],
            "4": colors["colors"]["color4"],
            "5": colors["colors"]["color5"],
            "6": colors["colors"]["color6"],
            "7": colors["colors"]["color7"],
            "8": colors["colors"]["color8"],
            "9": colors["colors"]["color9"],
            "10": colors["colors"]["color10"],
            "11": colors["colors"]["color11"],
            "12": colors["colors"]["color12"],
            "13": colors["colors"]["color13"],
            "14": colors["colors"]["color14"],
            "15": colors["colors"]["color15"],

            # special colors
            "border": colors["colors"]["color2"],
            "text": colors["colors"]["color15"],
            "accent": colors["colors"]["color13"],

            # short names
            "b": colors["special"]["background"], 
            "f": colors["special"]["foreground"],
            "br": colors["colors"]["color2"],
            "t": colors["colors"]["color15"],
            "a": colors["colors"]["color13"],
            "w": colors["wallpaper"]

        }

    @staticmethod
    def rgb_to_hls(color: tuple) -> tuple:
        """
        Converts the given rgb color to hls.

        :param color: The color to convert to hls.
        :type color: tuple
        :return: The color converted to hls.
        :rtype: tuple
        """
        r, g, b = color
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        maxc = max(r, g, b)
        minc = min(r, g, b)
        l = (maxc + minc) / 2.0
        if maxc == minc:
            h = s = 0.0
        else:
            d = maxc - minc
            s = d / (2.0 - maxc - minc) if l > 0.5 else d / (maxc + minc)
            if maxc == r:
                h = (g - b) / d + (6.0 if g < b else 0.0)
            elif maxc == g:
                h = (b - r) / d + 2.0
            else:
                h = (r - g) / d + 4.0
            h /= 6.0
        return h, l, s

    @staticmethod
    def return_rgba(color_tuple, opacity):
        return f"rgba({color_tuple[0]},{color_tuple[1]},{color_tuple[2]},{opacity})"

    @staticmethod
    def return_rgb(color_tuple, opacity):
        return f"rgb({color_tuple[0]},{color_tuple[1]},{color_tuple[2]})"

    @staticmethod
    def return_values(color_tuple, opacity):
        return f"{color_tuple[0]},{color_tuple[1]},{color_tuple[2]},{opacity}"

    @staticmethod
    def return_values_without_opacity(color_tuple, opacity):
        return f"{color_tuple[0]},{color_tuple[1]},{color_tuple[2]}"

    @staticmethod
    def return_red(color_tuple, opacity):
        return f"{color_tuple[0]}"

    @staticmethod
    def return_green(color_tuple, opacity):
        return f"{color_tuple[1]}"

    @staticmethod
    def return_blue(color_tuple, opacity):
        return f"{color_tuple[2]}"

    @staticmethod
    def return_opacity(color_tuple, opacity):
        return f"{opacity}"

    @staticmethod
    def return_hex(color_tuple, opacity):
        return f"#{color_tuple[0]:02x}{color_tuple[1]:02x}{color_tuple[2]:02x}"

    @staticmethod
    def return_hex_values(color_tuple, opacity):
        return f"{color_tuple[0]:02x}{color_tuple[1]:02x}{color_tuple[2]:02x}"

    
    def return_hsl(self, color_tuple, opacity):
        h, l, s = self.rgb_to_hls(color_tuple)
        return f"hsl({h},{l},{s})"

    
    def return_h_from_hsl(self, color_tuple, opacity):
        h, l, s = self.rgb_to_hls(color_tuple)
        return f"{h}"

    
    def return_s_from_hsl(self, color_tuple, opacity):
        h, l, s = self.rgb_to_hls(color_tuple)
        return f"{s}"

    
    def return_l_from_hsl(self, color_tuple, opacity):
        h, l, s = self.rgb_to_hls(color_tuple)
        return f"{l}"

    
    def return_hsl_values(self, color_tuple, opacity):
        h, l, s = self.rgb_to_hls(color_tuple)
        return f"{h},{l},{s}"
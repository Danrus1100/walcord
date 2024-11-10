import argparse
import pywal
import os
import sys
import re

HOME_PATH = os.environ['HOME']
VESKTOP_THEME_PATH = os.path.join(HOME_PATH, ".config/vesktop/themes")

def get_colors(image_path: str) -> dict:
    """
    Returns a dictionary of colors generated from the given image path.

    :param image_path: The path to the image to generate colors from.
    :type image_path: str
    :return: A dictionary of colors in the format of pywal.
    :rtype: dict
    """
    return pywal.colors.get(image_path)

def map_colors(colors: dict) -> dict:
    """
    Maps the given colors to list.

    :param colors: The colors to map to the theme file.
    :type colors: dict
    """
    return {
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

    }

def hex_to_rgb_map(colors: dict) -> dict:
    """
    Maps the hex colors to rgb colors.

    :param color: The colors to map to rgb.
    :type color: dict
    :return: A list of colors mapped to rgb.
    :rtype: dict
    """
    returned = {}
    for color in colors:
        returned[color] = tuple(int(colors[color].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    return returned

def remap_key(match) -> str:
    """
    Remaps the key to the css rgba format.

    :param match: The match object to remap.
    :type match: re.Match
    """
    global colors

    first_arg = match.group(1).lower()
    first_arg = f"{colors[first_arg][0]}, {colors[first_arg][1]}, {colors[first_arg][2]}"

    second_arg = match.group(2)
    if second_arg:
        second_arg = str(float(second_arg))
    else:
        second_arg = '1'
    return f'rgba({first_arg}, {second_arg})'

def replace_key(text: str) -> str:
    """
    Replaces the key with the rgba format.

    :param text: The text to replace the key in.
    :type text: str
    :return: The text with the key replaced.
    :rtype: str
    """
    return re.sub(r'KEY\((\w+)(?:,\s*(0\.\d+))?\)', remap_key, text)

colors = {}

def main():
    global colors
    parser = argparse.ArgumentParser(description="Create a theme file from pywal colors.")
    parser.add_argument("--image", "-i", type=str, help="The path to the image to generate colors from.")
    parser.add_argument("--theme", "-t", type=str, help="The path to the theme file to replace colors in.")
    args = parser.parse_args()
    if not args.image and not args.theme:
        print("Usage: walcord --image <image_path> --theme <theme_path>")
        sys.exit(1)
    
    if not os.path.exists(VESKTOP_THEME_PATH):
        os.makedirs(VESKTOP_THEME_PATH)

    image_path = args.image
    theme_path = args.theme
    theme_file_name = os.path.basename(theme_path)
    theme_text = ""
    colors = hex_to_rgb_map(map_colors(get_colors(image_path)))
    with open(theme_path, "r") as theme_file:
        theme_lines = theme_file.readlines()
    for i in theme_lines:
        i = replace_key(i)
        theme_text += i

    with open(os.path.join(VESKTOP_THEME_PATH, theme_file_name), "w+") as file:
        file.write(theme_text)

if __name__ == "__main__":
    main()
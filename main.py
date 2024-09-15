import argparse
import pywal
import os
import sys

HOME_PATH = os.environ['HOME']
VESCKTOP_THEME_PATH = os.path.join(HOME_PATH, ".config/vesktop/themes")

def main():
    parser = argparse.ArgumentParser(description="Create a theme file from pywal colors.")
    parser.add_argument("--image", "-i", type=str, help="The path to the image to generate colors from.")
    parser.add_argument("--theme", "-t", type=str, help="The path to the theme file to replace colors in.")
    args = parser.parse_args()
    if not args.image and not args.theme:
        print("Usage: main.py --image <image_path> --theme <theme_path>")
        sys.exit(1)
    
    if not os.path.exists(VESCKTOP_THEME_PATH):
        os.makedirs(VESCKTOP_THEME_PATH)
    

    image_path = args.image
    theme_path = args.theme
    theme_file_name = os.path.basename(theme_path)
    print(theme_path)
    with open(theme_path, "r") as theme_file:
        theme_text = theme_file.read()
    theme_file.close()
    theme_text = replace_keys(file=theme_text, keys=color_to_keys(get_colors(image_path)))
    with open(os.path.join(VESCKTOP_THEME_PATH, theme_file_name), "w+") as file:
        file.write(theme_text)

#-----------------------------------------------------------------------------------------------

def get_colors(image_path):
    """
    Returns a dictionary of colors generated from the given image path.

    :param image_path: The path to the image to generate colors from.
    :type image_path: str
    :return: A dictionary of colors in the format of pywal.
    :rtype: dict
    """
    return pywal.colors.get(image_path)

def color_to_keys(colors):
    """
    Maps pywal color names to key names that can be used for replacing strings in theme files.

    :param colors: A dictionary of colors in the format of pywal.
    :type colors: dict
    :return: A dictionary where the keys are the key names and the values are the corresponding color codes.
    :rtype: dict
    """
    return {
        #main colors
        "KEY_BACKGROUND": colors["special"]["background"],
        "KEY_FOREGROUND": colors["special"]["foreground"],
        "KEY_0": colors["colors"]["color0"],
        "KEY_1": colors["colors"]["color1"],
        "KEY_2": colors["colors"]["color2"],
        "KEY_3": colors["colors"]["color3"],
        "KEY_4": colors["colors"]["color4"],
        "KEY_5": colors["colors"]["color5"],
        "KEY_6": colors["colors"]["color6"],
        "KEY_7": colors["colors"]["color7"],
        "KEY_8": colors["colors"]["color8"],
        "KEY_9": colors["colors"]["color9"],
        "KEY_10": colors["colors"]["color10"],
        "KEY_11": colors["colors"]["color11"],
        "KEY_12": colors["colors"]["color12"],
        "KEY_13": colors["colors"]["color13"],
        "KEY_14": colors["colors"]["color14"],
        "KEY_15": colors["colors"]["color15"],

        #simplified titles (needed for unity of themes)
        "KEY_BORDER": colors["colors"]["color2"],
        "KEY_TEXT": colors["colors"]["color15"],
        "KEY_ACCENT": colors["colors"]["color13"]
    }

def replace_keys(file, keys):
    """
    Replace all occurrences of keys in a given string with their respective values.

    :param file: The string to replace keys in.
    :type file: str
    :param keys: A dictionary of keys to replace and their corresponding values.
    :type keys: dict
    :return: The string with all keys replaced.
    :rtype: str
    """
    string = file
    for key in keys:
        string = string.replace(key, keys[key])
    return string

if __name__ == "__main__":
    main()

import unittest
from unittest.mock import patch
import main
from main import replace_key

class TestReplaceKey(unittest.TestCase):
    def setUp(self):
        main.colors = {
            "background": (19, 31, 44),
            "foreground": (216, 212, 216),
            "wallpaper": "/mock/wallpaper/path/image.jpg",
        }

    def test_replace_key_basic(self):
        input_text = "KEY(background)"
        expected_output = "rgba(19,31,44,1.0)"
        self.assertEqual(replace_key(input_text), expected_output)

    def test_replace_key_with_opacity(self):
        input_text = "KEY(background, 0.5)"
        expected_output = "rgba(19,31,44,0.5)"
        self.assertEqual(replace_key(input_text), expected_output)

    def test_replace_key_with_modifier(self):
        input_text = "KEY(background).rgb"
        expected_output = "rgb(19,31,44)"
        self.assertEqual(replace_key(input_text), expected_output)

    def test_replace_key_with_opacity_and_modifier(self):
        input_text = "KEY(background, 0.7).rgb"
        expected_output = "rgb(19,31,44)"
        self.assertEqual(replace_key(input_text), expected_output)

    def test_replace_key_with_invalid_key(self):
        input_text = "KEY(invalid_key)"
        with self.assertRaises(ValueError):
            replace_key(input_text)

    def test_replace_key_with_wallpaper(self):
        input_text = "KEY(wallpaper)"
        expected_output = "/mock/wallpaper/path/image.jpg"
        self.assertEqual(replace_key(input_text), expected_output)

    def test_replace_key_with_wallpaper_and_opacity(self):
        input_text = "KEY(wallpaper, 0.5)"
        with self.assertRaises(ValueError):
            replace_key(input_text)

    def test_replace_key_with_multiple_keys(self):
        input_text = "KEY(background) and KEY(foreground)"
        expected_output = "rgba(19,31,44,1.0) and rgba(216,212,216,1.0)"
        self.assertEqual(replace_key(input_text), expected_output)

    def test_replace_key_with_seconds_mods(self):
        input_text = "KEY(background).rgb.add(0, 10) and KEY(foreground).rgb.sub(0, 10) and KEY(foreground).rgb.invert"
        expected_output = "rgb(29,31,44) and rgb(206,212,216) and rgb(39,43,39)"
        self.assertEqual(replace_key(input_text), expected_output)
    
    def test_replace_key_with_incorrect_add_second_mod(self):
        input_text = "KEY(background).r.add(-10)"
        with self.assertRaises(ValueError):
            replace_key(input_text)

if __name__ == "__main__":
    unittest.main()
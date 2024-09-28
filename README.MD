# Walcord - Pywal themes for Vesktop

### How to build frome source:
```bash
git clone https://github.com/Danrus1100/walcord.git
cd walcord
python -m venv .venv/
source .venv/bin/activate 
pip install -r requirements.txt --upgrade
pyinstaller --onefile main.py -n walcord
./dist/walcord
```
### Usage
First, you need to prepare a topic that will be used as the basis for your theme.
To do this, download the theme, and replace the colors you want with KEY_<PYWAL_COLOR_NAME>. Example:
```css
***
--bg-3: KEY_BACKGROUND;
--text-3: KEY_2
***
```
You can also use the following keys to simplify readability:
 - **KEY_BORDER = KEY_2**
 - **KEY_TEXT = KEY_15**
 - **KEY_ACCENT = KEY_13**

After that, you can use this theme in walcord:

```bash
./walcord -i <path/to/image> -t <path/to/theme>
```

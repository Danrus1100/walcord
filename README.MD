# Walcord - (Pywal)ing *every* themes for Vencord/Vesktop/BeterDiscord

![image](images/demo.gif)
<p align="center">

<a href="https://github.com/Danrus1100/walcord/tree/main/examples">More themes examples</a>
</p>

<p align="center">
<a href="https://aur.archlinux.org/packages/walcord"><img alt="Static Badge" src="https://img.shields.io/badge/AUR-2.8-blue"></a>
<a href="https://github.com/Danrus1100/walcord/releases/download/2.5/walcord.exe"><img alt="Static Badge" src="https://img.shields.io/badge/Windows-2.5-green"></a>
</p>

## How to install from [AUR](https://aur.archlinux.org/packages/walcord)
#### using yay:
```bash
yay -S walcord
```
#### using git:
```bash
git clone https://aur.archlinux.org/walcord.git
cd walcord
makepkg -si
```
## How to install from [releases](https://github.com/Danrus1100/walcord/releases):
#### Linux:
1. Download [Pywal](https://github.com/dylanaraps/pywal) / [Hellwal](https://github.com/danihek/hellwal) / [wallust](https://codeberg.org/onemoresuza/wallust)
2. Download a [binary](https://github.com/Danrus1100/walcord/releases/download/2.6/walcord) file
3. Сopy in /usr/bin/ directory:
```bash
sudo cp <path_to>/walcord /usr/bin
walcord
```

## How to build frome source:
```bash
git clone https://github.com/Danrus1100/walcord.git
cd walcord
python -m venv .venv/
source .venv/bin/activate 
pip install -r requirements-<your-system>.txt --upgrade
pyinstaller walcord.spec
./dist/walcord
```

## Usage cases:

### 1. Using Default theme (easiest way)

 1. *run a `walcord` command*
 2. *select `Walcord Default Theme` in Vesktop*

### 2. Overwrite a existing theme
First, you need to prepare a theme that will be used as the basis for your theme (or you can just take ready for use theme frome [examples](https://github.com/Danrus1100/walcord/tree/main/examples)).
To do this, [download](https://betterdiscord.app/themes) the theme, and replace the colors you want with KEY(key_name, opacity).
script will replace the KEY with the css color code in rgba format:

```css
--some-var: KEY(1, 0.5); /* will become rgba(r, g, b, 0.5) */
```
The KEY syntax will be discussed in more detail [here](#keys-syntax)

After that, you can use this theme (or folder with themes) in walcord:
```bash
walcord -t <path/to/themes>
```

### 3 Use for other applications
Walcord doesn't care what type of file is given to it, so it can be used in many places. the limit of possibilities is your imagination! to save a style file in a certain directory use `--output`:

```bash
walcord -t <path-to-some-file.txt> -o <path-and/or-name-a-new-file>
```

You can also use the image you want, from which the colors will be taken, using `--image`:
```bash
walcord -i <path-to-image>
```

## Tips and Tricks:
You can use the `--json` argument if you want to use a different palette creation backend, such as [Hellwal](https://github.com/danihek/hellwal): 
```bash
walcord -j ~/.cache/hellwal/colors.json
```

## KEY's syntax

KEY() can take `background`, `foreground` and numbers from 0 to 15 as the first argument:

```css
***
--bg-3: KEY(background);
--text-3: KEY(2)
***
```
you can also set the transparency of the color from 0 to 1 and use short names:
```css
***
--accent-1: KEY(F, 0.75)
--hover: KEY(br, 1)
***
```
<details>
<summary>All names of colors and they short vesions (click me)</summary>

 - `background: b`
 - `foreground: f`
 - `border: br (color 2)`
 - `text: t (color 15)`
 - `accent: a (color 13)`
 - `wallpaper: w`
</details>

If you only want values from KEY, individual colors, or HEX format, you can use the output parameters:

```css
***
--accentcolor: KEY(a).rgb_values; /* it will become just r,g,b values*/
--foo: KEY(T).r /* it will become just r value*/
***
```
<details>
<summary>All output parameters (click me)</summary>

 - `rgba` = `rgba(r, g, b, a)`
 - `rgb` = `rgba(r, g, b)`
 - `hex` = `#RRGGBB`
 - `hsl` = `hsl(h, s, l)`
 - `rgba_values` = `r,g,b,a`
 - `rgb_values` = `r,g,b`
 - `hex_values` = `RRGGBB`
 - `hsl_values` = `h, s, l`
 - `red / r` = `r`
 - `green / g` = `g`
 - `blue / b` = `b`
 - `opacity / o` = `a`
 - `hue / h` = `h`
 - `saturation / s` = `s`
 - `lightness / l` = `l`

</details>

You can also add, subtract a numeric value from a certain parameter, or invert colors with second modifiers:

```css
***
KEY(a).rgb  /* its 10, 20, 30 for example */
KEY(a).rgb.add(0, 50) /* become 60, 20, 30 */
KEY(a).rgb.invert /* become 245, 235, 225 */
***
```
<details>
<summary>All second modifiers (click me)</summary>

 - `add / a` (pos, val)
 - `sub / s` (pos, val)
 - `invert / i` no params

</details>

### ToDo
- [x] `--image` optional
- [x] `--output` argument (saving a file to a specific path and name)
- [x] simple theme
- [x] `--theme` optional (use simple theme)
- [x] windows support
- [ ] service mode (for windows users)

### Special thanks
 - [danihek/Themecord](https://github.com/danihek/Themecord): The Mastermind
 - [dylanaraps/pywal](https://github.com/dylanaraps/pywal): without it, this project would not exist

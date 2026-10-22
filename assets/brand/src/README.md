# Brand image sources

The crest images, banners and social preview in `assets/brand/` are brand assets: not open-licensed (see [NOTICE.md](../../../NOTICE.md)). The scripts in this folder are MIT code.

| File | What it does |
|---|---|
| `strip_png_metadata.py` | Copies a PNG and drops its text, time and EXIF chunks. Used on every PNG in `assets/brand/`. |
| `build_brand.py` | Lays out the banners and the social preview once and writes both the HTML render pages below and the outlined SVG banners. |
| `ttf_outlines.py` | Small TrueType reader used by `build_brand.py` to turn the text into vector outlines, so the SVGs need no font files. |
| `banner-dark.html`, `banner-light.html`, `social-preview.html` | Render pages for the PNGs (generated; edit `build_brand.py` instead). |

## Fonts (not shipped)

The render pages load fonts from a `fonts/` folder beside them. That folder is ignored by git. To rebuild, download these SIL Open Font License 1.1 files and place them in `assets/brand/src/fonts/`:

- `Oswald-VariableFont_wght.ttf` from https://github.com/googlefonts/OswaldFont
- `IBMPlexMono-Medium.ttf` and `IBMPlexMono-SemiBold.ttf` from https://github.com/IBM/plex

The title uses Oswald at its default weight (400), because `ttf_outlines.py` reads the variable font's default outlines only; the HTML uses the same weight so PNG and SVG match.

## Rebuild (PowerShell, from the repository folder)

```powershell
python assets\brand\src\build_brand.py --fonts assets\brand\src\fonts
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=1600,420 --screenshot=banner-dark-raw.png assets\brand\src\banner-dark.html
python assets\brand\src\strip_png_metadata.py banner-dark-raw.png assets\brand\banner-dark.png
```

Repeat the last two lines for `banner-light` (1600x420) and `social-preview` (1280x640). Chrome may need an absolute `file:///` URL for the page.

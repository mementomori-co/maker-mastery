# Brand image sources

The crest images, banners and social preview in `assets/brand/` are brand assets: not open-licensed (see [NOTICE.md](../../../NOTICE.md)). The scripts in this folder are MIT code.

| File | What it does |
|---|---|
| `strip_png_metadata.py` | Copies a PNG and drops its text, time and EXIF chunks. Used on every PNG in `assets/brand/`. |
| `build_brand.py` | Lays out the banners and the social preview once and writes both the HTML render pages below and the outlined SVG banners. |
| `ttf_outlines.py` | Small TrueType reader used by `build_brand.py` to turn the text into vector outlines, so the SVGs need no font files. |
| `banner-dark.html`, `banner-light.html`, `social-preview.html` | Render pages for the PNGs (generated; edit `build_brand.py` instead). |
| `clear_transparent_rgb.py` | Sets RGB to 0 under fully transparent pixels (hidden old background colour) and verifies visible pixels are byte-identical. |
| `build_family.py` | Writes the render pages for the crest-family images (see below). |
| `family-strip-*.html`, `org-avatar-500.html`, `crest-*-sign-off.html`, `crest-*-icon.html` | Render pages for the crest-family PNGs (generated; edit `build_family.py` instead). |

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

## The crest family (README images and org avatar)

`build_family.py` writes the render pages for the crest family. Each image is exported at 2x for sharp display; show it at half its pixel width.

| Output PNG | Pixels | Display width | Background |
|---|---|---|---|
| `family-strip-dark.png` | 1144x258 | 572 px | transparent, bone captions (GitHub dark mode) |
| `family-strip-light.png` | 1144x258 | 572 px | transparent, near-black captions (GitHub light mode) |
| `crest-parent-sign-off.png` | 320x247 | 160 px | transparent |
| `crest-streaming-icon.png` | 80x62 | 40 px | transparent |
| `crest-apparel-icon.png` | 80x61 | 40 px | transparent |
| `org-avatar-500.png` | 500x500 | upload as is | solid #0A0A0A |

- The strip and the sign-off draw a soft dark outline behind each crest (SVG filter `#halo`). It keeps the white "MEMENTO MORI" lettering on the parent crest readable on a white page and is invisible on a dark page.
- The org avatar scales the parent crest so its farthest visible pixel sits 10 px inside the circle inscribed in the square, so a round or rounded-square crop never cuts it.

Rebuild (PowerShell, from the repository folder). The transparent background needs `--default-background-color=00000000`:

```powershell
python assets\brand\src\build_family.py --fonts assets\brand\src\fonts
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --hide-scrollbars --force-device-scale-factor=1 --default-background-color=00000000 --window-size=1144,258 --screenshot=family-strip-dark-raw.png assets\brand\src\family-strip-dark.html
python assets\brand\src\strip_png_metadata.py family-strip-dark-raw.png assets\brand\family-strip-dark.png
```

Repeat the last two lines for each page in the table, using its pixel size as `--window-size`. Finally run `clear_transparent_rgb.py` on every transparent PNG (it sets RGB to 0 under fully transparent pixels and checks that visible pixels are unchanged).

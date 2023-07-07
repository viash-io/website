# Some info about the cheatsheets

Currently the cheatsheets were created in Inkscape.
The export to pdf happened there too.

However, we're now adding thumbnails in png for the cheatsheets, so a more standardized way of working will be required.

While there isn't an automized way yet, this is the command I used to create the thumbnails:

```sh
inkscape viash_cheatsheet_v1_0.svg --export-filename viash_cheatsheet_v1_0.png --export-type png --export-background-opacity 255 -w 280 -h 200
```

This converts the svg to png with a opaque background, and resizes to 200x280.

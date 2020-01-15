# tic80tileswap

Tools for modifying sprite sheet and tile map in a TIC-80 .lua file (requires TIC-80 pro)

The tools modify the file in-place, so take a backup before trying them out.

## replaceTile.py

usage: `python replaceTile.py [file] [oldtile] [newtile] ([tile_length = 1])`

example: `python replaceTile.py game.lua 14 185 3`

replaces instances of `[oldtile]` with `[newtile]` in MAP and swaps them around in TILES.

if tile_length is given, swaps a range {oldtile, oldtile + tile_length} with {newtile, newtile + tile_length}

## swapCols.py

usage: `python swapCols.py [infile] [col1] [col2] [tile]`

example: `python swapCols.py game.lua 1 4 152`

swaps colours `[col1]` and `[col2]` in `[tile]`.

## removeEmptiesFromMap.py

usage: `python removeEmptiesFromMap.py [file]`

goes through the tilemap in `[file]` and replaces empty (all-black) tiles with tile 0.


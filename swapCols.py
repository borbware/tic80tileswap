# -*- coding: utf-8 -*-

import sys
import argparse

if len(sys.argv) == 1:
    print("usage: python swapCols.py [infile] [col1] [col2] [tile], example: python swapCols.py game.lua 1 4 152")
    print("the program swaps colours [col1] and [col2] in [tile].")
    exit()

filename = sys.argv[1]
col1_str = sys.argv[2]
col2_str = sys.argv[3]
tile_str = sys.argv[4]

def intToHex(n):
    hexa = str(hex(n))[2:]   # [2:] gets rid of "0x"
    return hexa

def swap(col1, col2, tileline):
    newline = ""
    for i in range(0, len(tileline)):
        if tileline[i:i+1] == col1:
            newline += col2
        else:
            newline += tileline[i:i+1]
    return newline

def swapCols(tile_str, col1_str, col2_str, file_lines):

    tile = int(tile_str)
    tile_str = tile_str.zfill(3) #"5" --> "005"

    col1 = intToHex(int(col1_str))
    col2 = intToHex(int(col2_str))

    print("swap colours {} and {} in tile {}".format(col1,col2,tile_str))

    readtiles = False

    for line in file_lines:
        if line.startswith("-- <TILES>"):
            print("tiles starts!")
            readtiles = True
            continue
        elif line.startswith("-- </TILES>"):
            print("tiles ends!")
            readtiles = False
            continue
        if readtiles:
            tilenumber = int(line[3:6])
            if tilenumber == tile:
                tileline = line[7:]

                tileline = swap(col1, "g", tileline)
                tileline = swap(col2, col1, tileline)
                tileline = swap("g", col2, tileline)

                file_lines[file_lines.index(line)] = line[:7] + tileline

    return file_lines

with open(filename) as file:
    lines = file.readlines()
    edited_lines = swapCols(tile_str, col1_str, col2_str, lines)

with open(filename,"w") as file:
    for line in edited_lines:
        file.write(line)

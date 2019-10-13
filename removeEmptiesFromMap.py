# -*- coding: utf-8 -*-

import sys
import argparse

if len(sys.argv) == 1:
    print("usage: python removeEmptiesFromMap.py [file]")
    print("the program goes through the tilemap in [file] and replaces empty (all-black) tiles with tile 0.")
    exit()

filename = sys.argv[1]
oldtile_str = sys.argv[2]
newtile_str = sys.argv[3]

def intToHex(n):
    hexa = str(hex(n))[2:]   # [2:] gets rid of "0x"
    hexa = hexa[1:]+hexa[:1] #damn you nesbox with your endianness shenanigans
    hexa = hexa.ljust(2, '0')  #"7" --> "70"
    return hexa

def cleanMapOfEmptyTiles(file_lines):
    listOfNonEmptyTiles = [] 
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
            listOfNonEmptyTiles.append(intToHex(tilenumber))
    print("{} / 255 tiles non-empty".format(len(listOfNonEmptyTiles)))
    for i in range(0,256):
        if intToHex(i) in listOfNonEmptyTiles:
            print intToHex(i),
        else:
            print "__",
        if i%16 == 15:
            print "\n",

    readmap = False
    for line in file_lines:
        if line.startswith("-- <MAP>"):
            print("map starts!")
            readmap = True
            continue
        elif line.startswith("-- </MAP>"):
            print("map ends!")
            readmap = False
            continue
        if readmap:
            newline = ""
            mapline = line[7:]
            for i in range(0, len(mapline), 2):
                if (not mapline[i:i+2] in listOfNonEmptyTiles) and (not mapline[i:i+2] == "\n"):
                    newline += "00"
                else:
                    newline += mapline[i:i+2]
            file_lines[file_lines.index(line)] = line[:7] + newline
            continue

    return file_lines

with open(filename) as file:
    lines = file.readlines()
    edited_lines = cleanMapOfEmptyTiles(lines)

with open(filename,"w") as file:
    for line in edited_lines:
        file.write(line)

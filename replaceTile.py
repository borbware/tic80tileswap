# -*- coding: utf-8 -*-

import sys
import argparse

def intToHex(n):
    hexa = str(hex(n))[2:]   # [2:] gets rid of "0x"
    hexa = hexa[1:]+hexa[:1] #damn you nesbox with your endianness shenanigans
    hexa = hexa.ljust(2, '0')  #"7" --> "70"
    return hexa

def swapTiles(oldtile, newtile, file_lines):
    
    oldtile_str=str(oldtile)
    newtile_str=str(newtile)

    oldtile = int(oldtile_str)
    newtile = int(newtile_str)

    oldtile_str = oldtile_str.zfill(3) #"5" --> "005"
    newtile_str = newtile_str.zfill(3)

    oldtile_hex = intToHex(oldtile)
    newtile_hex = intToHex(newtile)

    print("(tiles as reversed hex, as they appear in .lua):")
    print(oldtile_hex + " -> " + newtile_hex)

    readtiles = False
    oldtile_newline = False
    oldtile_oldline = False
    newtile_newline = False
    newtile_oldline = False

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

            if tilenumber < oldtile:
                lastOldIndex = file_lines.index(line)
            if tilenumber < newtile:
                lastNewIndex = file_lines.index(line)

            if tilenumber == oldtile:
                oldtile_oldline = line
                oldtile_newline = line[:3] + newtile_str + line[6:]
            elif tilenumber == newtile:
                newtile_oldline = line
                newtile_newline = line[:3] + oldtile_str + line[6:]

    if newtile_oldline and oldtile_oldline:
        print("swap new and old")
        print(file_lines.index(newtile_oldline))
        file_lines[file_lines.index(newtile_oldline)] = oldtile_newline
        file_lines[file_lines.index(oldtile_oldline)] = newtile_newline

        edited_lines = changeTileInMAP(oldtile_hex,"gg",file_lines)
        edited_lines = changeTileInMAP(newtile_hex,oldtile_hex,edited_lines)
        edited_lines = changeTileInMAP("gg",newtile_hex,edited_lines)

    elif oldtile_oldline:
        print("newtile is an empty tile! insert oldtile after index {} and remove it from its original location".format(lastNewIndex))
        file_lines.insert(lastNewIndex, oldtile_newline)
        file_lines.pop(file_lines.index(oldtile_oldline))

        edited_lines = changeTileInMAP(newtile_hex,"00",file_lines)
        edited_lines = changeTileInMAP(oldtile_hex,newtile_hex,edited_lines)

    elif newtile_oldline:
        print("oldtile is an empty tile! insert newtile after index {} and remove it from its original location".format(lastOldIndex))
        file_lines.insert(lastOldIndex, newtile_newline)
        file_lines.pop(file_lines.index(newtile_oldline))

        edited_lines = changeTileInMAP(oldtile_hex,"00",file_lines)
        edited_lines = changeTileInMAP(newtile_hex,oldtile_hex,edited_lines)

    return edited_lines

def changeTileInMAP(oldtile,newtile,file_lines):
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
                if mapline[i:i+2] == oldtile:
                    newline += newtile
                    print(oldtile + " replaced with " + newtile)
                else:
                    newline += mapline[i:i+2]
            file_lines[file_lines.index(line)] = line[:7] + newline
            continue
    return file_lines

if len(sys.argv) == 1:
    print("usage: python replaceTile.py [file] [oldtile] [newtile] ([tile_length = 1]), example: python replaceTile.py game.lua 14 185 3")
    print("the program replaces instances of [oldtile] with [newtile] in MAP and swaps them around in TILES.")
    print("if tile_length is given, swaps a range {oldtile, oldtile + tile_length} with {newtile, newtile + tile_length}") 
    exit()

filename = sys.argv[1]
oldtile_str = sys.argv[2]
newtile_str = sys.argv[3]
oldtile = int(oldtile_str)
newtile = int(newtile_str)

try:
    tile_length = int(sys.argv[4])
except:
    tile_length = 1

with open(filename) as file:
    edited_lines = file.readlines()

    for i in xrange(tile_length):
        edited_lines = swapTiles(oldtile+i,newtile+i,edited_lines)

with open(filename,"w") as file:
    for line in edited_lines:
        file.write(line)

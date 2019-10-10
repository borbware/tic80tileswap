# -*- coding: utf-8 -*-

import sys

if len(sys.argv) == 1:
    print("usage: python replaceTile.py infile outfile oldtile newtile")
    print("the program replaces instances of [oldtile] with [newtile] in MAP and TILES.")
    exit()

filename = sys.argv[1]
outfilename = sys.argv[2]
oldtile_str = sys.argv[3]
newtile_str = sys.argv[4]

def changeTileInTILES(oldtile_str, newtile_str, file_lines):

    oldtile = int(oldtile_str)
    newtile = int(newtile_str)

    oldtile_str = oldtile_str.zfill(3)               #"5" --> "005"
    newtile_str = newtile_str.zfill(3)

    oldtile_hex = str(hex(oldtile))[2:]
    newtile_hex = str(hex(newtile))[2:]
    oldtile_hex = oldtile_hex[1:]+oldtile_hex[:1]    #damn you nesbox with your endianness shenanigans
    newtile_hex = newtile_hex[1:]+newtile_hex[:1]
    oldtile_hex = oldtile_hex.ljust(2, '0')          #"7" --> "70"
    newtile_hex = newtile_hex.ljust(2, '0')

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
        print("newtile is an empty tile! insert oldtile in lastNewIndex = {} and emove it from its original location".format(lastNewIndex))
        file_lines.insert(lastNewIndex, oldtile_newline)
        file_lines.pop(file_lines.index(oldtile_oldline))

        edited_lines = changeTileInMAP(newtile_hex,"00",file_lines)
        edited_lines = changeTileInMAP(oldtile_hex,newtile_hex,edited_lines)

    elif newtile_oldline:
        print("oldtile is an empty tile! insert newtile in lastOldIndex = {} and remove it from its original location".format(lastOldIndex))
        file_lines.insert(lastOldIndex, newtile_newline)
        file_lines.pop(file_lines.index(newtile_oldline))

        edited_lines = changeTileInMAP(oldtile_hex,"00",file_lines)
        edited_lines = changeTileInMAP(newtile_hex,oldtile_hex,edited_lines)

    return edited_lines

def changeTileInMAP(oldtile,newtile,file_lines):
    newfile = []
    readmap = False
    for line in file_lines:
        if line.startswith("-- <MAP>"):
            print("map starts!")
            readmap = True
            newfile.append(line)
            continue
        elif line.startswith("-- </MAP>"):
            print("map ends!")
            readmap = False
            newfile.append(line)
            continue
        if readmap:
            newline = ""
            mapline = line[7:]
            for i in range(0, len(mapline), 2):
                if mapline[i:i+2] == oldtile:
                    newline+=newtile
                    print(oldtile+" replaced with "+newtile)
                else:
                    newline+=mapline[i:i+2]
            newfile.append(line[:7]+newline)
            continue
        newfile.append(line)
    return newfile

with open(filename) as file:
    lines = file.readlines()
    #edited_lines = changeTileInMAP(oldtile_hex,newtile_hex,lines)
    edited_lines = changeTileInTILES(oldtile_str,newtile_str,lines)

with open(outfilename,"w") as file:
    for line in edited_lines:
        file.write(line)
"""
 *****************************************************************************
   FILE:        chess-v1.py

   AUTHOR: Eva Nolan

   DATE: October 2021

   DESCRIPTION: Reads game results file, organizes data into a CSV

 *****************************************************************************
"""

import csv
from converter.pgn_data import PGNData


def parseline(line):
    """ read line, distinguish column category and column info. Return cat & data"""
    """ category is one word, data is in single quotes """
    if line[0] != '[':
        return

    contents = line[1:-2]
    category = contents.split()[0]
    data_pos = contents.find(' ') + 2
    data = contents[data_pos:-1]
    return (category, data)

def addcolnames(file, writer, lines):
    writer = csv.writer(file)
    colnames = []
    start = 0
    line = lines[start]
    # find first nontrivial line in doc
    while line[start][0] != '[':
        start += 1
    # add all categories to a list
    while lines[start][0] == '[':
        contents = lines[start][1:-2]
        # print(start, contents)
        category = contents.split()[0]
        colnames.append(category)
        start += 1
    # add the categories to the csv
    writer.writerow(tuple(colnames))

def adddata(file, writer, lines):
    rowdata = []
    for line in lines:
        # if line containing game data, add data to row
        if line[0] == '[':
            data = line[line.find(" ")+2 : -3]
            rowdata.append(data)
            # if last item in row, add to csv and clear rowdata []
            if "Termination" in line:
                writer.writerow(tuple(rowdata))
                rowdata = []


def adddataprint(file, writer, lines):
    """ performs the same as adddata() but also prints to stdout what game
    number is being processed so you can track progress"""
    rowdata = []
    gamecounter = 0
    for line in lines:
        # if line containing game data, add data to row
        if line[0] == '[':
            data = line[line.find(" ")+2 : -3]
            rowdata.append(data)
            # if last item in row, add to csv and clear rowdata []
            if "Termination" in line:
                writer.writerow(tuple(rowdata))
                rowdata = []
                gamecounter += 1
                print(gamecounter)

def main():
    """ The main function. """
    # save text file as lines
    with open('chessdata.pgn') as tfile:
        lines = tfile.readlines()

    # lines = lines[0:200] # to test on shorter amounts of data, uncomment this
    # clear previous data from csv, then open for appending
    dfile = open("chess-data.csv", "w+" )
    dfile = open("chess-data.csv", "a", newline = "" )
    writer = csv.writer(dfile)
    # add column names and data to csv
    addcolnames(dfile, writer, lines)
    adddata(dfile, writer, lines)
    # uncomment this line if you want to see what line number you're on:
    # adddataprint(dfile, writer, lines)



if __name__ == '__main__':
    main()

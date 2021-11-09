"""
 *****************************************************************************
   FILE:        chess-v1.py

   AUTHOR: Eva Nolan

   DATE: November 08 2021

   DESCRIPTION: Reads game results file, organizes data into a CSV

 *****************************************************************************
"""

import csv
from converter.pgn_data import PGNData
CSVNAME = "chess-data2.csv"
ELOSNAME = "playerelo.csv"
# source is white, target is black
COLNAMES = ["Source", "Target", "WhiteElo", "BlackElo", "Event", "Opening", "Termination"]
MINELO = 1800
ELODICT = {}
BUCKETSIZE = 40

def addcolnames(file, writer, lines):
    writer = csv.writer(file)
    writer.writerow(tuple(COLNAMES))

def adddata(file, writer, lines):
    rowdict = {}
    categories = ["[White", "[Black", "[WhiteElo", "[BlackElo", "[Event", "[Opening", "[Termination"]
    for cat in categories:
        rowdict[cat] = ""
    for line in lines:
        if line[0] == "[":
            cat = line.split()[0]
            if cat in categories:
                data = line[line.find(" ")+2 : -3]
                rowdict[cat] = data

            if cat == "[Termination":
                rowdata = list(rowdict.values())
                if "?" not in rowdata and "0" not in rowdata:
                    if int(rowdict["[WhiteElo"]) > MINELO and int(rowdict["[BlackElo"]) > MINELO:
                        rowdata = SimpleEvent(rowdata)
                        writer.writerow(rowdata)

def SimpleEvent(rowdata):
    """ alter the row data to be labeled with a simplified version of the event type"""
    # index 4 contains the event type as a string
    event = rowdata[4]
    if "tournament" in event:
        rowdata[4] = "tournament "
    else:
        rowdata[4] = ""
    if "Blitz" in event:
        rowdata[4] += "Blitz"
        # print("Blitz")
    elif "Bullet" in event:
        rowdata[4] += "Bullet"
        # print('Bullet')
    elif "Classical" in event:
        rowdata[4] += "Classical"
    elif "Correspondence" in event:
        rowdata[4] += "Correspondence"
    else:
        print("none: ", event)
    return rowdata

def getelo(CSVNAME):
    """ open data CSV, get players and their elo for each game. Put player's
    average elo into dictionary """
    with open(CSVNAME, newline='') as dataCSV:
        reader = csv.DictReader(dataCSV)
        for row in reader:
            # print(row["White"], row["WhiteElo"], row["BlackElo"], row["Black"])
            (Wname, Welo, Bname, Belo) = (row["Source"], row["WhiteElo"], row["Target"], row["BlackElo"])
            # print(Wname, Welo, Bname, Belo)
            addtodict(Wname, Welo)
            addtodict(Bname, Belo)
    avgelos()
    efile = open(ELOSNAME, "w+" )
    efile = open(ELOSNAME, "a", newline = "" )
    writer = csv.writer(efile)
    writer.writerow(('ID', 'elo', 'bucket'))
    for key in ELODICT.keys():
        # add row with player name, avg elo, and elo bucket
        writer.writerow((key, ELODICT[key][0], ELODICT[key][1]))
        # print("adding: ", key, ELODICT[key])
    efile.close()
    # add elodict to csv

def avgelos():
    # bucket by 10s: avg // 10 * 10
    for key in ELODICT.keys():
        sum = 0
        for elo in ELODICT[key]:
            sum += elo
        avg = sum / len(ELODICT[key])
        # bucket rounds down to nearest bucketsize
        bucket = (avg // BUCKETSIZE) * BUCKETSIZE
        ELODICT[key] = [avg, bucket]

def addtodict(name, elo):
    """ update list associated with player to include elo"""
    if name in ELODICT.keys():
        elolist = ELODICT.get(name)
        elolist.append(int(elo))
    else:
        elolist = [int(elo)]
    ELODICT[name] = elolist

def main():
    """ The main function. """

    # save text file as lines
    print("reading ... ")
    with open('chessdata.pgn') as tfile:
        lines = tfile.readlines()
        # lines = []
        # for i in range(300):
        #     lines.append(tfile.readline())

    # clear previous data from csv, then open for appending
    dfile = open(CSVNAME, "w+" )
    dfile = open(CSVNAME, "a", newline = "" )
    writer = csv.writer(dfile)

    print('adding data ... ')
    # add column names and data to csv
    addcolnames(dfile, writer, lines)
    adddata(dfile, writer, lines)

    print('averageing elos ... ')
    getelo(CSVNAME)

    print('done')


if __name__ == '__main__':
    main()

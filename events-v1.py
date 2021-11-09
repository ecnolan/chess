"""
 *****************************************************************************
   FILE:        events-v1.py

   AUTHOR: Eva Nolan

   DATE: November 08 2021

   DESCRIPTION: reads in full csv, sorts data into new CSVs based on event type

 *****************************************************************************
"""

import csv
from converter.pgn_data import PGNData
CSVNAME = "chess-data2.csv"
ELOSNAME = "playerelo.csv"
ELODICT = {}
FILESMADE = []
# source is white, target is black
COLNAMES = ["Source", "Target", "WhiteElo", "BlackElo", "Event", "Opening", "Termination", "Result"]
BUCKETSIZE = 40


def grabrows(filename):
    """ returns list of rows from CSV """
    rows = []
    with open(filename, newline='') as dataCSV:
        reader = csv.reader(dataCSV)
        for row in reader:
            rows.append(row)
    return(rows)

def sortevent(rows, datatype):
    """ for each row, add row to event-based list. Write list to CSV """
    # goal: nested list. Contains four lists, each list contains rows
    # [[rows of type 1] [rows of type 2] [ rows of type 3] ... ]
    eventtypes = ["tournament", "Blitz", "Bullet", "Classical", "Correspondence"]
    # ie allevents[0] = list containing rows of tournament event data
    allevents = []
    for _ in eventtypes:
        allevents.append([])
    for row in rows:
        if eventtypes[0] in row[4]:
            allevents[0].append(row)
        else:
            for i in range(1,4):
                if eventtypes[i] in row[4]:
                    allevents[i].append(row)
                    break

    for i in range(len(allevents)):
        # datatype = "-data" or "-elo"
        # open file using event name
        filename = eventtypes[i] + datatype + ".csv"
        print(filename)
        FILESMADE.append(filename)
        file = open(filename, "w+" )
        file = open(filename, "a", newline = "" )
        writer = csv.writer(file)
        # for every event, still write first row - contains column names
        writer.writerow(rows[0])
        for row in allevents[i]:
            writer.writerow(row)
        file.close()

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
    efile = open(CSVNAME[:-8] + "elo.csv", "w+" )
    print(CSVNAME[:-8] + "elo.csv")
    efile = open(CSVNAME[:-8] + "elo.csv", "a", newline = "" )
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
    rows = grabrows(CSVNAME)
    sortevent(rows, "-data")
    for file in FILESMADE:
        getelo(file)
    # rows = grabrows(ELOSNAME)
    # sortevent(rows, "-elo")

if __name__ == '__main__':
    main()

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
# source is white, target is black
COLNAMES = ["Source", "Target", "WhiteElo", "BlackElo", "Event", "Opening", "Termination"]

def grabrows(filename):
    """ returns list of rows from CSV """
    rows = []
    with open(filename, newline='') as dataCSV:
        reader = csv.reader(dataCSV)
        for row in reader:
            rows.append(row)
    return(rows)

def sortevent(rows):
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
        # open file using event name
        filename = eventtypes[i] + "-data.csv"
        print(filename)
        file = open(filename, "w+" )
        file = open(filename, "a", newline = "" )
        writer = csv.writer(file)
        # for every event, still write first row - contains column names
        writer.writerow(rows[0])
        for row in allevents[i]:
            writer.writerow(row)
        file.close()


def main():
    """ The main function. """
    rows = grabrows(CSVNAME)
    sortevent(rows)

if __name__ == '__main__':
    main()

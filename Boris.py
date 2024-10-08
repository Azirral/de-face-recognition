import csv
import os
from datetime import datetime
import math

def print_table(table):
    for row in table:
        print(row)

def create_table(tab1, tab2, tab3):           #optimized version
    result_tab = []

    emotions = ['Unknown', 'Happy', 'Sad', 'Scared', 'Disgusted', 'Surprised', 'Angry']

    for row1, row2, row3 in zip(tab1, tab2, tab3):
        sum_rows = [int(a) + int(b) + int(c) for a, b, c in zip(row1[1:], row2[1:], row3[1:])]

        max_sum = max(sum_rows[1:], default=0)
        index = sum_rows.index(max_sum) if max_sum > 1 else -1  # Indeks od 1, jeśli suma jest większa niż 0, w przeciwnym razie -1

        if 0 <= index < len(emotions):
            result_tab.append([row1[0], emotions[index]])
        else:
            result_tab.append([row1[0], 'None'])
    return result_tab


def fill_table(table,csvreader):
    seconds = 0
    stop = 0
    for row in csvreader:
        row[0] = int(row[0].split('.')[0])
        if seconds <= row[0] and stop == 0:     #fill table with missing seconds
            for i in range(0,row[0]):
                table.append([i, '0', '0', '0', '0', '0', '0', '0'])
                seconds+=1
            stop = 1
            table.append(row)
        else:
            table.append(row)


def csv_files_reader(base_path):#read csv files from Boris
    index = ['I','II','III']
    tab1 = []
    tab2 = []
    tab3 = []

    if os.path.exists(base_path):

        for i in index:
            for file_name in os.listdir(base_path+i):
                file_path = os.path.join(base_path+i, file_name)

                with open(file_path, 'r') as file:
                    csvreader = csv.reader(file)
                    header = next(csvreader)

                    if i == 'I':
                        fill_table(tab1,csvreader)
                    elif i == 'II':
                        fill_table(tab2,csvreader)
                    elif i == 'III':
                        fill_table(tab3,csvreader)
    else:
        print(f"File path {base_path} doesn't exist.")

    large_table = max([tab1, tab2, tab3], key=len)

    for tab in [tab1, tab2, tab3]:
        if len(tab) < len(large_table):
            diff = len(large_table) - len(tab)

            if len(tab) == 0:
                sec=0
                for sec in range(len(large_table)):
                    tab.append([sec, '0', '0', '0', '0', '0', '0', '0'])
            else:
                sec = tab[-1][0]      #latest second in table
                for sec in range(tab[-1][0]+1, len(large_table)):
                    tab.append([sec, '0', '0', '0', '0', '0', '0', '0'])

    return create_table(tab1,tab2,tab3)

result_table_BORIS = csv_files_reader('C:/Users/oskik/InżynierkaSandbox/S01_boris/C01/Analysis/BORIS/')
print(result_table_BORIS)

#!/usr/bin/python3
#   Copyright (C) 2019 Lucas Lee Jing Yi
#   Author: Lucas Lee Jing Yi <lucasljyy@gmail.com>
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
import csv
import string
import tkinter as tk
from tkinter import filedialog
import time
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
#This script's function is to provide KNIME with usable data
#some things are such as String manipulation, data conversion is done much faster on python since 
#I have some experience in doing so. With python I have a very low level control of the data and I am able to fully control
#absolutely everything I am doing with it. It reduces the chance of erroneous data down the line and helps us(the team) understand
#the data preperation process better. While KNIME is a powerful tool for data preperation, python is far better for our usecase.
#We will still use KNIME for higher level data preperation such as infering a new column from all the data.
#TL;DR Python is just better than KNIME at data preperation at this level.
def compareAndConvert(a, b, value, col, row):
    #Function to compare values
    if(value == a):
        return 1;
    elif(value == b):
        return 0;
    else:
        #if none of the cases are true, it must be a spelling mistake
        print("Erroneous Data! at ROW: "+str(row)+" under "+col)
        #return and preserve original value for manual correction
        return value;
def storeMax(num):
    #function to store the baseline printer
    #Since some values we are comparing are converted from Strings, and can be erroneously entered(we are humans after all)
    #add a try-except to catch the exception that inevitably occurs.
    try:
        if(int(row[num]) > int(baselinePrinter[num])):
            baselinePrinter[num]=int(row[num])
    except:
        pass
with open(file_path, encoding='utf-8') as f:
    start=time.time()
    data = list(csv.reader(f))
    length = len(data)-1;
    sortedData = [];
    baselinePrinter=["baseline", "baseline","", 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 5, "", "", ""];
    for i, row in enumerate(data):
        #sort out empty rows using cost row as all of those are filled
        #printer resolution also should not be empty
        if(row[1] and row[12] and row[4] and i!=0):
            #lastly, filter out headers, except those from the first row, of course.
            if(row[0]!="Company"):
                #remove commas in numbers
                row[4]=float(row[4].replace(",",""));
                if(row[9] != ''):
                    row[9]=float(row[9].replace(",",""));
                #round catridge cost, yield and remove commas 
                if(row[15]):
                    row[15]=int(round(float(row[15])))
                if(row[14] != ''):
                    row[14]=float(row[14].replace(",",""));
                #round the values for cost
                #my teammate decided it was a good idea to add '?' for null data.
                #add an if statement to deal with that BS
                if(row[12]!='?'):
                    row[12]=int(round(float(row[12])))
                else:
                    row[12]=''
                #capitalise some of the data to standardise it for easy sorting
                row[2] = string.capwords(row[2])
                row[3] = string.capwords(row[3])
                row[5] = string.capwords(row[5])
                row[11] = string.capwords(row[11])
                #Change Color to the correct spelling
                if(row[5] == "Color"):
                    #change to the correct spelling
                    row[5] = "Colour"
                #
                #
                #We are changing printing colur to numbers as it affects the printer performance value
                row[5]=compareAndConvert("Colour", "Monochrome", row[5], "Printing_Colour", i+1)
                #
                #
                #Manual and Auto will play a part in printer performance
                #convert it to numbers for better calculation
                row[3]=compareAndConvert("Manual", "Auto", row[3], "Printing_Sides", i+1)
                #
                #
                #Wired and Wireless will play a part in printer performance
                #convert it to numbers for better calculation
                row[11]=compareAndConvert("Wireless", "Wired", row[11], "Connectivity", i+1)
                #
                #
                #We're doing nothing here, just checking spelling
                if(row[2] != "Inkjet" and row[2] != "Laser"):
                    print("Erroneous Data! at ROW: "+str(i+1)+" under Printing_Method")
                #
                #
                #We will now write values to the baseline printer if it is higher than the previous value
                #So that it will have the highest values, as intended for a baseline.
                storeMax(4);
                storeMax(5);
                storeMax(6);
                storeMax(7);
                storeMax(8);
                storeMax(9);
                storeMax(10);
                storeMax(11);
            
                #
                #
                #Lastly, we will remove the brand names from the Model names.
                if(row[0] in row[1]):
                    #Replace the space in front of it with an empty string
                    #So the model name does not look retarded
                    row[1]=row[1].replace(row[0]+" ","");
                #
                #
                #DO NOT INSERT DUPLICATE PRINTER
                if(row[1] not in sortedData):
                    sortedData.append(row);
            else:
                print("Removing Row "+str(i+1));
        elif(i==0):
            #always append the first row
            sortedData.append(row);
        else:
            print("Removing Row "+str(i+1));
        #
        #
        #Check if last in list, then append baseline printer as the very last printer.
        if(i==length):
            sortedData.append(baselinePrinter);
    with open("data_sorted.csv", "w") as w:
        csv.writer(w).writerows(sortedData);
        end=time.time()
        print("Time elapsed: "+str(end-start));

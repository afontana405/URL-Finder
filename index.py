#Python Standard Libraries
import sys
import os
import re
from binascii import hexlify

# Python 3rd Party Libraries
from prettytable import PrettyTable     # pip install prettytable

# Local Functions
def SearchTextForURL(fileChunk): #uses Regex to search binary text for URLs
    urlPattern = re.compile(rb'\w+:\/\/[\w@][\w.:@]+\/?[\w\.?=%&=\-@/$,]*')
    matches = urlPattern.findall(fileChunk)
    return matches

def ProcessFile(largeFile): # Breaks large files into chunks to be better processed
    try:
        with open(largeFile, 'rb') as targetFile:
            foundURLs = []
            while True:
                fileChunk = targetFile.read(65535) #65535 byte chunks as per assignment
                fileChunk = fileChunk.lower()  # broaden search
                if fileChunk:  # if we still have data
                    matches = SearchTextForURL(fileChunk) #calls function to search chunk for URLs
                    foundURLs += matches #adds matches to found URL list
                else: #file has been processed
                    return(foundURLs)
    except Exception as err:
        print("Error: "+ str(err))
        
def FormatData(foundURLs):
    setofURLs = set(foundURLs)
    URLdictionary = {}  # Create a dictionary to keep track of the URL hits
    for eachURL in setofURLs:
        URLdictionary[eachURL] = 0
    for eachURL in foundURLs: #cycles thru every URL found
        URLdictionary[eachURL] += 1 #counts each occurance of URL
    return URLdictionary

def CreateTable(URLdictionary):
    tbl = PrettyTable(['OCCURS', 'URL']) # Formating table
    tbl.align = "l" 
    for eachURL in URLdictionary: #cycles thru URLS and # of occurancies to fill in table
        tbl.add_row( [ URLdictionary[eachURL], eachURL ] )
    tbl = tbl.get_string(sortby="OCCURS", reversesort=True) # sorts table by most occurances to least   
    print(tbl)

# Main Entry
try:
    # Prompt user for a large file    
    largeFile = input("Enter the name of a large File: ")

    if os.path.isfile(largeFile):  # Verify file is real
        foundURLs = ProcessFile(largeFile)
        URLdictionary = FormatData(foundURLs)
        CreateTable(URLdictionary)
        
    else:
        print(largeFile, "is not a valid file")
        sys.exit("Script Aborted")
        
except Exception as err:
    sys.exit("\nException: "+str(err)+ "Script Aborted")
    
print("\nFile Processed ... Script End")
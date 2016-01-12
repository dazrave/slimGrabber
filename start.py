# global imports
import time
import os
import glob
import os.path
import shutil
import sys

# custom imports
import config
import functions

from config import mainPath, moviePath, showPath, recyclePath, rgUser, rgPass, fileBot
config = [mainPath, moviePath, showPath, recyclePath, rgUser, rgPass, fileBot]

# get manual settings
i = 0

# Set variables
timeStamp = time.strftime('%d/%m/%Y %I:%M:%S')


#while len(sys.argv) > i:
    #videoType = sys.argv[1]
    #i = i + 1
    #if i > 1:
    #    downloadAmount = sys.argv[2]
videoType = False
downloadAmount = False


def startProcess(videoType, downloadAmount, config):
    #setup
    mainPath = config[0]
    moviePath = config[1]
    showPath = config[2]
    recyclePath = config[3]
    # get auto settings
    downloadPath = mainPath+'/downloads/'+videoType+'s'
    if moviePath is '':
        moviePath = mainPath+'/movies'
    if showPath is '':
        showPath = mainPath+'/shows'
    if recyclePath is '':
        recyclePath = mainPath+'/recycle/'+videoType+'s'
    os.makedirs(downloadPath)
    # Start process
    print('[Process started]')
    # Set varibles needed
    if videoType is 'movie':
        mediaPath = moviePath
    elif videoType is 'show':
        mediaPath = showPath
    # Count the number of links avalible to download
    print('[Checking '+videoType+' links]')
    linkAmount = functions.countLinks(videoType)
    # Make sure everything is downloaded if no manual amount set
    if downloadAmount is False:
        downloadAmount = linkAmount
    # Loop over downloadable links
    processedAmount = 0
    while True:
        # print('[Download started]')
        downloadProcess = functions.downloadFile(videoType, downloadPath, mainPath)
        processedAmount = processedAmount + 1
        #  print ('[ '+processedAmount ' of ' linkAmount ' downloaded]')
        if processedAmount is downloadAmount:
            print('[Done]')
            break
        if downloadProcess is False:
            break
    # unzip downloaded files
    rarExists = functions.unzipFile(videoType, downloadPath)
    # format filenames
    functions.renameFile(downloadPath)
    # check for duplicates
    functions.moveFiles(downloadPath, mediaPath, recyclePath)
    # move downloaded videos
    # record to logs
    shutil.rmtree(downloadPath)
    print('[End of '+videoType+'s]')

# Add Timestamp to 'done.txt'
timeStamp = time.strftime('%d/%m/%Y %I:%M:%S')
with open(mainPath+'/downloads/done.txt', 'a') as myfile:
    print ('[Writing to log]')
    myfile.write('\n')
    myfile.write('====== '+timeStamp+' ======\n')

# start the correct process
if videoType:
    downloadResult = startProcess(videoType, downloadAmount, config)
else:
    showResult = startProcess('show', downloadAmount, config)
    movieResult = startProcess('movie', downloadAmount, config)

# Add Timestamp to 'done.txt'
timeStamp = time.strftime('%d/%m/%Y %I:%M:%S')
with open(mainPath+'/downloads/done.txt', 'a') as myfile:
    myfile.write('###### '+timeStamp+' ######\n')

print ('[Finished]')

# Was the downloading successfull?

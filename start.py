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

from config import mainPath, moviePath, showPath, filePath, recyclePath, rgUser, rgPass, fileBot
config = [mainPath, moviePath, showPath, recyclePath, rgUser, rgPass, fileBot]

# get manual settings
i = 0

# Set variables
timeStamp = time.strftime('%d/%m/%Y %I:%M:%S')


#while len(sys.argv) > i:
    #fileType = sys.argv[1]
    #i = i + 1
    #if i > 1:
    #    downloadAmount = sys.argv[2]
fileType = False
downloadAmount = False


def startProcess(fileType, downloadAmount, config):
    #setup
    mainPath = config[0]
    moviePath = config[1]
    showPath = config[2]
    filePath = config[3]
    recyclePath = config[4]
    # get auto settings
    downloadPath = mainPath+'/downloads/'+fileType+'s'
    if moviePath is '':
        moviePath = mainPath+'/movies'
    if showPath is '':
        showPath = mainPath+'/shows'
    if filePath is '':
        filePath = mainPath+'/files'
    if recyclePath is '':
        recyclePath = mainPath+'/recycle/'+fileType+'s'
    tempFolder = os.path.exists(downloadPath)
    os.chdir(mainPath+'/downloads')
    if tempFolder:
        timeStamp = time.strftime('%d%m%Y%I%M%S')
        os.rename(fileType+'s', fileType+'s_'+timeStamp)
    os.makedirs(downloadPath)
    # Start process
    print('-----------------------------=['+fileType+' Process started]')
    # Set varibles needed
    if fileType is 'movie':
        mediaPath = moviePath
    elif fileType is 'show':
        mediaPath = showPath
    elif fileType is 'file':
        mediaPath = filePath
    # Count the number of links avalible to download
    print('[Checking '+fileType+' links]')
    linkAmount = functions.countLinks(fileType)
    # Make sure everything is downloaded if no manual amount set
    if downloadAmount is False:
        downloadAmount = linkAmount
    # Loop over downloadable links
    processedAmount = 0
    while True:
        # print('[Download started]')
        downloadProcess = functions.downloadFile(fileType, downloadPath, mainPath)
        processedAmount = processedAmount + 1
        #  print ('[ '+processedAmount ' of ' linkAmount ' downloaded]')
        if processedAmount is downloadAmount:
            print('[Done]')
            break
        if downloadProcess is False:
            break
    if fileType is not 'file':
        if downloadProcess is not False:
            # unzip downloaded files
            rarExists = functions.unzipFile(fileType, downloadPath)
            # format filenames
            functions.renameFile(downloadPath)
            # check for duplicates
            functions.moveFiles(downloadPath, mediaPath, recyclePath)
    # record to logs
    shutil.rmtree(downloadPath)
    print('[End of '+fileType+'s]')

# Add Timestamp to 'done.txt'
timeStamp = time.strftime('%d/%m/%Y %I:%M:%S')
with open(mainPath+'/downloads/done.txt', 'a') as myfile:
    print ('[Writing to log]')
    myfile.write('\n')
    myfile.write('====== '+timeStamp+' ======\n')

# start the correct process
if fileType:
    downloadResult = startProcess(fileType, downloadAmount, config)
else:
    showResult = startProcess('show', downloadAmount, config)
    movieResult = startProcess('movie', downloadAmount, config)
    fileResult = startProcess('file', downloadAmount, config)

# Add Timestamp to 'done.txt'
timeStamp = time.strftime('%d/%m/%Y %I:%M:%S')
with open(mainPath+'/downloads/done.txt', 'a') as myfile:
    myfile.write('###### '+timeStamp+' ######\n')

print ('[Finished]')

# Was the downloading successfull?

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

from config import mainPath, moviePath, showPath, musicPath, filePath, recyclePath, rgUser, rgPass, fileBot
config = [mainPath, moviePath, showPath, musicPath, filePath, recyclePath, rgUser, rgPass, fileBot]

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

    # Start process
    print('-----------------------------=['+fileType+' Process started]')
    #setup
    mainPath = config[0]
    moviePath = config[1]
    showPath = config[2]
    musicPath = config[3]
    filePath = config[4]
    recyclePath = config[5]
    # get auto settings
    if fileType is not 'music':
        fileType = fileType+'s'

    if moviePath is '':
        moviePath = mainPath+'/movies'
    if showPath is '':
        showPath = mainPath+'/shows'
    if musicPath is '':
        musicPath = mainPath+'/music/Loose'
    if filePath is '':
        filePath = mainPath+'/files'
    if recyclePath is '':
        recyclePath = mainPath+'/recycle/'+fileType
    downloadPath = mainPath+'/downloads/'+fileType
    tempFolder = os.path.exists(downloadPath)
    if tempFolder:
        timeStamp = time.strftime('%d%m%Y%I%M%S')
        os.rename(fileType, fileType+'_'+timeStamp)
    os.chdir(mainPath+'/downloads')
    os.makedirs(downloadPath)
    # Set varibles needed
    if fileType is 'movies':
        mediaPath = moviePath
    elif fileType is 'shows':
        mediaPath = showPath
    elif fileType is 'files':
        mediaPath = filePath
    elif fileType is 'music':
        musicPath = filePath
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
        # unzip downloaded files
        rarExists = functions.unzipFile(fileType, downloadPath)
        if fileType is not 'music':
            if downloadProcess is not False:
                # format filenames
                functions.renameFile(downloadPath)
            # check for duplicates
            functions.moveFiles(downloadPath, mediaPath, recyclePath)
    # record to logs
    shutil.rmtree(downloadPath)
    print('[End of '+fileType+']')

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
    musicResult = startProcess('music', downloadAmount, config)
    fileResult = startProcess('file', downloadAmount, config)

# Add Timestamp to 'done.txt'
timeStamp = time.strftime('%d/%m/%Y %I:%M:%S')
with open(mainPath+'/downloads/done.txt', 'a') as myfile:
    myfile.write('###### '+timeStamp+' ######\n')

print ('-----------------------------=[Finished]')

# Was the downloading successfull?

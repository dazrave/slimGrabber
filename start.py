# global imports
import time, os, glob, os.path, shutil, sys

# imports
import config, functions

# get manual settings
videoType = sys.argv[1]
downloadAmount = sys.argv[2]

# get auto settings
downloadPath = mainPath+'/downloads'
if moviePath == False:
    moviePath = mainPath+'/movies'
if showPath == False:
    showPath = mainPath+'/shows'

def startProcess(videoType, downloadAmount):
    # Set varibles needed
    if videoType:
        if videoType == 'movie':
            mediaPath = moviePath
        else if videoType = 'show':
            mediaPath = showPath
        break
    downloadPath = downloadPath+'/'+videoType+'s'
    # Count the number of links avalible to download
    linkAmount = functions.countLinks(videoType)
    # Make sure everything is downloaded if no manual amount set
    if downloadAmount == False
        downloadAmount = linkAmount
    # Loop over downloadable links
    while True:
        functions.downloadFile(videoType)
        processedAmount = processedAmount + 1
        if processedAmount == downloadAmount:
            break
    # unzip downloaded files
    functions.unzipFile(videoType, downloadPath)
    # format filenames
    functions.renameFile(downloadPath)
    # check for duplicates
    functions.moveFiles(downloadPath, recyclePath)
    # move downloaded videos
    # record to logs
    break

# start the correct process
if videoType:
    downloadResult = startProcess(videoType, downloadAmount)
else:
    showResult = startProcess('show', downloadAmount)
    movieResult = startProcess('movie', downloadAmount)

# Was the downloading successfull?

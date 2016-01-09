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

# get manual settings
videoType = sys.argv[1]
downloadAmount = sys.argv[2]

# get auto settings
downloadPath = mainPath+'/downloads'
if moviePath is False:
    moviePath = mainPath+'/movies'
if showPath is False:
    showPath = mainPath+'/shows'
if showPath is False:
    showPath = mainPath+'/recycle'


def startProcess(videoType, downloadAmount):
    # Set varibles needed
    if videoType:
        if videoType is 'movie':
            mediaPath = moviePath
        elif videoType is 'show':
            mediaPath = showPath
        break
    downloadPath = downloadPath+'/'+videoType+'s'
    # Count the number of links avalible to download
    linkAmount = functions.countLinks(videoType)
    # Make sure everything is downloaded if no manual amount set
    if downloadAmount is False:
        downloadAmount = linkAmount
    # Loop over downloadable links
    while True:
        functions.downloadFile(videoType)
        processedAmount = processedAmount + 1
        if processedAmount is downloadAmount:
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

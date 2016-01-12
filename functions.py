#!/bin/bash
# global imports
import time
import os
import glob
import os.path
import shutil
import sys

# custom imports
import config

from config import mainPath, moviePath, showPath
from config import recyclePath, rgUser, rgPass, fileBot
config = [mainPath, moviePath, showPath, recyclePath, rgUser, rgPass, fileBot]

# Link checking


def countLinks(videoType):
    from config import mainPath
    downloadPath = mainPath+'/downloads'
    with open(downloadPath+'/'+videoType+'s.txt') as f:
        return sum(1 for _ in f)

# Link checking


def checkLinks(videoType):
    linkNumber = countLinks(videoType)
    if linkNumber > 0:
        linkCheck = True
    else:
        print('[No '+videoType+' links detected]')
        linkCheck = False
    return linkCheck

# Get download link


def getLink(videoType):
    from config import mainPath
    link = checkLinks(videoType)
    downloadPath = mainPath+'/downloads'
    if link:
        print('[Grabbing '+videoType+' link]')
        with open(downloadPath+'/'+videoType+'s.txt', 'r') as f:
            return f.readline()
    else:
        return False


def downloadFile(videoType, downloadPath, mainPath):
    downloadLink = getLink(videoType)
    os.chdir(downloadPath)
    if downloadLink:
        print('[Downloading '+videoType+']')
        os.system('plowdown '+downloadLink)
        with open(mainPath+'/downloads/done.txt', 'a') as myfile:
            myfile.write(downloadLink)
            print ('[Writing link to logs]')
        logFile = downloadPath+'.txt'
        with open(logFile, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(logFile, 'w') as fout:
            fout.writelines(data[1:])
            print ('[Removing link from download list]')
        return True
    else:
        return False


def unzipFile(videoType, downloadPath):
    # Navigation
    os.chdir(downloadPath)
    # find rar files
    if glob.glob("*.rar"):
        rarExists = True
    else:
        rarExists = False
        print('[No files to unpack]')
    if rarExists:
        for file in glob.glob('*.rar'):  # cycle through found rar files
            print('[Unpacking: '+file+']')
            os.system('filebot -extract '+file)
            # re-count all files in folders
            os.system('rm '+file)  # Delete .rar
            print('[Deleting: '+file+']')
    return rarExists


def renameFile(downloadPath):
    # Navigation
    os.chdir(downloadPath)
    # Find all videos and move into main directory
    extensions = ('.mp4', '.avi', '.wmv', '.mkv')
    # search through folder
    for file in glob.glob('*'):
        folderName = file
        if os.path.isdir(folderName):
            os.chdir(downloadPath+'/'+folderName)
            for file in glob.glob('*'):
                fileName = file
                ext = os.path.splitext(fileName)[-1].lower()
                if ext in extensions:
                        print('[Moving: '+fileName+']')
                        os.rename(downloadPath+'/'+folderName+'/'+fileName, downloadPath+'/'+fileName)
                        # delete empty folder
                        # shutil.rmtree(fileName)
            os.chdir(downloadPath)
            shutil.rmtree(downloadPath+'/'+folderName)
    # Scan and rename
    print('[Renaming video files]')
    os.system('filebot -rename -non-strict '+downloadPath)


def checkDuplicates(downloadPath, mediaPath, recyclePath):
    # Navigation
    os.chdir(downloadPath)
    # cycle through files in downloads
    print('[Checking for duplicates]')
    for file in glob.glob('*'):
        downloadedFile = file
        os.chdir(mediaPath)
        for file in glob.glob(downloadedFile):
            os.rename(mediaPath+'/'+file, recyclePath+'/'+file)


def moveFiles (downloadPath, mediaPath, recyclePath):
    checkDuplicates(downloadPath, mediaPath, recyclePath)
    # Navigation
    os.chdir(downloadPath)
    # supported extentions
    extensions = ('.mp4', '.avi', '.wmv', '.mkv')
    # search through folder
    for subdir, dirs, files in os.walk(downloadPath):
        for file in files:
            # get extention of file found
            ext = os.path.splitext(file)[-1].lower()
            # if extention is valid
            if ext in extensions:
                print('[Moving file: '+file+']')
                os.rename(downloadPath+'/'+file, mediaPath+'/'+file)

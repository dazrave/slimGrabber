# global imports
import time
import os
import glob
import os.path
import shutil
import sys

# imports
import config

# Link checking


def countLinks(videoType):
    with open(downloadPath+'/'+videoType+'s.txt') as f:
        print('[Checking '+videoType+' links]')
        return sum(1 for _ in f)
    break

# Link checking


def checkLinks(videoType):
    linkNumber = countLinks(videoType)
    if linkNumber > 0:
        linkCheck = True
    else:
        print('[No '+videoType+' links detected]')
        linkCheck = False
    return linkCheck
    break

# Get download link


def getLink(videoType):
    link = checkLinks(downloadPath, videoType)
    if link:
        print('[Grabbing '+videoType+' link]')
        with open(downloadPath+'/'+videoType+'s.txt', 'r') as f:
            return f.readline()
    else:
        return False
    break


def downloadFile(videoType):
    downloadLink = getLink(downloadPath, videoType)
    if downloadLink:
        print('[Downloading '+videoType+']')
        os.system('plowdown '+downloadLink)
        return True
    else:
        return False
    break


def unzipFile(videoType, downloadPath):
    # Navigation
    os.chdir(downloadPath)
    # find rar files
    if glob.glob("*.rar"):
        rarExists = True
    else:
        print('[No files to unpack]')
    if rarExists:
        for file in glob.glob('*.rar'):  # cycle through found rar files
            print('[Unpacking: '+file+']')
            # reset temp variables
            folderAmount = 0
            fileAmount = 0
            newfolderAmount = 0
            newfileAmount = 0
            # count all files in folders
            for _, dirs, files in os.walk(dir_to_list_recursively):
                folderAmount += len(dirs)
                fileAmount += len(files)
            # Unpack rar file
            os.system('filebot -extract '+file)
            # re-count all files in folders
            for _, dirs, files in os.walk(dir_to_list_recursively):
                    newFolderAmount += len(dirs)
                    newFileAmount += len(files)
            if newfileAmount > fileAmount:
                os.system('rm '+file)  # Delete .rar
                print('[Deleting: '+file+']')
    break


def renameFiles(downloadPath):
    # Navigation
    os.chdir(downloadPath)
    # Scan and rename
    print('[Renaming video files]')
    os.system('filebot -rename -non-strict '+filepath)
    break


def checkDuplicates(mediaPath, recyclePath, fileName):
    # Navigation
    os.chdir(downloadPath)
    # cycle through files in downloads
    for file in glob.glob('*'):
        downloadFile = file
        os.chdir(mediaPath)
        # cycle through files in media
        for file in glob.glob('*'):
            # match download and media files
            if downloadFile is file:
                print('[Duplicate found: '+file+']')
                os.system('mv '+file+' '+recyclePath)
                break
            break


def moveFiles(videoType, downloadPath, mediaPath):
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
                os.system('mv '+file+' '+mediaPath)
                break
            break

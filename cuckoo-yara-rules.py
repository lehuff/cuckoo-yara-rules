'''
The goal of this file is to grab all the files from the Yara-Rules github repo and then automatically add them to cuckoo, similar to the community.py tool for signatures.

Ideally this will be run under /cuckoo/data/yara/
'''

import urllib2
import glob
import zipfile
import os.path
from macpath import dirname
import sys
import subprocess

#Grab the current working directory for future use.
cwd = os.getcwd()
repo_path = cwd

#Insert repos to clone here.
repos = ['https://github.com/Yara-Rules/rules/archive/master.zip'
         ]
etc = 1
print('Starting')
for each in repos:
    try:
        file = urllib2.urlopen(each)
        data = file.read()
        with open(("master" + str(etc) + ".zip"), "wb") as code:
            code.write(data)
        etc += 1
    except Exception as e:
        print(e)   
print ("Downlading Yara Files")
zips = []
zipList = glob.glob('*.zip')
zips.extend(zipList)

for each in zips:
    try:
        zfile = zipfile.ZipFile(each)
        for name in zfile.namelist():
            (dirname, filename) = os.path.split(name)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            zfile.extract(name, dirname)
        os.remove(cwd + "/" + each)
    except Exception as e:
        print(e)
print("Extracting Yara Files")
yarFiles = []

for root, dirs, files in os.walk(cwd):
    for file in files:
        if file.endswith('.yar'):
            yarFiles.append(os.path.join(root, file))
        elif file.endswith('.yara'):
            yarFiles.append(os.path.join(root, file))
            
lFile = open('yara-rules-repo.yar', 'wb')
print("Writing yara-includes file")
for value in yarFiles:
    try:
        lFile.write('include ' + '"' + value + '"\n')
    except Exception as e:
        print(e)
lFile.close()
subprocess.check_output('cat yara-rules-repo.yar >> index_binaries.yar', shell=True)
print ('Done!')

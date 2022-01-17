# Publish web files to the Arduino data folder
import os
from os import listdir
from os.path import isfile, join
import subprocess

source_path = "C:\\Users\\delimas\\PycharmProjects\\SpaTestServer\\public"
dest_path = "C:\\Users\\delimas\\Documents\\Arduino\\SpaPoolController\\data"
gz_path = '"C:\\Program Files\\7-Zip\\7Z.exe"'

# Remove existing files
files = [f for f in listdir(dest_path) if isfile(join(dest_path, f))]
for file in files:
    os.remove(join(dest_path, file))

# Compress new files
files = [f for f in listdir(source_path) if isfile(join(source_path, f))]
for file in files:
    source = join(source_path, file)
    dst = join(dest_path, file + '.gz')
    command = gz_path +  ' a -tgzip "' + dst + '" "' + source + '"'
    subprocess.call(command)

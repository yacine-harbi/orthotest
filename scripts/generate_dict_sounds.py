from os import listdir
from os.path import isfile, join
from shutil import copyfile
import json
from pathlib import Path
from tinytag import TinyTag


flac_db = {}

for index, file in enumerate(listdir('flac')):
    if index % 5:
        filepath = join('flac', file)
        if isfile(filepath) and filepath.endswith('.flac'):
            tag: TinyTag = TinyTag.get(filepath)
            # print(tag.title)
            flac_db[file] = tag.title
            copyfile(filepath, join('sounds', file))
        
with open('words_flac.json', 'w', encoding='utf-8') as f:
    json.dump(flac_db, f)
    

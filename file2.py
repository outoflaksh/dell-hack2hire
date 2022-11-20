import os
import re
import json
import pprint
from collections import Counter



path = r"E:\GitHub\Misc\dell-hack2hire"


blacklisted_folders = ["node_modules", "venv",".git",".vscode","__pycache__","vendor"]
blacklisted_files = ["package-lock.json","requirements.txt",".gitignore"]
filelist = []

# list of regex pattern
regex_patterns = [r".get\(\"(.*?)\"", r".post\(\"(.*?)\"", r".put\(\"(.*?)\"", r".delete\(\"(.*?)\"",r"(?i)\b((?:http?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",]

def regexchecker(code_base:str):
    # regex = r"(?i)\b((?:http?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    data = []
    for line, string in enumerate(code_base.split('\n')):
        for regex in regex_patterns:
            url = re.findall(regex,string)
            
            if (url):
                line_url = [line+1, [x for x in url]]
                data.append(line_url)
        # url = re.findall(regex,string)
        # if url:
        #     line_url = [line+1, [x[0] for x in url]]
        #     data.append(line_url)
    # pprint.pprint(urls)
    return data

for dirPath, dirNames, fileNames in os.walk(path):
    if any(folder in dirPath for folder in blacklisted_folders):
        continue
    # for fileName in fileNames:
        #print(os.path.join(dirPath, fileName))
    else:
        for fileName in fileNames:
            if any(file in fileName for file in blacklisted_files):
                continue
            else:
                filelist.append(os.path.join(dirPath, fileName))
                print(os.path.join(dirPath, fileName))

# print('-' * 15)
print("Total Files: ", len(filelist))
# print(filelist)
print('-' * 15)

counts = Counter()
for c_dir, dirnames, filenames in os.walk('.'):
	for filename in filenames:
		before_ext, extension = os.path.splitext(filename)
		counts[extension]+= 1

for extension, count in counts.items():
	print(f"{extension:10}{count}")

print('-' * 15)

fin = {}

def loadfile(file:str):
    global fin
    with open(file, "r+" ,encoding="utf8") as f:
        code_base: str = f.read()
        data=regexchecker(code_base)
        fin[file] = data
        print(file, fin[file])
        # try:
            
        #     print(file,re.findall(r".get\(\"(.*?)\"", code_base))
        # except:
        #     print("Error")
        # print(code_base)
        # get_endpoints_from_file(file)
        # get_http_urls_from_file(file)
        # get_external_libraries_from_file(file)
        # result = {"http_urls": get_http_urls_from_file(file), 
	    # "external_libraries": get_external_libraries_from_file(file), 
	    # "internal_endpoints": get_endpoints_from_file(file)}
        # print(result)



for file in filelist:
    loadfile(file)

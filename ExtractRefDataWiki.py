import xml.etree.ElementTree as tree
import json
from os import listdir # install the "listdir" package (pip install dirlist)
from os.path import isfile, join
files =[]
dir = "outputNER"
for file in listdir(dir): 
    if isfile(join(dir, file)):
        files.append(dir + "/" + file)
for f in files:
    if ".xml" not in f:
        files.remove(f)
files.sort()

files = ["outputNER/ner_theIndicator01.xml", "outputNER/theIndicator39.xml", "outputNER/theIndicator40.xml","outputNER/theIndicator40.xml" ]
result = {}

def compile():
    for file in files:
        result[file] = {}
        root = tree.parse(file)
        string = ""
        result[file]["persons"] = {}
        result[file]["persons"]["real"] = {}
        result[file]["persons"]["fictional"] = {}
        result[file]["places"] = {}
        result[file]["org"] = {}
        #no = ""
        #bibtitle = "" 

        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}persName[@type = 'real']"):
            key = el.get('key')
            string = el.get('ref')
            if key is not None and string is not None:
                result[file]["persons"]["real"][key] = string
           # elif key is not None and string is None:
            #    result[file]["persons"]["real"][key] = key
        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}persName[@type = 'fictional']"):
            key = el.get('key')
            string = el.get('ref')
            if key is not None and string is not None:
                result[file]["persons"]["fictional"][key] = string
           # elif key is not None and string is None:
            #    result[file]["persons"]["fictional"][key] = key
        
        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}placeName[@key]"):
            string = el.get('key')
            ref = el.get('ref')
            type = el.get('type')
            country = el.get('corresp')
            result[file]["places"][string] = ref
            #result[file]["places"][string]["type"] = type
            #result[file]["places"][string]["country"] = country

        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}orgName"):
            key = el.get('key')
            string = el.get('ref')
            if key is not None and string is not None:
                result[file]["org"][key] = string
           # else:
              #  string = el.text
              #  result[file]["org"][string] = string
          
    return result


jsonfile = compile()
print(jsonfile)
json_obj = json.dumps(jsonfile, indent=7, ensure_ascii = False)
with open("Hunt_wikiIds.json", "w") as outfile:
    outfile.write(json_obj)
    print("Done!")

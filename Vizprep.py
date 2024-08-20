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

#files = ["Structural Versions/theIndicator39.xml", "Structural Versions/theIndicator40.xml"]
result = {}

def compile():
    for file in files:
        result[file] = {}
        root = tree.parse(file)
        string = ""
        result[file]["title"] = []
        result[file]["bibl"] = {}
        result[file]["bibl"]["title"] = {}
        result[file]["persons"] = {}
        result[file]["persons"]["real"] = {}
        result[file]["persons"]["fictional"] = {}
        result[file]["places"] = {}
        result[file]["org"] = {}
        result[file]["dates"] = {}
        no = ""
        bibtitle = "" 

        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}title"):
            altstring = ""
            expan = el.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
            if expan is not None:
                altstring = expan.text
            string = el.text
            if altstring is not None and altstring != "" and altstring not in result[file]["title"]:
                result[file]["title"].append(altstring)
            if string is not None and string != "" and string not in result[file]["title"]:
                result[file]["title"].append(string)                        
            

        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}persName[@type = 'real']"):
            key = el.get('key')
            string = el.get('ref')
            if key is not None and string is not None:
                result[file]["persons"]["real"][key] = string
            elif key is not None and string is None:
                result[file]["persons"]["real"][key] = key
        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}persName[@type = 'fictional']"):
            key = el.get('key')
            string = el.get('ref')


            if key is not None and string is not None:
                result[file]["persons"]["fictional"][key] = string
            elif key is not None and string is None:
                result[file]["persons"]["fictional"][key] = key
        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}bibl"): 
            altstring = ""
            head = el.find("{http://www.tei-c.org/ns/1.0}title")
            
            if head is not None:
                expan = head.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                bibtitle = head.text
                if expan is not None:
                    altstring = expan.text
            if bibtitle is not None and bibtitle != "":
                result[file]["bibl"]["title"][bibtitle] = {}
            if altstring is not None and altstring != "":
                bibtitle = altstring
                result[file]["bibl"]["title"][bibtitle] = {}
            author = el.find("{http://www.tei-c.org/ns/1.0}author")
            if author is not None:
                string = author.text
                if string is not None:
                    result[file]["bibl"]["title"][bibtitle]["author"] = string
            ref = el.find("{http://www.tei-c.org/ns/1.0}ref")
            if ref is not None:
                target = ref.get('target')
                string = target
                if string is not None:
                    if bibtitle != "":
                        result[file]["bibl"]["title"][bibtitle]["ref"] = string
        
        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}placeName[@key]"):
            string = el.get('key')
            ref = el.get('ref')
            type = el.get('type')
            country = el.get('corresp')
            result[file]["places"][string] = {}
            result[file]["places"][string]["type"] = type
            result[file]["places"][string]["country"] = country

        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}orgName"):
            key = el.get('key')
            string = el.get('ref')
            if key is not None and string is not None:
                result[file]["org"][key] = string
            else:
                string = el.text
                result[file]["org"][string] = string
        
        for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2//{http://www.tei-c.org/ns/1.0}date"):
            when = el.get('when')
            string = el.text
            if when is not None:
                result[file]["dates"][when] = string
          
    return result


jsonfile = compile()
print(jsonfile)
json_obj = json.dumps(jsonfile, indent=7, ensure_ascii = False)
with open("Hunt_dataNew.json", "w") as outfile:
    outfile.write(json_obj)
    print("Done!")

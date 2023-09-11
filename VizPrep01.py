import xml.etree.ElementTree as tree
import json
from os import listdir # install the "listdir" package (pip install dirlist)
from os.path import isfile, join
files =[]
dir = "Structural Versions"
for file in listdir(dir): 
    if isfile(join(dir, file)):
        files.append(dir + "/" + file)
for f in files:
    if ".xml" not in f:
        files.remove(f)
files.sort()

result = {} 
def compile():
    for file in files:
            result[file] = {}
            root = tree.parse(file)
            string = ""
            no = ""
            bibtitle = "" 
            nestedText= []
            #hText = ""
            for el in root.findall(".//{http://www.tei-c.org/ns/1.0}div2"):
                n = el.get('n')
                sectname = el.get("type")
                if sectname is not None:     #gets the section without an "n" attribute
                    if n is None and sectname != "title":
                        section = sectname
                        
                        result[file][section] = {}
                        result[file][section]["header"] = ""
                        result[file][section]["subheader"] = ""
                        result[file][section]["title"] = []
                        result[file][section]["bibl"] = {}
                        result[file][section]["bibl"]["title"] = {}
                        result[file][section]["persons"] = {}
                        result[file][section]["persons"]["real"] = {}
                        result[file][section]["places"] = {}
                        result[file][section]["org"] = {}
                        result[file][section]["dates"] = {}
                        
                        for e in el.findall("{http://www.tei-c.org/ns/1.0}head[@type='header']"):
                            ar =[]
                            header = ""
                                    
                            if e.find("./*") is None:
                                result[file][section]["header"] = e.text
                            else:
                                nestedText.append(e.text)
                                for x in e.findall("./*"):
                                    if x.tag != "{http://www.tei-c.org/ns/1.0}note":
                                        nestedText.append(x.text)
                                    ar = x.findall("./*")
                                    if len(ar) > 0:
                                        string = ar[-1].text
                                        if string != "":
                                            nestedText.append(string)
                                                
                                    after = x.tail
                                    nestedText.append(after)
                                        
                                for i in nestedText:
                                    if i is None:
                                        nestedText.remove(i)
                                
                                header = "".join(nestedText)
                                result[file][section]["header"] = header             
                                
                        for e in el.findall("{http://www.tei-c.org/ns/1.0}head[@type='subheader']"):
                            string = e.text
                            if string is not None:
                                result[file][section]["subheader"] = e.text    

                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}title"):
                            altstring = ""
                            expan = e.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                            if expan is not None:
                                altstring = expan.text
                            string = e.text
                            if altstring is not None and altstring != "" and altstring not in result[file][section]["title"]:
                                result[file][section]["title"].append(altstring)
                            if string is not None and string != "" and string not in result[file][section]["title"]:
                                result[file][section]["title"].append(string)                        
                        

                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}persName[@type = 'real']"):
                            key = e.get('key')
                            string = e.get('ref')
                            if key is not None and string is not None:
                                result[file][section]["persons"]["real"][key] = string
                            elif key is not None and string is None:
                                result[file][section]["persons"]["real"][key] = key
                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}persName[@type = 'fictional']"):
                            result[file][section]["persons"]["fictional"] = []
                            if e.get('corresp') is not None:
                                no = e.text
                            if e.text != no:
                                string = e.text
                            if string not in result[file][section]["persons"]["fictional"]:
                                result[file][section]["persons"]["fictional"].append(string)
                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}bibl"): 
                            altstring = ""
                            head = e.find("{http://www.tei-c.org/ns/1.0}title")
                            
                            if head is not None:
                                expan = head.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                                bibtitle = head.text
                                if expan is not None:
                                    altstring = expan.text
                            if bibtitle is not None and bibtitle != "":
                                result[file][section]["bibl"]["title"][bibtitle] = {}
                            if altstring is not None and altstring != "":
                                bibtitle = altstring
                                result[file][section]["bibl"]["title"][bibtitle] = {}
                            author = e.find("{http://www.tei-c.org/ns/1.0}author")
                            if author is not None:
                                string = author.text
                                if string is not None:
                                    result[file][section]["bibl"]["title"][bibtitle]["author"] = string
                            ref = e.find("{http://www.tei-c.org/ns/1.0}ref")
                            if ref is not None:
                                target = ref.get('target')
                                string = target
                                if string is not None:
                                    if bibtitle != "":
                                        result[file][section]["bibl"]["title"][bibtitle]["ref"] = string
                        
                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}placeName[@key]"):
                            result[file][section]["places"] = {}
                            string = e.get('key')
                            ref = e.get('ref')
                            result[file][section]["places"][string] = string

                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}orgName"):
                            result[file][section]["org"] = {}
                            key = e.get('key')
                            string = e.get('ref')
                            if key is not None and string is not None:
                                result[file][section]["org"][key] = string
                            else:
                                string = e.text
                                result[file][section]["org"][string] = string
                        
                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}date"):
                            result[file][section]["dates"] = {}
                            when = e.get('when')
                            string = e.text
                            if when is not None:
                                result[file][section]["dates"][when] = string                                       

                    elif n is not None and sectname != "title": #gets the section with an "n" attribute
                        section = sectname + " " + n
                        result[file][section] = {}
                        result[file][section]["header"] = ""
                        result[file][section]["subheader"] = ""
                        result[file][section]["title"] = []
                        result[file][section]["bibl"] = {}
                        result[file][section]["bibl"]["title"] = {}
                        result[file][section]["persons"] = {}
                        result[file][section]["persons"]["real"] = {}
                        result[file][section]["places"] = {}
                        result[file][section]["org"] = {}
                        result[file][section]["dates"] = {}

                        for e in el.findall("{http://www.tei-c.org/ns/1.0}head[@type='header']"):
                            ar =[]
                            header = ""
                            
                            if e.find("./*") is None:
                                result[file][section]["header"] = e.text
                            else:
                                nestedText.append(e.text)
                                for x in e.findall("./*"):
                                    if x.tag != "{http://www.tei-c.org/ns/1.0}note":
                                        nestedText.append(x.text)
                                    ar = x.findall("./*")
                                    if len(ar) > 0:
                                        string = ar[-1].text
                                        if string != "":
                                            nestedText.append(string)
                                                
                                    after = x.tail
                                    nestedText.append(after)
                                        
                                for i in nestedText:
                                    if i is None:
                                        nestedText.remove(i)
                                
                                header = "".join(nestedText)
                                result[file][section]["header"] = header

                        for e in el.findall("{http://www.tei-c.org/ns/1.0}head[@type='subheader']"):
                            string = e.text
                            if string is not None:
                                result[file][section]["subheader"] = e.text

                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}title"):
                            altstring = ""
                            expan = e.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                            if expan is not None:
                                altstring = expan.text
                            string = e.text
                            if altstring is not None and altstring != "" and altstring not in result[file][section]["title"]:
                                result[file][section]["title"].append(altstring)
                            if string is not None and string != "" and string not in result[file][section]["title"]:
                                result[file][section]["title"].append(string)                        
                        

                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}persName[@type = 'real']"):
                            key = e.get('key')
                            string = e.get('ref')
                            if key is not None and string is not None:
                                result[file][section]["persons"]["real"][key] = string
                            elif key is not None and string is None:
                                result[file][section]["persons"]["real"][key] = key
                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}persName[@type = 'fictional']"):
                            result[file][section]["persons"]["fictional"] = []
                            if e.get('corresp') is not None:
                                no = e.text
                            if e.text != no:
                                string = e.text
                            if string not in result[file][section]["persons"]["fictional"]:
                                result[file][section]["persons"]["fictional"].append(string)
                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}bibl"): 
                            altstring = ""
                            head = e.find("{http://www.tei-c.org/ns/1.0}title")
                            
                            if head is not None:
                                expan = head.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                                bibtitle = head.text
                                if expan is not None:
                                    altstring = expan.text
                            if bibtitle is not None and bibtitle != "":
                                result[file][section]["bibl"]["title"][bibtitle] = {}
                            if altstring is not None and altstring != "":
                                bibtitle = altstring
                                result[file][section]["bibl"]["title"][bibtitle] = {}
                            author = e.find("{http://www.tei-c.org/ns/1.0}author")
                            if author is not None:
                                string = author.text
                                if string is not None:
                                    result[file][section]["bibl"]["title"][bibtitle]["author"] = string
                            ref = e.find("{http://www.tei-c.org/ns/1.0}ref")
                            if ref is not None:
                                target = ref.get('target')
                                string = target
                                if string is not None:
                                    if bibtitle != "":
                                        result[file][section]["bibl"]["title"][bibtitle]["ref"] = string
                        
                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}placeName[@key]"):
                            result[file][section]["places"] = {}
                            string = e.get('key')
                            ref = e.get('ref')
                            result[file][section]["places"][string] = string

                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}orgName"):
                            result[file][section]["org"] = {}
                            key = e.get('key')
                            string = e.get('ref')
                            if key is not None and string is not None:
                                result[file][section]["org"][key] = string
                            else:
                                string = e.text
                                result[file][section]["org"][string] = string
                        
                        for e in el.findall(".//{http://www.tei-c.org/ns/1.0}date"):
                            result[file][section]["dates"] = {}
                            when = e.get('when')
                            string = e.text
                            if when is not None:
                                result[file][section]["dates"][when] = string

    return result                  

jsonfile = compile()
print(jsonfile)
json_obj = json.dumps(jsonfile, indent=10, ensure_ascii = False)
with open("Hunt_data01.json", "w") as outfile:
    outfile.write(json_obj)
    print("Done!")
        
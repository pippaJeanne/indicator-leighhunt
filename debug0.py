import xml.etree.ElementTree as tree
import json
from os import listdir # install the "listdir" package (pip install dirlist)
from os.path import isfile, join
files =[]
dir = "OutputNER"
for file in listdir(dir): 
    if isfile(join(dir, file)):
        files.append(dir + "/" + file)
for f in files:
    if ".xml" not in f:
        files.remove(f)
files.sort()
print(files)

result = {} 


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
                div3 = el.findall("{http://www.tei-c.org/ns/1.0}div3")
                if div3 == []:
                    if sectname is not None:     #gets the section without an "n" attribute
                        if n is None and sectname != "title":
                            section = sectname
                            
                            result[file][section] = {}
                            result[file][section]["header"] = ""
                            result[file][section]["subheader"] = ""
                            result[file][section]["title"] = []
                            result[file][section]["bibl"] = {}
                            result[file][section]["bibl"]["title"] = []
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
                                title_type = ""
                                key = e.get("key")
                                level= e.get("level")
                                expan = e.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                                if expan is not None:
                                    altstring = expan.text
                                if key is not None:
                                    string = key
                                    #print(string)
                                elif key is None:
                                    string = e.text
                                    #print(string)
                                if level is not None:
                                    title_type = level
                                    #print(title_type)
                                
                                if altstring is not None and altstring != "": #and altstring not in result[file][section]["title"]
                                    result[file][section]["title"].append({"title": altstring,
                                    "level": title_type})
                                if string is not None and string != "":# and string not in result[file][section]["title"]:
                                    result[file][section]["title"].append({"title": string,
                                    "level": title_type})
                            

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
                                bibl = {} 
                                altstring = ""
                                head = e.find("{http://www.tei-c.org/ns/1.0}title")
                                t_type = ""
                                if head is not None:
                                    expan = head.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                                    bibtitle = head.text
                                    if expan is not None:
                                        altstring = expan.text
                                    t_type = head.get("level")
                                if bibtitle is not None and bibtitle != "" and string not in result[file][section]["bibl"]["title"]:
                                    bibl["title"] = bibtitle
                                    #result[file][section]["bibl"]["title"][bibtitle] = {}
                                if altstring is not None and altstring != "" and string not in result[file][section]["bibl"]["title"]:
                                    bibtitle = altstring
                                    bibl["title"] = bibtitle
                                    #result[file][section]["bibl"]["title"][bibtitle] = {}
                                author = e.find("{http://www.tei-c.org/ns/1.0}author")
                                if author is not None:
                                    string = author.text
                                    if string is not None:
                                        bibl["author"] = string
                                
                                        #result[file][section]["bibl"]["title"][bibtitle]["author"] = string
                                editor = e.find("{http://www.tei-c.org/ns/1.0}editor")
                                if editor is not None:
                                    string = editor.text
                                    if string is not None:
                                        bibl["editor"] = string
                                        #result[file][section]["bibl"]["title"][bibtitle]["editor"] = string
                                ref = e.find("{http://www.tei-c.org/ns/1.0}ref")
                                if ref is not None:
                                    target = ref.get('target')
                                    string = target
                                    if string is not None:
                                        if bibtitle != "":
                                            bibl["ref"] = string
                                            #result[file][section]["bibl"]["title"][bibtitle]["ref"] = string
                                if t_type is not None and t_type != "":
                                    bibl["level"] = t_type
                                    #result[file][section]["bibl"]["title"][bibtitle]["level"] = t_type
                                if bibl is not result[file][section]["bibl"]["title"] and len(bibl.keys()) > 1:
                                    result[file][section]["bibl"]["title"].append(bibl)

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
                            result[file][section]["bibl"]["title"] = []
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
                                obj= {}
                                altstring = ""
                                title_type = ""
                                key = e.get("key")
                                #print(key)
                                level= e.get("level")
                                #print(level)
                                expan = e.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                                if expan is not None and key is None:
                                    altstring = expan.text
                                if key is not None:
                                     string = key
                                     #print(string)
                                elif key is None:
                                    string = e.text
                                    #print(string)
                                if level is not None:
                                    title_type = level
                                    #print(title_type)
                                if altstring is not None and altstring != "": 
                                    obj = {"title": altstring,
                                              "level": title_type}
                                if string is not None and string != "": 
                                    obj = {"title": string,
                                              "level": title_type}
                                if obj not in result[file][section]["title"]:
                                    result[file][section]["title"].append(obj)  
                            

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
                                bibl = {} 
                                altstring = ""
                                head = e.find("{http://www.tei-c.org/ns/1.0}title")
                                t_type = ""
                                if head is not None:
                                    expan = head.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                                    bibtitle = head.text
                                    if expan is not None:
                                        altstring = expan.text
                                    t_type = head.get("level")
                                if bibtitle is not None and bibtitle != "" and string not in result[file][section]["bibl"]["title"]:
                                    bibl["title"] = bibtitle
                                    #result[file][section]["bibl"]["title"][bibtitle] = {}
                                if altstring is not None and altstring != "" and string not in result[file][section]["bibl"]["title"]:
                                    bibtitle = altstring
                                    bibl["title"] = bibtitle
                                    #result[file][section]["bibl"]["title"][bibtitle] = {}
                                author = e.find("{http://www.tei-c.org/ns/1.0}author")
                                if author is not None:
                                    string = author.text
                                    if string is not None:
                                        bibl["author"] = string
                                
                                        #result[file][section]["bibl"]["title"][bibtitle]["author"] = string
                                editor = e.find("{http://www.tei-c.org/ns/1.0}editor")
                                if editor is not None:
                                    string = editor.text
                                    if string is not None:
                                        bibl["editor"] = string
                                        #result[file][section]["bibl"]["title"][bibtitle]["editor"] = string
                                ref = e.find("{http://www.tei-c.org/ns/1.0}ref")
                                if ref is not None:
                                    target = ref.get('target')
                                    string = target
                                    if string is not None:
                                        if bibtitle != "":
                                            bibl["ref"] = string
                                            #result[file][section]["bibl"]["title"][bibtitle]["ref"] = string
                                if t_type is not None and t_type != "":
                                    bibl["level"] = t_type
                                    #result[file][section]["bibl"]["title"][bibtitle]["level"] = t_type
                                if bibl is not result[file][section]["bibl"]["title"] and len(bibl.keys()) > 1:
                                    result[file][section]["bibl"]["title"].append(bibl)
                                print(bibl)
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

                else: #accounting for the div3
                    if n is not None and sectname != "title":
                        section = sectname + " " + n
                        result[file][section] = {}
                        result[file][section]["header"] = ""
                        result[file][section]["subheader"] = ""

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
                        
                        for div in div3:
                            num = div.get('n')
                            subsection = div.get("type")
                            subsect = subsection + " " + num
                            result[file][section][subsect] = {}
                            result[file][section][subsect]["header"] = ""
                            result[file][section][subsect]["subheader"] = ""
                            result[file][section][subsect]["title"] = []
                            result[file][section][subsect]["bibl"] = {}
                            result[file][section][subsect]["bibl"]["title"] = []
                            result[file][section][subsect]["persons"] = {}
                            result[file][section][subsect]["persons"]["real"] = {}
                            result[file][section][subsect]["places"] = {}
                            result[file][section][subsect]["org"] = {}
                            result[file][section][subsect]["dates"] = {}

                            for e in div.findall("{http://www.tei-c.org/ns/1.0}head[@type='header']"):
                                ar =[]
                                header = ""
                                
                                if e.find("./*") is None:
                                    result[file][section][subsect]["header"] = e.text
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
                                    result[file][section][subsect]["header"] = header

                                    for e in div.findall("{http://www.tei-c.org/ns/1.0}head[@type='subheader']"):
                                        string = e.text
                                        if string is not None:
                                            result[file][section][subsect]["subheader"] = e.text

                                    for e in div.findall(".//{http://www.tei-c.org/ns/1.0}title"):
                                        altstring = ""
                                        title_type = ""
                                        key = e.get("key")
                                        level= e.get("level")
                                        expan = e.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                                        if expan is not None:
                                            altstring = expan.text
                                        if key is not None:
                                            string = key
                                        elif key is None:
                                            string = e.text
                                        if level is not None:
                                            title_type = level
                                        if altstring is not None and altstring != "":# and altstring not in result[file][section][subsect]["title"]:
                                            result[file][section][subsect]["title"].append({"title": altstring,
                                              "level": title_type})
                                        if string is not None and string != "":# and string not in result[file][section][subsect]["title"]:
                                            result[file][section][subsect]["title"].append({"title":string,
                                              "level":title_type})                        
                                    

                                    for e in div.findall(".//{http://www.tei-c.org/ns/1.0}persName[@type = 'real']"):
                                        key = e.get('key')
                                        string = e.get('ref')
                                        if key is not None and string is not None:
                                            result[file][section][subsect]["persons"]["real"][key] = string
                                        elif key is not None and string is None:
                                            result[file][section][subsect]["persons"]["real"][key] = key
                                    for e in el.findall(".//{http://www.tei-c.org/ns/1.0}persName[@type = 'fictional']"):
                                        result[file][section][subsect]["persons"]["fictional"] = []
                                        if e.get('corresp') is not None:
                                            no = e.text
                                        if e.text != no:
                                            string = e.text
                                        if string not in result[file][section][subsect]["persons"]["fictional"]:
                                            result[file][section][subsect]["persons"]["fictional"].append(string)
                                    for e in div.findall(".//{http://www.tei-c.org/ns/1.0}bibl"):
                                        bibl = {} 
                                        altstring = ""
                                        head = e.find("{http://www.tei-c.org/ns/1.0}title")
                                        t_type = ""
                                        if head is not None:
                                            expan = head.find("{http://www.tei-c.org/ns/1.0}choice/{http://www.tei-c.org/ns/1.0}expan")
                                            bibtitle = head.text
                                            if expan is not None:
                                                altstring = expan.text
                                            t_type = head.get("level")
                                        if bibtitle is not None and bibtitle != "" and string not in result[file][section][subsect]["bibl"]["title"]:
                                            bibl["title"] = bibtitle
                                            #result[file][section][subsect]["bibl"]["title"][bibtitle] = {}
                                        if altstring is not None and altstring != "" and string not in result[file][section][subsect]["bibl"]["title"]:
                                            bibtitle = altstring
                                            bibl["title"] = bibtitle
                                            #result[file][section][subsect]["bibl"]["title"][bibtitle] = {}
                                        author = e.find("{http://www.tei-c.org/ns/1.0}author")
                                        if author is not None:
                                            string = author.text
                                            if string is not None:
                                                bibl["author"] = string
                                        
                                                #result[file][section][subsect]["bibl"]["title"][bibtitle]["author"] = string
                                        editor = e.find("{http://www.tei-c.org/ns/1.0}editor")
                                        if editor is not None:
                                            string = editor.text
                                            if string is not None:
                                                bibl["editor"] = string
                                                #result[file][section][subsect]["bibl"]["title"][bibtitle]["editor"] = string
                                        ref = e.find("{http://www.tei-c.org/ns/1.0}ref")
                                        if ref is not None:
                                            target = ref.get('target')
                                            string = target
                                            if string is not None:
                                                if bibtitle != "":
                                                    bibl["ref"] = string
                                                    #result[file][section][subsect]["bibl"]["title"][bibtitle]["ref"] = string
                                        if t_type is not None and t_type != "":
                                            bibl["level"] = t_type
                                            #result[file][section][subsect]["bibl"]["title"][bibtitle]["level"] = t_type
                                        if bibl is not result[file][section][subsect]["bibl"]["title"] and len(bibl.keys()) > 1:
                                            result[file][section][subsect]["bibl"]["title"].append(bibl)

                                    for e in div.findall(".//{http://www.tei-c.org/ns/1.0}placeName[@key]"):
                                        result[file][section][subsect]["places"] = {}
                                        string = e.get('key')
                                        ref = e.get('ref')
                                        result[file][section][subsect]["places"][string] = string

                                    for e in div.findall(".//{http://www.tei-c.org/ns/1.0}orgName"):
                                        result[file][section][subsect]["org"] = {}
                                        key = e.get('key')
                                        string = e.get('ref')
                                        if key is not None and string is not None:
                                            result[file][section][subsect]["org"][key] = string
                                        else:
                                            string = e.text
                                            result[file][section][subsect]["org"][string] = string
                                    
                                    for e in div.findall(".//{http://www.tei-c.org/ns/1.0}date"):
                                        result[file][section][subsect]["dates"] = {}
                                        when = e.get('when')
                                        string = e.text
                                        if when is not None:
                                            result[file][section][subsect]["dates"][when] = string
#print(result)
json_obj = json.dumps(result, indent=7, ensure_ascii = False)
with open("debug0.json", "w") as outfile:
    outfile.write(json_obj)
    print("Done!")
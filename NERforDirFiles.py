# First it is necessary to install the packages: spacy and xml.etree.ElementTree (collections and pprint are optional)
# for installing spacy : https://spacy.io/usage 
# Import of modules and language models for NER
import spacy
#nlp = spacy.load('en_core_web_trf') #EN model 
nlp = spacy.load('xx_ent_wiki_sm') # multilingual model 
#nlp = spacy.load('fr_dep_news_trf') #French model

from os import listdir # install the "listdir" package (pip install dirlist)
from os.path import isfile, join
import re
# This module will help us manage the xml structure and use xpath for retreiving the text 
import xml.etree.ElementTree as ET
files =[]
reFiles=[]
dir = "ForNER"
for file in listdir(dir): 
    if isfile(join(dir, file)):
        files.append(file)
        reFiles.append(dir + "/" + file)
for f in files:
    if ".xml" not in f:
        files.remove(f)
#print(files)
#print(reFiles)

# function to replace the entities in the text with the right tag according to the label given
def replace(input, output): # passing the input and output files
  # open files
  with open(input, "r") as f: 
    with open(output, "w") as file_towrite:
      # testing every line of text
      for line in f:
        # testing every entity (it's a dictionary)
        for l in new_ls_ent:
          # establish variables for clean output
          origline = "" 
          newLine = ""
          # test if entity appears in that line and if it is labeled as "person"
          if new_ls_ent[l] == "PER" and l in line: 
            line = re.sub(l,f"<persName key=\"{l}\">{l}</persName>", line) # replace and overwrite line
            newLine = line # pass value to variable previously established
          # same for remaining labels
          if new_ls_ent[l] == "GPE" or new_ls_ent[l] == "LOC" and l in line:
            line = re.sub(l,f"<placeName key='{l}'>{l}</placeName>", line)
            newLine = line 
          if new_ls_ent[l] == "WORK_OF_ART" and l in line:
            line = re.sub(l,f"<title>{l}</title>", line)
            newLine = line
          if new_ls_ent[l] == "DATE" and l in line:
            line = re.sub(l,f"<date>{l}</date>", line)
            newLine = line    
          # else if the entity does not appear in the line, we pass the original value without modifying it
          elif l not in line:
            origline = line
          # once out of the entity loop we write the resulting line in the output file and continue to next line   
        file_towrite.write(origline) 
        file_towrite.write(newLine) 
    # the values of origline and newLine will reset when entering the entities loop
    print("Done!")

for f in reFiles:
    # parsing the file
    root = ET.parse(f)
    string = ""
    result = []
    # retrieving the text with an xpath query (leaving TEI Header and the forematter info out, since it is already encoded in that regard)
    for elem in root.findall(".//{http://www.tei-c.org/ns/1.0}body//*"): 
        # removing all empty nodes
        if elem.text is None :
            elem.text = ""
        string += str(elem.text) + " "
        result = "".join(string) 
    #print(result) 
    doc = nlp(result)
    # Placing them into a dictionary or object for better manipulation
    ls_ents = dict([str(x), x.label_] for x in doc.ents)
    print(ls_ents)
    # Removing all entities that are not "person", "date", "place(GPE)" or "organisation"
    new_ls_ent = {}
    for a in ls_ents:
        if ls_ents[a] == "PER" or ls_ents[a] == "DATE" or ls_ents[a] == "GPE" or ls_ents[a] == "ORG" or ls_ents[a] == "LOC" or ls_ents[a] == "WORK_OF_ART":
            new_ls_ent[a] = ls_ents[a] 
    print(new_ls_ent)
    #path to input file
    input = f
    file = f.split("/")
    filename = file[-1]
    output = "outputNER/ner_" + filename  
    #calling the previously defined function
    replace(input, output)

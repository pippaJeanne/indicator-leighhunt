# First it is necessary to install the packages: spacy and xml.etree.ElementTree (collections and pprint are optional)
# for installing spacy : https://spacy.io/usage 
# Import of modules and language models for NER
import spacy
nlp = spacy.load('en_core_web_trf')  # multilingual model 
efficiencyPack = spacy.load('xx_ent_wiki_sm')

#from collections import Counter
#from pprint import pprint
import re
# This module will help us manage the xml structure and use xpath for retreiving the text 
import xml.etree.ElementTree as ET
# path for the file
file = "Structural Versions/theIndicator39 copie.xml"
# parsing the file
root = ET.parse(file)
string = ""
result = []
# retrieving the text with an xpath query (leaving TEI Header and the forematter info out, since it is already encoded in that regard)
for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}div2[@type="section"]//*'): 
    # removing all empty nodes
    if elem.text is None :
       elem.text = ''
    string += str(elem.text) + " "
    result = "".join(string) 
for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}div2[@type="correspondents"]//*'):   
    # removing all empty nodes
    if elem.text is None :
        elem.text = ''
    string += str(elem.text) + " "
    result = "".join(string)
for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}div2[@type="colophon"]//*'): 
    # removing all empty nodes
    if elem.text is None :
        elem.text = ''
    string += str(elem.text) + " "
    result = "".join(string)
#print(result)
    
# We begin applying the Named Entity Recognition (NER) with spacy

# Reference: article "Named Entity Recognition with NLTK and SpaCy" by Susan Li on Medium 
# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da

# Preparing list of entities and tokens
doc = nlp(result)
# Placing them into a dictionary or object for better manipulation
ls_ents = dict([str(x), x.label_] for x in doc.ents)
len(ls_ents)
# Removing all entities that are not "person", "date", "place(GPE)" or "organisation"
new_ls_ent = {}
for a in ls_ents:
    if ls_ents[a] == "PERSON" or ls_ents[a] == "DATE" or ls_ents[a] == "GPE" or ls_ents[a] == "ORG":
        new_ls_ent[a] = ls_ents[a] 

# function to replace the entities in the text with the right tag according to the label given
def replace(input, output): # passing the input and output files
  # open files
  with open(input, "r") as f: 
    with open(output, "w") as file_towrite:
      # testing every line of text
      for line in f:
        for l in new_ls_ent: # testing every entity (it's a dictionary)
          origline = "" # establish variables for clean output
          newLine = ""
          if new_ls_ent[l] == "PERSON" and l in line: # test if entity appears in that line and if it is labeled as "person"
            line = re.sub(l,f"<persName>{l}</persName>", line) # replace and overwrite line
            newLine = line # pass value to variable previously established
          # same for remaining labels
          if new_ls_ent[l] == "GPE" and l in line:
            line = re.sub(l,f"<placeName>{l}</placeName>", line)
            newLine = line 
          if new_ls_ent[l] == "DATE" and l in line:
            line = re.sub(l,f"<date>{l}</date>", line)
            newLine = line 
          if new_ls_ent[l] == "ORG" and l in line:
            line = re.sub(l,f"<orgName>{l}</orgName>", line)
            newLine = line 
          # else if the entity does not appear in the line, we pass the original value without modifying it
          elif l not in line:
            origline = line
         # once out of the entity loop we write the resulting line in the output file and continue to next line   
        file_towrite.write(origline) 
        file_towrite.write(newLine) 
    # the values of origline and newLine will reset when entering the entities loop

input = "Structural Versions/theIndicator39.xml" # path to input file
output = "Structural Versions/theIndicator39ner.xml"   # path to output file
replace(input, output) # calling the previously defined function  


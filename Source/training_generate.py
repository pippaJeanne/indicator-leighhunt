from google import genai
from google.genai import types
import json
import os
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

# Get list of tuned models
for model_info in client.tunings.list():
    print(model_info.tuned_model.model)

# Use base model
# To help in the encoding of the structure of the letter given the template with the editorial protocol
template = open("templateEncodage.xml", "r").read()
text = open("ToProcess.txt", "r").read()

response = client.models.generate_content(
    model='gemini-2.5-flash', contents=f"En prenant le modèle d'encodage TEI dans {template}, prends le texte océrisé dans {text} et fais l'encodage TEI du text océrisé en suivant le modèle fourni. Produis le contenu dans un fichier XML-TEI.")
with open("input/1545_08_05_MFallais.xml", "w", encoding="utf8") as outfile:
    outfile.write(response.text) #change name of file following the model => 1538_10_20_NomDestinataire.xml

#####
    # To help in the encoding of the structure of set of letters given the template with the editorial protocol 
for i in range(1,4): #number for last argument of range depends on number of letters in the 'text' doc plus 1 (no index 0).
    template = open("templateEncodage.xml", "r").read()
    text = open("ToProcess.txt", "r").read()

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=f"En prenant le modèle d'encodage TEI dans {template}, prends le texte océrisé dans {text} de la lettre correspondant au numéro {i} en ordre (les lettres ont été divisées par des lignes pointillées) et fais l'encodage TEI du text océrisé en suivant le modèle fourni. Produis le contenu dans un fichier XML-TEI.")
    with open(f"input/{i}.xml", "w", encoding="utf8") as outfile:
        outfile.write(response.text) #change name of file following the model => 1538_10_20_NomDestinataire.xml

#####    
# text to translate
text = open("Translations_txt/1538_01_LouisduTillet.txt", "r").read()

# generate content with the tuned model
# Segmenting text to fit the token limit
limit = 4000
nloops = len(text)//limit
# output file
outfile = open("Translations_txt/1538_01_LouisduTilletES.txt", "a", encoding="utf8")
for i in range(0,nloops+1):
    milestone = i * limit
    if milestone < len(text):
        substring = text[milestone:milestone+limit]
        #i = i + limit
    #if i < nloops:
    #    substring = text[i:i+limit]
        
        response = client.models.generate_content(
            model="tunedModels/tradcalvinfres-jeclu1o78weer7wramhdpb312",
    #model=tuning_job.tuned_model.model,
    contents=f"Traduis le texte suivant vers l'espagnol.\nTexte : {substring}",
)
        outfile.write(response.text)


#For finetuning the model
file = open("output_finetuning01.json", "r") #dataset
training_dataset = json.load(file)
# print(training_dataset)
#To check length of strings (has to be < 5000)
for i in range(len(training_dataset)):
    print(f"{i} {len(training_dataset[i]['input'])}")
    print(f"{i} {len(training_dataset[i]['output'])}")
    
training_dataset=types.TuningDataset(
        examples=[
            types.TuningExample(
                text_input=i["input"],
                output=i["output"],
            )
            for i in training_dataset
        ],
    )
tuning_job = client.tunings.tune(
    base_model='models/gemini-1.5-flash-001-tuning',
    training_dataset=training_dataset,
    config=types.CreateTuningJobConfig(
        epoch_count= 5,
        batch_size=4,
        learning_rate=0.001,
        tuned_model_display_name="trad_Calvin_FR-ES"
    )
)
# Check models list
for model_info in client.models.list():
    print(model_info.name)


# Translating remaining text
#laststr = text[limit * nloops - 10:len(text)] 

#response = client.models.generate_content(
#    model="tunedModels/tradcalvinfres-jeclu1o78weer7wramhdpb312",
    #model=tuning_job.tuned_model.model,
#    contents=f"Traduis le texte suivant vers l'espagnol.\nTexte : {laststr}",
#)
# print(response.text)
#outfile.write(f"\n {response.text}")

######################
# Segmenting text to fit the token limit
#limit = 4000
#nloops = len(text)//limit
# rest = len(text1) - (limit * nloops)
#for i in range(0,nloops):
    #if i < nloops:
        #substring = text[i:i+limit]
        # print(substring)
#        outfile = open("Translations_txt/sectioning_test.txt", "a", encoding="utf8")
        #outfile.write(substring)
#laststr = text[limit * nloops - 10:len(text)]
# print(laststr)
# outfile.write(f"\n {laststr}")




#pip install SPARQLWrapper
import json
from SPARQLWrapper import SPARQLWrapper, JSON
#get json file contianing the data
persdata = {}
with open("Hunt_wikiIds.json", "r") as indexData:
  persdata = json.load(indexData) 
# Preparing data for query
# Getting access keys 
files = persdata.keys()
pers = {}
# Organize according to service : dbpedia or wikidata
for f in files:
  names_real = list(persdata[f]["persons"]["real"].keys())
  if names_real is not None:
    for n in names_real:
      pers[n] = persdata[f]["persons"]["real"][n] 
  names_fict = list(persdata[f]["persons"]["fictional"].keys())
  if names_fict is not None:
    for n in names_fict:
      pers[n] = persdata[f]["persons"]["fictional"][n] 
urisdb = {}
uriswiki = {}
for key in pers.keys():
  if pers[key].__contains__("dbpedia"):
    urisdb[key] = pers[key]
  if pers[key].__contains__("wikidata"):
    spans = pers[key].split("/")
    uriswiki[key] = spans[-1]
qdb = []
qwiki = []
dblist = list(urisdb.keys())
wikilist = list(uriswiki.keys())
#print(urisdb, uriswiki)
query_db = ""
query_wiki = ""
for db in dblist:
  item = urisdb[db]
  q = "{<" + item + ">  dbo:abstract ?abstract; <http://dbpedia.org/ontology/thumbnail> ?img.}"
  qdb.append(q)
  query_db =  " UNION ".join(qdb)
# Seting limit of about 25
limit = 25
for w in wikilist: 
  if wikilist.index(w) <= limit: 
    item = uriswiki[w]
    q = "{BIND(wd:" + item + " AS ?item) Optional {?item wdt:P18 ?img; wdt:P570 ?deathDate; wdt:P569 ?birthDate.} [ schema:about ?item ; schema:name ?name;].}"
    qwiki.append(q)
    query_wiki =  " UNION ".join(qwiki)

# To execute query | Pass values for queries
urlDbpadia = "http://dbpedia.org/sparql"
urlWikidata = "https://query.wikidata.org/sparql"
sparql_wiki = SPARQLWrapper(urlWikidata)
sparql_db = SPARQLWrapper(urlDbpadia)
sparql_db.setQuery("\n"
"PREFIX dbo: <http://dbpedia.org/ontology/> \n"
"PREFIX dct: <http://purl.org/dc/terms/> \n"
"PREFIX foaf: <http://xmlns.com/foaf/0.1/> \n "
"SELECT DISTINCT ?abstract, ?img \n "
"WHERE { \n" + query_db + "\n FILTER ( LANG ( ?abstract ) = 'en'  ) \n"
"} "  
)
sparql_wiki.setQuery("\n"
"PREFIX wdt: <http://www.wikidata.org/prop/direct/> \n"
"PREFIX wd: <http://www.wikidata.org/entity/> \n"
"PREFIX wikibase: <http://wikiba.se/ontology#> \n"
"SELECT DISTINCT ?item ?itemLabel ?itemDescription ?birthDate ?deathDate ?img \n "
"WHERE { \n " + query_wiki +  "\n SERVICE wikibase:label { bd:serviceParam wikibase:language 'en' } \n"
"}"
)
sparql_wiki.setReturnFormat(JSON)
sparql_db.setReturnFormat(JSON)
results = sparql_wiki.query().convert()
results1 = sparql_db.query().convert()
persons = []

for result in results1["results"]["bindings"]:
 img = ""
 name = ""
 abstract = result["abstract"]["value"]
 for db in urisdb.keys():
   if abstract.__contains__(db):
    name = db
 if result.__contains__("img"):
  img = result["img"]["value"]
  pers = {"name":name, "abstract" : abstract}
 if img is not None or img != "":
  pers["img"]=img
 persons.append(pers)

 for result in results["results"]["bindings"]:
  img = ""
  url = result["item"]["value"]
  name = result["itemLabel"]["value"]
  desc = result["itemDescription"]["value"]
  pers =  {"name": name,"desc" : desc, "url": url}
  if result.__contains__("deathDate") or result.__contains__("birthDate"):
    birth = result["birthDate"]["value"]
    death = result["deathDate"]["value"]
    b = birth.split("T")
    d = death.split("T")
    dates = f"({b[0]} - {d[0]})"
    pers["dates"]=dates
  if result.__contains__("img"):
    img = result["img"]["value"]
  if img is not None or  img != '':
    pers["img"]=img
  persons.append(pers)
#print(len(qwiki))

# Do the rest (same limit)
n = 2
if len(wikilist) > limit:
  qwiki = []
  newlimit = 25 * n
  for w in wikilist: 
    if wikilist.index(w) > limit and wikilist.index(w) <= newlimit: 
      #print(wikilist.index(w) > limit and wikilist.index(w) <= newlimit)
      item = uriswiki[w]
      q = "{BIND(wd:" + item + " AS ?item) Optional {?item wdt:P18 ?img; wdt:P570 ?deathDate; wdt:P569 ?birthDate.} [ schema:about ?item ; schema:name ?name;].}"
      qwiki.append(q)
      query_wiki =  " UNION ".join(qwiki)
  sparql_wiki.setQuery("\n"
"PREFIX wdt: <http://www.wikidata.org/prop/direct/> \n"
"PREFIX wd: <http://www.wikidata.org/entity/> \n"
"PREFIX wikibase: <http://wikiba.se/ontology#> \n"
"SELECT DISTINCT ?item ?itemLabel ?itemDescription ?birthDate ?deathDate ?img \n "
"WHERE { \n " + query_wiki +  "\n SERVICE wikibase:label { bd:serviceParam wikibase:language 'en' } \n"
"}"
)
  sparql_wiki.setReturnFormat(JSON)
  #sparql_db.setReturnFormat(JSON)
  results = sparql_wiki.query().convert()
  #results1 = sparql_db.query().convert()
  for result in results["results"]["bindings"]:
    img =""
    url = result["item"]["value"]
    name = result["itemLabel"]["value"]
    desc = result["itemDescription"]["value"]
    pers =  {"name": name,"desc" : desc, "url": url}
    if result.__contains__("deathDate") or result.__contains__("birthDate"):
      birth = result["birthDate"]["value"]
      death = result["deathDate"]["value"]
      b = birth.split("T")
      d = death.split("T")
      dates = f"({b[0]} - {d[0]})"
      pers["dates"]=dates
    if result.__contains__("img"):
      img = result["img"]["value"]
    if img is not None or  img != '':
      pers["img"]=img
    persons.append(pers)
  limit = newlimit
  n+=1

jsonfile = persons
#print(jsonfile)
json_obj = json.dumps(jsonfile, indent=7, ensure_ascii = False)
with open("persIndexData1.json", "w") as outfile:
    outfile.write(json_obj)
    print("Done!")

#pip install SPARQLWrapper
import json
from SPARQLWrapper import SPARQLWrapper, JSON
#get json file contianing the data
placedata = {}
with open("Hunt_wikiIds.json", "r") as indexData:
  placedata = json.load(indexData) 
# Preparing data for query
# Getting access keys 
files = placedata.keys()
place = {}
# Organize according to service :@ wikidata
for f in files:
  places = list(placedata[f]["places"].keys())
  if places is not None:
    for n in places:
      place[n] = placedata[f]["places"][n] 

uriswiki = {}
for key in place.keys():
  if place[key] is not None and place[key].__contains__("wikidata"):
    spans = place[key].split("/")
    uriswiki[key] = spans[-1]

qwiki = []

wikilist = list(uriswiki.keys())
print(uriswiki)

query_wiki = ""

# Seting limit of about 25 for query, otherwise system crashes.
limit = 25
for w in wikilist: 
  if wikilist.index(w) <= limit: 
    item = uriswiki[w]
    q = "{BIND(wd:" + item + " AS ?item) \n  OPTIONAL{?item wdt:P625  ?coord; wdt:P18 ?img. \n BIND(geof:longitude(?coord) AS   ?lon) \n BIND(geof:latitude(?coord) AS   ?lat) \n}}"
    qwiki.append(q)
    query_wiki =  " UNION ".join(qwiki)

# To execute query | Pass values for queries
urlWikidata = "https://query.wikidata.org/sparql"
sparql_wiki = SPARQLWrapper(urlWikidata)
query = "\n PREFIX wdt: <http://www.wikidata.org/prop/direct/> \n PREFIX wd: <http://www.wikidata.org/entity/> \n PREFIX wikibase: <http://wikiba.se/ontology#> \n PREFIX geof: <http://www.opengis.net/def/geosparql/function/> \n SELECT DISTINCT ?item ?itemLabel ?itemDescription ?coord ?lon ?lat ?img \n  WHERE { \n " + query_wiki +  "\n SERVICE wikibase:label { bd:serviceParam wikibase:language 'en' } \n }"
print(query)
sparql_wiki.setQuery(query)
sparql_wiki.setReturnFormat(JSON)
results = sparql_wiki.query().convert()

#Organize results
places = []

for result in results["results"]["bindings"]:
  img = ""
  url = result["item"]["value"]
  name = result["itemLabel"]["value"]
  desc = result["itemDescription"]["value"]
  place =  {"name": name,"desc" : desc, "url": url}
  if result.__contains__("lat") or result.__contains__("lon"):
    lat = result["lat"]["value"]
    lon = result["lon"]["value"]
    place["coord"]={"lat" : lat, "lon": lon}
  if result.__contains__("img"):
    img = result["img"]["value"]
  if img is not None or  img != '':
    place["img"]=img
  places.append(place)
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
      q = "{BIND(wd:" + item + " AS ?item) \n  OPTIONAL{?item wdt:P625  ?coord; wdt:P18 ?img. \n BIND(geof:longitude(?coord) AS   ?lon) \n BIND(geof:latitude(?coord) AS   ?lat) \n}}"
      qwiki.append(q)
      query_wiki =  " UNION ".join(qwiki)
  sparql_wiki.setQuery(query)
  sparql_wiki.setReturnFormat(JSON)
  #sparql_db.setReturnFormat(JSON)
  results = sparql_wiki.query().convert()
  #results1 = sparql_db.query().convert()
  for result in results["results"]["bindings"]:
    img = ""
    url = result["item"]["value"]
    name = result["itemLabel"]["value"]
    desc = result["itemDescription"]["value"]
    place =  {"name": name,"desc" : desc, "url": url}
    if result.__contains__("lat") or result.__contains__("lon"):
      lat = result["lat"]["value"]
      lon = result["lon"]["value"]
      place["coord"]={"lat" : lat, "lon": lon}
    if result.__contains__("img"):
      img = result["img"]["value"]
    if img is not None or  img != '':
      place["img"]=img
    places.append(place)

  limit = newlimit
  n+=1

# Create file for with results
jsonfile = places
#print(jsonfile)
json_obj = json.dumps(jsonfile, indent=7, ensure_ascii = False)
with open("placeData_MapIndex.json", "w") as outfile:
    outfile.write(json_obj)
    print("Done!")

# Create files for query
jsonfile1 = query
json_obj1 = json.dumps(jsonfile1, indent=7, ensure_ascii = False)
with open("placesQuery.txt", "w") as outfile:
    outfile.write(json_obj1)
    print("Done!")


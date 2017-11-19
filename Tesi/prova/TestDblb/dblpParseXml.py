import json
import xml.etree.ElementTree as ET
import csv



parser = ET.XMLParser()
parser._parser.UseForeignDTD(True)

parser.entity['nbsp'] = u'\u00A0'
parser.entity['ouml'] = 'U+00D6'
parser.entity['uuml'] = 'U+00FC'
parser.entity['aacute'] = 'U+00C1'
parser.entity['auml'] = 'U+00C4'
parser.entity['eacute'] = 'U+00C9'
parser.entity['Eacute'] = 'U+00C9'
parser.entity['uacute'] = 'U+00DA'
parser.entity['aring'] = 'a'
parser.entity['iacute'] = 'i'
parser.entity['oacute'] = 'o'
parser.entity['szlig'] = 's'
parser.entity['oslash'] = 'o'
parser.entity['ccedil'] = 'c'
parser.entity['yacute'] = 'y'
parser.entity['iuml'] = 'i'
parser.entity['igrave'] = 'i'
parser.entity['ocirc'] = 'o'
parser.entity['icirc'] = 'o'
parser.entity['Uuml'] = 'U'
parser.entity['euml'] = 'e'
parser.entity['acirc'] = 'a'
parser.entity['atilde'] = 'a'
parser.entity['Uacute'] = 'U'
parser.entity['egrave'] = 'e'
parser.entity['times'] = 't'






tree = ET.parse('sample2.xml',parser=parser)
title = []
authors = []
root = tree.getroot()
dataA=[]
dataT=[]

for child in root:
    child.find('title').text

    for author in child.iter('author'):
        dataT.append({'title': child.find('title').text,'author':author.text})


#    jsonD= json.dumps(data)
 #   dataJ = json.loads(jsonD)
  #  lista.append(dataJ)
print(dataT)

lista=[]
#Leggo la lista di dati e li scrivo su file csv
csv= open('test2.csv', 'w')
columnTitleRow = "Autori, Titoli\n"
csv.write(columnTitleRow)
for x in dataT:
  autore = x['author']
  titolo = x['title']
  print(autore,titolo)
  linea = autore.encode('utf-8')+","+titolo.encode('utf-8')+"\n"
  print(linea)
  csv.write(linea)


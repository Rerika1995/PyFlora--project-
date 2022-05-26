
import requests
import json
import xml.etree.ElementTree as ET
from urllib.request import urlopen #provjeri modul, prouci!



def get_temp():
    with urlopen('https://prognoza.hr/prognoza_danas.xml') as URL: #kao i otvaranje file-a, urlopen sluzi za otvaranje url-a? A sve ovo ispod radimo dok je file otvoren, sve izvan, file je zatvoren
        tree = ET.parse(URL)
        root = tree.getroot()[1]
        #tu je file otvoren i mozemo spremiti iz njega, raditi nesto sa njim
    #ovdje je file zatvoren i ne mozemo pristupiti
    

    for child in root: 
        print(child)
        print(f'ovo su svi child attrib{child.attrib}')
        if child.attrib ['name'] == 'Zagreb':
            print(f'ovo je child{child}')
            print(f'ovo je child attrib {child.attrib}')
            for el in child:
                if el.attrib['name'] == 'Tmx': #Tmn je maximalna dnevna temperatura, vidis ime i u xml-u
                    print(el.attrib)  # el.attribute = {'name': 'Tmx', 'value': '26'} sada smo dosli do ovog, u biti dictionary
                    temp = int(el.attrib['value'])
                    print(temp)

    return temp

    #probaj i sa jsonom, da pretvoris u text pa onda prozivas kao dictionary isto 




    
    # response = requests.get(URL)  # request data from this side 
    # return json.loads(response.text) #load that data with json and return/convert to text 

    

import re
import os.path
import urllib.request, json 


def searchDiva(id, types, dateFrom, dateTo):
    search_url = "http://kth.diva-portal.org/smash/export.jsf?format=csl_json&addFilename=true"


    search_url += '&aq=[[{"personId":"' + id + '"},{"dateUpdated":{"from":"' + dateFrom + '","to":"' + dateTo + '"}}]]'
    search_url += '&aqe=[]'
    search_url += '&aq2=[[{"publicationTypeCode":['
    
    for i in range(len(types)):
        search_url += '"' + types[i] + '",'
        
    
    # Remove the last comma to make it valid JSON
    
    search_url = search_url[0:-1]
    
    search_url += ']}]]'
    search_url += '&onlyFullText=false&noOfRows=50&sortOrder=dateIssued_sort_desc&sortOrder2=dateIssued_sort_desc'
    
    data = ""
    
    #print(urllib.request.urlopen(search_url).read())
    
    with urllib.request.urlopen(search_url) as url:
    #    rawData = url.read()
    #    for index in range(0, len(rawData))
    #        print(index + ': ' rawData[index] + ', ')
    #      
    #        if index % 50 == 0
    #            print('\n')
    #      
        rawData = url.read()
        encoding = url.info().get_content_charset('utf-8')
        data = json.loads(rawData.decode(encoding), strict=False)
    
    return data


def escape(s):
    pattern = re.compile(r'(\\|")')
    
    new = pattern.sub(r'\\\1', s)
    
    return new


def stripDate(s):
    #pattern = re.compile('\d{4}[-]\d{2}[-]\d{2}')
    
    return s[0:10]
    
    
def stripAuthor(author_list):
    stripped_author_list = []
    
    for index in range(len(author_list)):
        stripped_author_list.append({key : value for key, value in author_list[index].items() if key == "family" or key == "given"})
    
    return stripped_author_list


def getAllDivaPubs():
    publicationTypes = ["article","book","chapter","conferencePaper","conferenceProceedings"]
    #person_id = "u18ax6vz"
    person_id = "u15fgmo2"
    
    more_publications = True
    
    last_date = ""
    
    pubs = []
          
    while more_publications:
        list = searchDiva(person_id, publicationTypes, "", last_date)
        
        if len(list):
            for index in range(len(list)):
                item = extractPub(list[index])
                
                last_date = item['published']
                
                #print("Last date:" + last_date)
                
                notDuplicate = True
                
                for indexed in range(len(pubs)):
                    if 'DOI' in item and 'DOI' in pubs[indexed] and pubs[indexed]['DOI'] == item['DOI']:
                        notDuplicate = False
                
                if notDuplicate:
                    pubs.append(item)
        else:
            more_publications = False
            
    return pubs
            

def extractPub(pubItem):
    save_keys = ['title','author','year','published','container-title','issue','volume','page','DOI','ISSN','url','status','abstract']
    
    pubItem = {key : value for key, value in pubItem.items() if key in save_keys}
    
    for key in pubItem:
        if key == 'author':
            pubItem['author'] = stripAuthor(pubItem['author'])
        elif key == 'published':
            pubItem['published'] = stripDate(pubItem['published'][0]['raw'])
        elif key == 'type':
            pubItem['publication_type'] = pubItem['type']
            del pubItem['type']
    
    return pubItem



file_to_open = os.path.join("data", "publications.json")

file = open(file_to_open,"w")

pubs = getAllDivaPubs()

print("List of pubs")
print(pubs)

print(len(pubs))

#print(json.dumps(pubs))

file.write(json.dumps(pubs))

file.close()
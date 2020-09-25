import re
import os.path
from scholarly import scholarly

search_query = scholarly.search_author('Carlo Fischione')
author = next(search_query).fill()

# print(author)

#print(author.publications[0].bibtex)
print(author.publications[0])

# Take a closer look at the first publication

def dequote(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s

def wash(s):
    dequote(s)
    
    pattern = re.compile(r'(\\|")')
    
    new = pattern.sub(r'\\\1', s)
    
    return new
    
file_to_open = os.path.join("data", "publications.json")

file = open(file_to_open,"w")

keys = {  'author' : "author",
          'title' : "title",
          'year' : "year",
          'journal' : "journal",
          'volume' : "volume",
          'pages' : "pages",
          'eprint' : "link" }

def pubsJSON(pubList):
    pubs = '{\n' + '"publication": ['
    
    for pub in pubList:
      #try:
      #  pub.fill()
      #except:
      #  pass
      
      
      
      pubInfo = '\n'      
      pubInfo += '{'
      
      if hasattr(pub, 'id_citations'):
        pubInfo += '\n"id": "' + wash( pub.id_citations ) + '",' 

      for key in keys:
        if key in pub.bib:
          pubInfo += '\n"' + keys[key] + '": "' + wash( pub.bib[key] ) + '",'

      pubInfo = pubInfo[0:-1]
      pubInfo += '\n},'

      #print(pubInfo)
      
      pubs += pubInfo
      
     
    pubs = pubs[0:-1]
    pubs += '\n]\n}'

    return pubs

pubs = pubsJSON(author.publications)

print(pubs)

file.write(pubs)

file.close()

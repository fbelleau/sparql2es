from SPARQLWrapper import SPARQLWrapper, JSONLD
from rdflib import Graph
import json


# https://stackoverflow.com/questions/14962485/finding-a-key-recursively-in-a-dictionary

def _finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = _finditem(v, key)
            if item is not None:
                return item

def sparql_construct(uri) :
    sparql = SPARQLWrapper("http://bio2rdf.org/sparql")

    sparql.setQuery("""
        CONSTRUCT {
            ?s ?p ?o .
        }
        WHERE {
            ?s ?p ?o .
            FILTER (?s = <http://bio2rdf.org/mesh:D010145>)
            }
    """)

    sparql.setReturnFormat(JSONLD)
    query = sparql.query()
    print(query)

    results = query.convert()
    #print(results.serialize(format='n3'))
    print(results)



    #sparql.setReturnFormat(XML)
    #results = sparql.query().convert()
    buf = results.serialize(format='json-ld')

    buf = buf.replace("http://bio2rdf.org/","")
    buf = buf.replace("http://purl.org/dc/terms/","dc:")
    buf = buf.replace("http://rdfs.org/ns/void#","void:")
    buf = buf.replace("http://www.w3.org/2000/01/rdf-schema#","rdfs:")
    buf = buf.replace("http://www.w3.org/2001/XMLSchema#","xsd:")
    buf = buf.replace("http://identifiers.org/","identifiers:")

    python_obj = json.loads(buf)
    #print(python_obj)
    python_obj[0][u'mesh_vocabulary:backfile-posting'] = ''

    obj2 = {}
    for k, v in python_obj[0].items():
        print(k, v)

        if type(v) is list:
            vr = []
            for i in v:
                v2 = i
                if type(i) is dict:
                    v2 = i.get('@value')
                    if v2 is None:
                        v2 = i.get('@id')
                vr.append(v2)
            #print(vr)
        print(k, vr)
        obj2[k] = vr

    print(obj2)
    print json.dumps(obj2)

#{"@context": {
#   "schema": "http://schema.org/",
#  	"mesh": "http://bio2rdf.org/mesh:",
#  	"mesh_vocabulary": "http://bio2rdf.org/mesh_vocabulary:",
#  	"bio2rdf": "http://bio2rdf.org/bio2rdf:",
#  	"dc": "http://purl.org/dc/terms/",
#  	"void": "http://rdfs.org/ns/void#",
#  	"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
#  	"xsd": "http://www.w3.org/2001/XMLSchema#",
#  	"identifiers": "http://www.w3.org/2000/01/rdf-schema#",
#  },


sparql_construct("")

import json
import sys

from SPARQLWrapper import SPARQLWrapper, JSONLD
from rdflib import Graph
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'vps216232.vps.ovh.ca', 'port': 9200}])
#print(es)

# https://stackoverflow.com/questions/14962485/finding-a-key-recursively-in-a-dictionary

def _finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = _finditem(v, key)
            if item is not None:
                return item

def sparql_construct(uri_id) :
    sparql = SPARQLWrapper("http://bio2rdf.org/sparql")

    query_construct = """
        CONSTRUCT {
            ?s ?p ?o .
        }
        WHERE {
            ?s ?p ?o .
            FILTER (?s = <http://bio2rdf.org/URI>)
            }
    """

    sparql.setQuery(query_construct.replace('URI', uri_id))

    sparql.setReturnFormat(JSONLD)
    query = sparql.query()

    results = query.convert()
    #print(results.serialize(format='n3'))

    #sparql.setReturnFormat(XML)
    #results = sparql.query().convert()

    buf = results.serialize(format='json-ld')
    #print buf

    buf = buf.replace("_vocabulary","_v")
    buf = buf.replace("http://bio2rdf.org/","")
    buf = buf.replace("http://purl.org/dc/terms/","dc:")
    buf = buf.replace("http://rdfs.org/ns/void#","void:")
    buf = buf.replace("http://www.w3.org/2000/01/rdf-schema#","rdfs:")
    buf = buf.replace("http://www.w3.org/2001/XMLSchema#","xsd:")
    buf = buf.replace("http://identifiers.org/","identifiers:")

    vcontext = {
       "schema": "http://schema.org/",
      	"bio2rdf": "http://bio2rdf.org/",
      	"mesh": "http://bio2rdf.org/mesh:",
      	"mesh_v": "http://bio2rdf.org/mesh_vocabulary:",
        "ctd_v": "http://bio2rdf.org/ctd_vocabulary:",

      	"dc": "http://purl.org/dc/terms/",
      	"void": "http://rdfs.org/ns/void#",
      	"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
      	"xsd": "http://www.w3.org/2001/XMLSchema#",
      	"identifiers": "http://www.w3.org/2000/01/rdf-schema#",
      }

    python_obj = json.loads(buf)
    #print(python_obj)

    obj2 = {}
    obj2['@context'] = vcontext

    for k, v in python_obj[0].items():
        #print(k, v)
        vr = v

        if k == u'mesh_v:backfile-posting':
            #print 'mesh_vocabulary:backfile-posting'
            continue

        id = False
        if type(v) is list:
            vr = []
            for i in v:
                v2 = i
                if type(i) is dict:
                    # remove @value
                    v2 = i.get('@value')
                    if v2 is None:
                        # remove @id identifying URIs
                        v2 = i.get('@id')
                        id = True
                vr.append(v2)
            #print(vr)
        #print(k, vr)

        if id :
            # add @id to identify URIs list
            #obj2[k] = {'@id':vr}
            obj2[k] = vr
        else:
            obj2[k] = vr

    #print(obj2)
    #print json.dumps(obj2)
    res = es.index(index="bio2rdf", doc_type='resource', id=uri_id,  body=json.dumps(obj2))
    print(uri_id, res['result'])

    return json.dumps(obj2)

uri = 'mesh:D010145'
uri = 'mesh:D010144'

uri = sys.argv[1]

#print sparql_construct(uri)
#sparql_construct(uri)

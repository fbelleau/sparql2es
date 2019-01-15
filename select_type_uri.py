import hashlib

from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'vps216232.vps.ovh.ca', 'port': 9200}])
print(es)

uri_type = 'http://bio2rdf.org/kegg_vocabulary:Enzyme'
uri_graph = 'http://bio2rdf.org/hgnc_resource:bio2rdf.dataset.hgnc.R3'

uri_sparql = 'http://bio2rdf.org/sparql'
max = 398950

sparql = SPARQLWrapper(uri_sparql)


query1 = """
select count(distinct ?u) as ?c
  where {
    graph <&GRAPH&> {
    ?u a ?t .
    filter(regex(?u, "bio2rdf"))
}}
"""
sparql.setQuery(query1.replace('&GRAPH&', uri_graph))
sparql.setReturnFormat(JSON)
result = sparql.query().convert()
print(uri_graph, result["results"]["bindings"][0]["c"]["value"])


query2 = """
select distinct(?u) as ?u1
  where {
    graph <&GRAPH&> {
    ?u a ?t .
    filter(regex(?u, "bio2rdf"))
}}
    offset &OFFSET& limit 1000
"""

for offset in range(0, max/1000):
    print(offset)

    #sparql.setQuery(query1.replace('&TYPE&', uri_type).replace('&OFFSET&', str(offset*100)))
    sparql.setQuery(query2.replace('&GRAPH&', uri_graph).replace('&OFFSET&', str(offset*1000)))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    #print(results)

    for result in results["results"]["bindings"]:
        #print(result["t"]["value"], result["u"]["value"])

        doc = {
            'sparql': uri_sparql,
            'graph': uri_graph,
            'uri': result["u1"]["value"],
            'timestamp': datetime.now(),
        }

        hash_object = hashlib.md5(result["u1"]["value"])
        uri_id = hash_object.hexdigest()

        uri_id = result["u1"]["value"].replace('http://bio2rdf.org/','')

        res = es.index(id=uri_id, index="type", doc_type='resource', body=doc)
        print(offset, uri_id, res['result'])

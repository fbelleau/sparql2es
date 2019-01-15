import hashlib

from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'vps216232.vps.ovh.ca', 'port': 9200}])
print(es)

sparql = SPARQLWrapper("http://bio2rdf.org/sparql")

query1 = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?s count(*) as ?c
    WHERE {
        ?s ?p ?o .
        FILTER(?s = <http://dbpedia.org/resource/Semantic_Web>)
    }
"""

query2 = """
    select ?g ?t count(*) as ?c
    where {
graph ?g {
       [] a ?t .
    }}
order by 1 2
"""

sparql.setQuery(query2)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["g"]["value"], result["t"]["value"], result["c"]["value"])

    doc = {
        'graph': result["g"]["value"],
        'type': result["t"]["value"],
        'count': int(result["c"]["value"]),
        'timestamp': datetime.now(),
    }

    hash_object = hashlib.md5(result["g"]["value"]+result["t"]["value"])
    hash_id = hash_object.hexdigest()

    res = es.index(id=hash_id, index="graph", doc_type='resource', body=doc)
    print(res['result'])

from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'vps216232.vps.ovh.ca', 'port': 9200}])
print(es)


res = es.search(index="type-bio2rdf", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    t = hit["_source"]["t"]["value"]
    c =  hit["_source"]["c"]["value"]
    print ''.join([t,'\t',str(c)])

from SPARQLWrapper import SPARQLWrapper, RDFXML, N3, JSONLD
from rdflib import Graph

sparql = SPARQLWrapper("http://bio2rdf.org/sparql")

sparql.setQuery("""
select ?t count(*) as ?c
where {[] a ?t}
order by desc (?c)
""")

sparql.setReturnFormat(N3)
results = sparql.query().convert()
print(results.serialize(format='n3'))
#print(results.serialize(format='jsonld'))
#print(results)

#fb


from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://bio2rdf.org/sparql")

sparql.setQuery("""
select ?t count(*) as ?c
  where {[] a ?t}
  order by desc (?c)
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["t"]["value"], result["c"]["value"])

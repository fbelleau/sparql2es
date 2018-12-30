from SPARQLWrapper import SPARQLWrapper, RDFXML, N3, JSONLD
from rdflib import Graph

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX schema: <http://schema.org/>

    CONSTRUCT {
      ?lang a schema:Language ;
      schema:alternateName ?iso6391Code .
    }
    WHERE {
      ?lang a dbo:Language ;
      dbo:iso6391Code ?iso6391Code .
      FILTER (STRLEN(?iso6391Code)=2) # to filter out non-valid values
    }
""")

sparql.setReturnFormat(N3)
results = sparql.query().convert()
print(results.serialize(format='n3'))
#print(results.serialize(format='jsonld'))
#print(results)

#fb

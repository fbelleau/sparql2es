from SPARQLWrapper import SPARQLWrapper, JSON

def bio2rdf_type_list() :
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

def bio2rdf_type_subject(type_rdf, limit, offset) :
    sparql = SPARQLWrapper("http://bio2rdf.org/sparql")

    sparql_query = """
    select ?s
      where {
        ?s a ?t .
        filter(?t = <http://bio2rdf.org/reactome_vocabulary:Resource>) .
      }
      order by ?s
      limit 1000 offset 2000
    """

    sparql_query = """
    select ?s
      where {
        ?s a ?t .
        filter(?t = <&t>) .
      }
      limit &l offset &o
    """

    sparql_query = sparql_query.replace("&t", type_rdf)
    sparql_query = sparql_query.replace("&l", str(limit))
    sparql_query = sparql_query.replace("&o", str(offset))

    sparql.setQuery(sparql_query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    i = 0
    for result in results["results"]["bindings"]:
        i += 1
        print(result["s"]["value"], i)

#bio2rdf_type_list()

#bio2rdf_type_subject("http://bio2rdf.org/reactome_vocabulary:Resource", 10, 1000)

s = 27782
l = 1000
t = "http://bio2rdf.org/reactome_vocabulary:Resource"

#(u'http://bio2rdf.org/ncbigene_vocabulary:Resource', u'9750395')
s = 9750395
l = 10000
t = "http://bio2rdf.org/ncbigene_vocabulary:Resource"

#for x in range(0, s, l):
for x in range(0, s, l):
  bio2rdf_type_subject(t, l, x)
  print(x)

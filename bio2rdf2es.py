import sys

from sparql_bio2rdf_construct import sparql_construct 

uri = 'mesh:D010145'
uri = 'mesh:D010144'

uri = sys.argv[1]

#print sparql_construct(uri)
sparql_construct(uri)

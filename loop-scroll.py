from elasticsearch import Elasticsearch


def index_loop(pes, pindex, ptype, ppage_size):
	# Initialize the scroll
	page = pes.search(
		index = pindex,
	  	doc_type = ptype,
	  	scroll = '2m',
	  	size = ppage_size,
	  	body = {
			"query":{
				"match_all": {}
				},
				"sort" : [
					{"c.value" : "desc"}
					]
					}
	)

	sid = page['_scroll_id']
	scroll_size = page['hits']['total']
	print scroll_size

	  # Start scrolling
	while (scroll_size > 0):
		print "Scrolling..."
		page = es.scroll(scroll_id = sid, scroll = '2m')
		# Update the scroll ID
		sid = page['_scroll_id']
		# Get the number of results that we returned in the last scroll
		scroll_size = len(page['hits']['hits'])
		print "scroll size: " + str(scroll_size)

		for hit in page['hits']['hits']:
			t = hit["_source"]["t"]["value"]
			c =  hit["_source"]["c"]["value"]
			print ''.join([pindex, '    ', t, '    ', str(c)])
		print
	print


es = Elasticsearch([{'host': 'vps216232.vps.ovh.ca', 'port': 9200}])
print(es)

index_loop(es, 'type-bio2rdf','type',100)
index_loop(es, 'type-ontobee','type',100)
index_loop(es, 'type-agrold','type',100)

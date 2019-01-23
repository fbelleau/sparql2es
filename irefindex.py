#irefindex
# http://irefindex.org/download/irefindex/data/archive/release_15.0/psi_mitab/MITAB2.6/

import hashlib
import json
import re
from datetime import datetime

from elasticsearch import Elasticsearch

def extract_uri(uri_label):
    try:
        m = re.search('(.*?)[(](.*?)[)]', uri_label)
        return m.group(1)
    except:
        return uri_label

def extract_label(uri_label):
    try:
        m = re.search('(.*?)[(](.*?)[)]', uri_label)
        return m.group(1)
    except:
        return uri_label


es = Elasticsearch([{'host': 'vps216232.vps.ovh.ca', 'port': 9200}])
#print(es)

file_in = open("All.mitab.01-22-2018.txt", "r")
ctr = 1

for line in file_in:
    if ctr == 1:
        ctr = ctr + 1
        continue
    values = line.split("\t")
    #print(ctr, values)

    json1 = {
        'iref:uidA_uri':values[0],
        'iref:uidB_uri':values[1],
        'iref:altA_uri':values[2].split("|"),
        'iref:altB_uri':values[3].split("|"),
        'iref:aliasA_uri':values[4].split("|"),
        'iref:aliasB_uri':values[5].split("|"),
        'iref:method_uri':extract_uri(values[6].replace('"',"").replace('psi-mi:',"")),
        'iref:method_label':extract_label(values[6].replace('"',"").replace('psi-mi:',"")),
        'iref:author':values[7],
        'iref:pmids_uri':values[8].split("|"),
        'iref:taxa_uri':extract_uri(values[9]),
        'iref:taxb_uri':extract_uri(values[10]),
        'iref:taxa_label':extract_label(values[9]),
        'iref:taxb_label':extract_label(values[10]),
        'iref:interactionType_uri':extract_uri(values[11].replace('"',"").replace('psi-mi:',"")),
        'iref:interactionType_label':extract_label(values[11].replace('"',"").replace('psi-mi:',"")),
        'iref:sourcedb_uri':extract_uri(values[12]),
        'iref:sourcedb_label':extract_label(values[12]),
        'iref:interactionIdentifier':values[13].split("|"),
        'iref:confidence_uri':values[14].split("|"),
        'iref:expansion':values[15],
        'iref:biological_role_A_uri':extract_uri(values[16]),
        'iref:biological_role_B_uri':extract_uri(values[17]),
        'iref:biological_role_A_label':extract_label(values[16]),
        'iref:biological_role_B_label':extract_label(values[17]),
        'iref:experimental_role_A_uri':extract_uri(values[18]),
        'iref:experimental_role_B_uri':extract_uri(values[19]),
        'iref:experimental_role_A_label':extract_label(values[18]),
        'iref:experimental_role_B_label':extract_label(values[19]),
        'iref:interactor_type_A_uri':extract_uri(values[20]),
        'iref:interactor_type_B_uri':extract_uri(values[21]),
        'iref:interactor_type_A_label':extract_label(values[20]),
        'iref:interactor_type_B_label':extract_label(values[21]),
        'iref:xrefs_A_uri':values[22].split("|"),
        'iref:xrefs_B_uri':values[23].split("|"),
        'iref:xrefs_Interaction_uri':values[24],
        'iref:annotations_A':values[25],
        'iref:annotations_B':values[26],
        'iref:annotations_Interaction':values[27],
        'iref:host_organism_taxid':values[28],
        'iref:parameters_Interaction':values[29],
        'iref:creation_date':values[30],
        'iref:update_date':values[31],
        'iref:checksum_A_uri':values[32],
        'iref:checksum_B_uri':values[33],
        'iref:checksum_Interaction_uri':values[34],
        'iref:negative':values[35],
        'iref:originalReferenceA_uri':values[36],
        'iref:originalReferenceB_uri':values[37],
        'iref:finalReferenceA_uri':values[38],
        'iref:finalReferenceB_uri':values[39],
        'iref:mappingScoreA':values[40],
        'iref:mappingScoreB':values[41],
        'iref:irogida':values[42],
        'iref:irogidb':values[43],
        'iref:irigid':values[44],
        'iref:crogida':values[45],
        'iref:crogidb':values[46],
        'iref:crigid':values[47],
        'iref:icrogida':values[48],
        'iref:icrogidb':values[49],
        'iref:icrigid':values[50],
        'iref:imex_id':values[51],
        'iref:edgetype':values[52],
        'iref:numParticipants':int(values[53].replace("\n",""))
    }
    #print(json1)

    json_txt1 = json.dumps(json1, sort_keys=True)
    #print(json_txt1)
    #uri_id = hashlib.sha256(json_txt1).hexdigest()
    uri_id = hashlib.md5(json_txt1).hexdigest()

    json_context = {
        'iref' : 'http://bio2rdf.org/irefweb_vocabulary:',
        'irefweb' : 'http://bio2rdf.org/irefweb:',
        'bio2rdf' : 'http://bio2rdf.org/'
    }

    json1['@context'] = json_context
    json1['@type'] = 'irefweb_vocabulary:interaction'
    json1['@id'] = 'irefewb:' + uri_id

    json_txt1 = json.dumps(json1, sort_keys=True)
    #print(json_txt1)

    res = es.index(index="irefweb", doc_type='resource', body=json_txt1, id=ctr)
    res['ctr'] = ctr
    res['uri_id'] = uri_id
    res['timestamp'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    print(ctr, uri_id, res['result'])
    #print(ctr, uri_id, res)
    json_txt2 = json.dumps(res, sort_keys=True).replace('_','')
    #print(json_txt2)

    res = es.index(index="log", doc_type='irefweb', body=json_txt2)
    #print(res)

    #there is double in the source file
    #res = es.index(index="irefweb", doc_type='resource', body=json_txt1, id=ctr)
    #print(ctr, uri_id, res['result'])

#    if ctr == 3:
#        break
    ctr = ctr + 1

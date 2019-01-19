#irefindex
# http://irefindex.org/download/irefindex/data/archive/release_15.0/psi_mitab/MITAB2.6/

import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'vps216232.vps.ovh.ca', 'port': 9200}])
#print(es)

file_in = open("../../Downloads/All.mitab.01-22-2018.txt", "r")
ctr = 1

for line in file_in:
    values = line.split("\t")
    #print(ctr, values)

    json1 = {
        'uidA':values[0],
        'uidB':values[1],
        'altA':values[2].split("|"),
        'altB':values[3].split("|"),
        'aliasA':values[4].split("|"),
        'aliasB':values[5].split("|"),
        'method':values[6].replace('"',""),
        'author':values[7],
        'pmids':values[8].split("|"),
        'taxa':values[9],
        'taxb':values[10],
        'interactionType':values[11],
        'sourcedb':values[12],
        'interactionIdentifier':values[13].split("|"),
        'confidence':values[14].split("|"),
        'expansion':values[15],
        'biological_role_A':values[16],
        'biological_role_B':values[17],
        'experimental_role_A':values[18],
        'experimental_role_B':values[19],
        'interactor_type_A':values[20],
        'interactor_type_B':values[21],
        'xrefs_A':values[22].split("|"),
        'xrefs_B':values[23].split("|"),
        'xrefs_Interaction':values[24],
        'Annotations_A':values[25],
        'Annotations_B':values[26],
        'Annotations_Interaction':values[27],
        'Host_organism_taxid':values[28],
        'parameters_Interaction':values[29],
        'Creation_date':values[30],
        'Update_date':values[31],
        'Checksum_A':values[32],
        'Checksum_B':values[33],
        'Checksum_Interaction':values[34],
        'Negative':values[35],
        'OriginalReferenceA':values[36],
        'OriginalReferenceB':values[37],
        'FinalReferenceA':values[38],
        'FinalReferenceB':values[39],
        'MappingScoreA':values[40],
        'MappingScoreB':values[41],
        'irogida':values[42],
        'irogidb':values[43],
        'irigid':values[44],
        'crogida':values[45],
        'crogidb':values[46],
        'crigid':values[47],
        'icrogida':values[48],
        'icrogidb':values[49],
        'icrigid':values[50],
        'imex_id':values[51],
        'edgetype':values[52],
        'numParticipants':values[53].replace("\n","")
    }
    #print(json1)

    json2 = json.dumps(json1)
    #print(json2)

    res = es.index(index="irefindex", doc_type='resource', body=json2)
    print(ctr, res['result'])

#    if ctr == 3:
#        break
    ctr = ctr + 1

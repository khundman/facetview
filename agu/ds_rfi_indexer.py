import csv
import distance
import tika
from tika import parser
from tika import detector
from tika import config
import re
import urllib
tika.initVM()

# curl -XDELETE 'http://search-hyspiri-usewpxxqltz2vmfgyqg2zglosi.us-west-2.es.amazonaws.com/agu_dsi'
# curl -XPOST http://search-hyspiri-usewpxxqltz2vmfgyqg2zglosi.us-west-2.es.amazonaws.com/agu_dsi --data-binary @/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/agu_dsi_map
# curl -s -XPOST search-hyspiri-usewpxxqltz2vmfgyqg2zglosi.us-west-2.es.amazonaws.com/_bulk --data-binary @/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/index_rfp

#(?<!\} \})\n(?!\{ \"index)

doc_counter = 1

def clean(text):
	return text.replace("\"","`").replace("\t","")

with open("/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/dsi_rfp.csv","rU") as rfp:
	with open("/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/index_rfp", "w") as rfp_index:
		reader = csv.reader(rfp)
		for row in reader:
			if reader.line_num > 1:
				rfp_auths = row[1].lower() + " " + row[2].lower()
				affil = row[3].lower() + "::"
				full = row[7]
				title = row[5]
				abstract = clean(row[6])
				# print full
				co_auths = row[4]
				co_auths = re.sub("\([\w, -\.]+\)", "", co_auths)
				if co_auths != "":
					for auth in co_auths.split(","):
						name = auth
						name = re.sub("/\w+", "", name)
						# print name.strip().split(" ")
						first_name = name.strip().split(" ")[0].strip().lower().replace(".","")
						last_name = name.strip().split(" ")[len(name.strip().split(" "))-1].strip().lower().replace(".","")
						# print first_name + " " + last_name
						rfp_auths += "::" + first_name + " " + last_name


				file_extension = re.search("\.pdf|\.docx|\.doc", full).group(0)

				# urllib.urlretrieve(full, "/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/dsi_rfp/dsi_" + str(doc_counter) + file_extension)

				parsed = parser.from_file("/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/dsi_rfp/dsi_" + str(doc_counter) + file_extension)
				content = clean(parsed["content"].encode('utf8'))

				string = '{ "index" : { "_index" : "agu_dsi", "_type" : "type1", "_id" : "%s" } }\n' %(doc_counter)
				rfp_index.write(string.encode('utf8'))

				doc = '''{"authors_only":"%s", "affils_only":"%s", "authors": "%s", "url":"%s", "full_link":"%s", "title":"%s", "abstract":"%s", "type":"DSI_RFP", "content":"%s", "section":"n/a", "authors_both":"%s"}\n''' %(rfp_auths, affil, "n/a", "n/a", full, title ,abstract, content)
				                                                      
				rfp_index.write(doc)
				doc_counter += 1
		rfp_index.write("\n")


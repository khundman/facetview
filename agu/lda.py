import json
import re
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import csv
import distance
import csv
import tika
from tika import parser
from tika import detector
from tika import config
import urllib
tika.initVM()
# import numpy
# import gensim
# from gensim import corpora, models


tokenizer = RegexpTokenizer(r'\w+')

cat = {"EP": "Earth and Planetary Surface Processes", 
"A": "Atmospheric Sciences",
"GC": "Global Environment Change",
"IN": "Earth and Space Science Informatics",
"H": "Hydrology",
"NG": "Nonlinear Geophysics",
"NS": "Near Surface Geophysics", 
"OS":"Ocean Sciences",
"AE": "Atmospheric and Space Electricity",
"T":"Tectonophysics",
"V":"Volcanology",
"MR":"Mineral and Rock Physics",
"S":"Seismology",
"P":"Planetary Sciences",
"NH":"Natural Hazards",
"C":"Cryosphere",
"U":"Union",
"B":"Biogeosciences",
"E":"Education",
"G":"Geodesy",
"GP":"Geomagnetism and Paleomagnetism",
"PP":"Paleoceanography and Paleoclimatology",
"PA":"Public Affairs",
"DI":"Earth's Deep Interior",
"SA":"Aeronomy",
"SM":"Magnetospheric Physics",
"SH":"Solar and Heliospheric Physics",
"TH": "Town Hall",
"ED": "Education"}

es = {"EP": "Earth and Planetary Surface Processes", 
"A": "Atmospheric Sciences",
"GC": "Global Environment Change",
"IN": "Earth and Space Science Informatics",
"H": "Hydrology",
"NG": "Nonlinear Geophysics",
"NS": "Near Surface Geophysics", 
"OS":"Ocean Sciences",
"AE": "Atmospheric and Space Electricity",
"T":"Tectonophysics",
"V":"Volcanology",
"MR":"Mineral and Rock Physics",
"S":"Seismology",
"NH":"Natural Hazards",
"C":"Cryosphere",
"B":"Biogeosciences",
"E":"Education",
"G":"Geodesy",
"GP":"Geomagnetism and Paleomagnetism",
"PP":"Paleoceanography and Paleoclimatology",
"PA":"Public Affairs",
"DI":"Earth's Deep Interior",
"TH": "Town Hall"}

agu_names = []
dsi_names = []


for r in range(1,9):
	count = 0
	lda_string = ""
	with open("/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/index", "r") as index:
		with open("/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/index" + str(r), "w") as new_index:
			content = index.readlines()
			idx = 1
			paper_num = 0

			# for row in content:
			# 	authors = ""
			# 	author_matches = re.finditer("(\"|--)[-\s\w]+::", row)
			# 	for match in author_matches:
			# 		# print match.group(0).replace("::","").replace("\"","").replace("--","") + "::"
			# 		agu_names.append(match.group(0).replace("::","").replace("\"","").replace("--","").lower())
			# doc_counter = 1

			def clean(text):
				return text.replace("\"","`").replace("\t","")

			with open("/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/dsi_rfp.csv","rU") as rfp:
				# with open("/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/index_rfp", "w") as rfp_index:
				reader = csv.reader(rfp)
				for row in reader:
					if reader.line_num > 1:
						rfp_auths = row[1].lower() + " " + row[2].lower()
						affil = row[3].lower() + "::"
						full = row[7]
						title = row[5]
						abstract = clean(row[6])
						names_in_both = ""
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

								dsi_names.append(first_name + " " + last_name)
								if first_name + " " + last_name in agu_names:
									names_in_both += first_name + " " + last_name + "::"




				# 		file_extension = re.search("\.pdf|\.docx|\.doc", full).group(0)

				# 		# urllib.urlretrieve(full, "/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/dsi_rfp/dsi_" + str(doc_counter) + file_extension)

				# 		parsed = parser.from_file("/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/dsi_rfp/dsi_" + str(doc_counter) + file_extension)
				# 		content = clean(parsed["content"].encode('utf8'))

				# 		string = '{ "index" : { "_index" : "agu_dsi", "_type" : "type1", "_id" : "%s" } }\n' %(doc_counter)
				# 		rfp_index.write(string.encode('utf8'))

				# 		doc = '''{"authors_only":"%s", "affils_only":"%s", "authors": "%s", "url":"%s", "full_link":"%s", "title":"%s", "abstract":"%s", "type":"DSI_RFP", "content":"%s", "section":"n/a", "authors_both":"%s"}\n''' %(rfp_auths, affil, "n/a", "n/a", full, title ,abstract, content, names_in_both)
						                                                      
				# 		rfp_index.write(doc)
				# 		doc_counter += 1
				# rfp_index.write("\n")

			for row in content:
				names_in_both2 = ""
				start = 0
				if r > 1:
					start = 2
				if count >= start + ((r-1)*5000) and count <= (r * 5000) + 1:
					if idx % 2 == 1:
						# print row
						row = row.replace("agu_2015","agu_dsi")
						new_index.write(row)
						paper_num = re.search("\d\d\d\d\d", row).group(0)
					else:
						section = ""
						# try:
						try:
							section = re.search("title\":(\s)*\"(\s)*\w+(?=\d)", row).group(0)
							section = section.replace('title":"',"")
							section = re.sub("\d","",section)
							row = row.replace("}", ', "section":"' + cat[section] + '"}')
						except:
							row = row.replace("}", ', "section":"' + section + '"}')

						authors = ""
						author_matches = re.finditer("(\"|--)[-\s\w]+::", row)
						for match in author_matches:
							# print match.group(0).replace("::","").replace("\"","").replace("--","") + "::"
							# names.append(match.group(0).replace("::","").replace("\"","").replace("--","").lower())
							authors += match.group(0).replace("::","").replace("\"","").replace("--","") + "::"
							name = match.group(0).replace("::","").replace("\"","").replace("--","").lower()
							if name in dsi_names:
								names_in_both2 += name + "::"

						affils = ""
						affil_matches = re.finditer("::[\s\w|.,-]+--", row)
						for affil in affil_matches:
							# print affil.group(0).replace("--","").replace("::","") 
							affils += affil.group(0).replace("--","").replace("::","") + "::"

						row = row.replace("}", ', "url":"https://agu.confex.com/agu/fm15/meetingapp.cgi/Paper/' + str(paper_num) + '"}')
						row = row.replace("}", ', "type":"AGU Abstract"}')
						row = row.replace("}", ', "authors_only":"' + authors + '"}')
						row = row.replace("}", ', "affils_only":"' + affils + '"}')
						row = row.replace("}", ', "full_link":""}')
						row = row.replace("}", ', "content":""}')
						row = row.replace("}", ', "authors_both":"' + names_in_both2 +'"}')
						new_index.write(row)
						# except:
						# 	print row
						# 	raise ValueError
							# row = row.replace("}", ', "url":"https://agu.confex.com/agu/fm15/meetingapp.cgi/Paper/' + str(paper_num) + '"}')
							# row = row.replace("}", ', "section":"''"}')
							# new_index.write(row)

						# try:
						# 	section = re.search("title\":(\s)*\"(\s)*\w+(?=\d)", row).group(0)
						# 	section = section.replace('title":"',"")
						# 	section = re.sub("\d","",section)
						# 	check = cat[section]
						# 	title_start = re.search("title\":", row).start() + 10
						# 	# print(row[title_start:])
						# 	title_end = re.search("\"", row[title_start:]).end()
						# 	title = row[title_start+7:title_end + title_start]
							
						# 	lda_string += title
						# except:
						# 	pass
					idx += 1
				else:
					pass
				count += 1

			# print names
			# curl -XDELETE 'http://search-hyspiri-usewpxxqltz2vmfgyqg2zglosi.us-west-2.es.amazonaws.com/agu_dsi'
			# curl -XPOST http://search-hyspiri-usewpxxqltz2vmfgyqg2zglosi.us-west-2.es.amazonaws.com/agu_dsi --data-binary @/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/agu_dsi_map
			# curl -s -XPOST search-hyspiri-usewpxxqltz2vmfgyqg2zglosi.us-west-2.es.amazonaws.com/_bulk --data-binary @/users/hundman/documents/data_science/hyspiri_search/facetview-agu/agu/index_rfp

			#(?<!\} \})\n(?!\{ \"index)

			
		# stop2 = ["university", "authors", "title", "will", "time", "can", "will", 
		# "using", "research", "s", "abstract", 'model', "use", "data", "institute",
		# "observations", "based", "earth", "models", "results", "univers", "system", "1", "high",
		# "laboratory","national", "atmospheric", "different", "processes", "space",
		# "science", "global", "center", "scale", "new", "field", "study", "well", "low", "modeling",
		# "change", "solar", "analysis", "implications", "dynamics", "sea", "land","sea", "effects", "5", '3']

		# raw =  lda_string.lower()
		# tokens = tokenizer.tokenize(raw)
		# en_stop = get_stop_words('en')
		# stopped_tokens = [i for i in tokens if not i in en_stop and not i in stop2]
		# p_stemmer = PorterStemmer()
		# stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
		# texts = []
		# texts.append(stopped_tokens)
		# dictionary = corpora.Dictionary(texts)
		# corpus = [dictionary.doc2bow(text) for text in texts]
		# ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=40)
		# print(ldamodel.print_topics(num_topics=10, num_words=25))

	#stomata
	#global
	#climate change - words, like temperature
	#climate change
	#
	#climate
	#seismic
	#satellite
	#monitoring
	#earthquake
	#climate
	#water
	#temperature
	#global
	#carbon
	#ice
	#ocean

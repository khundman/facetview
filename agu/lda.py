import json
import re
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
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

count = 0
file_split = 10
lda_string = ""
with open("/users/hundman/documents/data_science/hyspiri_search/facetview-hyspiri-public/agu/index", "r") as index:
	with open("/users/hundman/documents/data_science/hyspiri_search/facetview-hyspiri-public/agu/index_new" + str(file_split), "w") as new_index:
		content = index.readlines()
		idx = 1
		paper_num = 0
		for row in content:
			if count >= 42002 and count <= 49001:
				if idx % 2 == 1:
					# print row
					new_index.write(row)
					paper_num = re.search("\d\d\d\d\d", row).group(0)
				else:
					# print row
					try:
						section = re.search("title\":(\s)*\"(\s)*\w+(?=\d)", row).group(0)
						section = section.replace('title":"',"")
						section = re.sub("\d","",section)
						row = row.replace("}", ', "url":"https://agu.confex.com/agu/fm15/meetingapp.cgi/Paper/' + str(paper_num) + '"}')
						row = row.replace("}", ', "section":"' + cat[section] + '"}')
						new_index.write(row)
					except:
						row = row.replace("}", ', "url":"https://agu.confex.com/agu/fm15/meetingapp.cgi/Paper/' + str(paper_num) + '"}')
						row = row.replace("}", ', "section":"''"}')
						new_index.write(row)

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

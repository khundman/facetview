from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import time

output = "/users/hundman/documents/data_science/hyspiri_search/facetview-hyspiri-public/agu/"
driver = webdriver.Firefox()

start = 50000
stop = 100000

with open(output + "index", "a") as out:
	found = 0
	for num in range(start,stop):
		# try:
		driver.get("https://agu.confex.com/agu/fm15/meetingapp.cgi/Paper/" + str(num))
		paper = None
		print str(num)
		try:
			load_time = 3
			if num == start:
				load_time = 10
			WebDriverWait(driver, load_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.item.People")))
			time.sleep(3)
			content = driver.find_element_by_id("main")
			paper = True
		except:
			paper = False
		if paper == True:
			abstract = content.find_element_by_css_selector("section.item.Additional")
			abstract = abstract.text
			if len(abstract) > 1:
				found += 1
				print "found: " + str(found)
				title = content.find_element_by_css_selector("li.itemTitle").text
				all_auths = ""
				auth_affils = ""
				authors = content.find_elements(By.CSS_SELECTOR, "li.RoleListItem")
				for auth in authors:
					affil = auth.find_element_by_tag_name("span").text
					all_auths += auth.find_element_by_tag_name("a").text + "::" + affil + "||"

				string = '{ "index" : { "_index" : "agu_2015", "_type" : "type1", "_id" : "%s" } }\n' %(num)
				out.write(string)

				doc = '''{"authors":"%s", "title":"%s", "abstract":"%s"} \n''' %(all_auths, title, abstract)                                                  
				out.write(doc.encode('utf-8'))
		# except:
		# 	print "issue with: " + str(cnt)
		# 	cnt += 1

	print "found: " + str(found)		                    
	out.write("\n")


driver.close()



#53876
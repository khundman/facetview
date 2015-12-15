from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC

#get title, get affiliations (add with:)
ouptput = "users/hundman/documents/data_science/hyspiri_search/agu/"
driver = webdriver.Firefox()

with open(output + "index", "a") as out:
	# for num in range(57282,99999)
	for num in range(57282,57286):
		driver.get("https://agu.confex.com/agu/fm15/meetingapp.cgi/Paper/" + str(num))
		paper = None
		try:
			content = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "main")))
			paper = True
		except:
			paper = False
		if paper == True:
			abstract = content.find_element_by_css_selector("section.item.Additional")
			abstract = abstract.text.encode('utf-8')
			if len(abstract) > 3:
				all_auths = ""
				auth_affils = ""
				authors = content.find_elements(By.CSS_SELECTOR, "li.RoleListItem")
				for auth in authors:
					affil = auth.find_element_by_tag_name("li").text
					all_auths += auth.find_element_by_tag_name("a").text + "::" + affil + "--"
				print all_auths
				# print all_auths
				# abstract = driver.find_element(By.CLASS_NAME,"item Additional")




				string = '{ "index" : { "_index" : "agu_2015", "_type" : "type1", "_id" : "%s" } }\n' %(doc_counter)
				out.write(string.encode('utf8'))

				doc = '''{"authors":"%s", "title":"%s", ","abstract":"%s"} \n''' %(all_auths, "", abstract)
				                                                      
				out.write(doc)
		                    
	out.write("\n")




driver.close()

#57282 first
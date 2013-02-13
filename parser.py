import xml.etree.ElementTree as ET
import urllib2
import json

# Load urls from table of contents (http://www.helsebiblioteket.no/retningslinjer/hjerneslag/innhold)
result = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.helsebiblioteket.no%2FRetningslinjer%2FProstatakreft%2FInnhold%22%20and%20xpath%3D%22%2F%2F*%5B%40id%3D'leftmenu'%5D%2F%2Fa%22&format=json").read()
data = json.loads(result)
recommendation_ID = 0

root = ET.Element("guidelines")

def fetchMaintext(url):
	# Parse url with xpath="//*[@id='recommendations']/ancestor::div" (Finds all chapters with a recommendation)
	maintext_data = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22"+urllib2.quote(url.encode("utf-8"))+"%22%20and%20xpath%3D%22%2F%2F*%5B%40id%3D'recommendations'%5D%2Fancestor%3A%3Adiv%22").read()
	try:
		print("Trying to fetch main text")

		results = ET.fromstring(maintext_data)
		results_element = results.find("results")

		if len(results.find("results")) > 0:
			global recommendation_ID

			print("Creating recommendation #"+str(recommendation_ID))

			guidelinebreadcrumb = results_element.find(".//*[@id='guidelinebreadcrumb']") # Find first element with id="guidelinebreadcrumb"
			heading = results_element.find("*/h2") # Find first element with tag "h2"
			content = results_element.find(".//*[@id='recommendations']") # Find first element with id="recommendations"

			if recommendation_ID == 0:
				content.__delitem__(0) # Removes "her er en beskrivende tekst"

			recommendation_element = ET.SubElement(root, "recommendation", {"id" : "recommendation"+str(recommendation_ID), "link" : url}) # Create recommendation element with id and link as attributes
			breadcrumb_element = ET.SubElement(recommendation_element, "div", {"class" : "breadcrumbs"})
			breadcrumb_element.extend(guidelinebreadcrumb)

			recommendation_element.append(heading)
			recommendation_element.append(content)

			recommendation_ID += 1

	except Exception, e:
		print(e)

def fetchURLs():
	no_urls = len(data['query']['results']['a'])
	for x in xrange(1,no_urls):
		title = data['query']['results']['a'][x]['content']
		url = data['query']['results']['a'][x]['href']
		print("Fetching recommendation from "+url+" ("+str(x)+"/"+str(no_urls)+")")
		fetchMaintext(url)

	# Create element tree from root element its children
	tree = ET.ElementTree(root)
	# Write tree to file
	tree.write("test.xml")

fetchURLs()
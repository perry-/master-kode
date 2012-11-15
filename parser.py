import xml.etree.ElementTree as ET
import urllib2
import json
import codecs

result = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.helsebiblioteket.no%2FRetningslinjer%2FHjerneslag%2FInnhold%22%20and%20xpath%3D%22%2F%2F*%5B%40id%3D'leftmenu'%5D%2F%2Fa%22&format=json").read()
data = json.loads(result)
recommendation_ID = 0

root = ET.Element("guidelines")


def fetchMaintext(url):
	maintext_data = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22"+urllib2.quote(url.encode("utf-8"))+"%22%20and%20xpath%3D%22%2F%2F*%5B%40id%3D'recommendations'%5D%2Fancestor%3A%3Adiv%2Fpreceding-sibling%3A%3Ah2%7C%2F%2F*%5B%40id%3D'recommendations'%5D%22&format=xml").read()
	try:
		print("Trying to fetch main text")

		results = ET.fromstring(maintext_data)
		results_element = results.find("results")

		if len(results_element) > 0:
			global recommendation_ID

			ET.SubElement(root, "recommendations")
			recommendations = root.find("recommendations")
			recommendations.append(results_element)

			results_element.set("id", "recommendation"+str(recommendation_ID))
			recommendation_ID += 1

	except Exception, e:
		print(e)

def fetchURLs():
	for x in xrange(1,10): #len(data['query']['results']['a'])):
		title = data['query']['results']['a'][x]['content']
		url = data['query']['results']['a'][x]['href']
		#title_node = dom.createTextNode(title)
		#top_element.appendChild(title_node)
		#top_element.appendChild(url.encode("utf-8"))
		#text_file.write("<h3> %s </h3>"%title.encode("utf-8"))
		#text_file.write("<a href="'%s'"> </a>\n"%url.encode("utf-8"))
		print("Fetching recommendation "+str(x)+" from "+url)
		fetchMaintext(url)

		tree = ET.ElementTree(root)
		tree.write("results.xml")

fetchURLs()
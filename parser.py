from xml.dom.minidom import parseString, getDOMImplementation
import urllib2
import json
import codecs

result = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.helsebiblioteket.no%2FRetningslinjer%2FHjerneslag%2FInnhold%22%20and%20xpath%3D%22%2F%2F*%5B%40id%3D'leftmenu'%5D%2F%2Fa%22&format=json").read()
data = json.loads(result)
dom = parseString("<?xml version='1.0' encoding='UTF-8' standalone='yes'?><guidelines></guidelines>")
top_element = dom.documentElement
recommendation_ID = 0

def fetchMaintext(url):
	maintext_data = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22"+urllib2.quote(url.encode("utf-8"))+"%22%20and%20xpath%3D%22%2F%2F*%5B%40id%3D'recommendations'%5D%2Fancestor%3A%3Adiv%2Fpreceding-sibling%3A%3Ah2%7C%2F%2F*%5B%40id%3D'recommendations'%5D%22&format=xml").read()
	try:
		print("Trying to fetch main text")
		dom = parseString(maintext_data)
		maintext_results = dom.getElementsByTagName("results")[0]

		if maintext_results.hasChildNodes():
			global recommendation_ID

			recommendations = dom.createElement("recommendations")
			top_element.appendChild(recommendations)
			recommendations.appendChild(maintext_results)
			
			maintext_results.setAttribute('id', 'recommendation'+str(recommendation_ID))
			maintext_results.setIdAttribute('id')
			recommendation_ID += 1

	except Exception, e:
		print(e)

def fetchURLs():
	for x in xrange(1,10): #len(data['query']['results']['a'])):
		title = data['query']['results']['a'][x]['content']
		url = data['query']['results']['a'][x]['href']
		title_node = dom.createTextNode(title)
		top_element.appendChild(title_node)
		#top_element.appendChild(url.encode("utf-8"))
		#text_file.write("<h3> %s </h3>"%title.encode("utf-8"))
		#text_file.write("<a href="'%s'"> </a>\n"%url.encode("utf-8"))
		print("Fetching recommendation "+str(x)+" from "+url)
		fetchMaintext(url)
	with codecs.open("results.xml", "w", "utf-8") as f:
		top_element.writexml(f)

fetchURLs()
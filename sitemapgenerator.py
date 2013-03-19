import itertools  

file = open('sitemap.txt', 'w')

for x in xrange(0, 120):    
    file.write("http://folk.ntnu.no/chriper/Retningslinjer/recommendations/recommendation"+str(x)+".html\n")
file.close()
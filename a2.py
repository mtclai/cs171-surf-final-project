from BeautifulSoup import BeautifulSoup
import urllib2

#Sample surf spots for testing of getspotdetails function
samplespot="http://www.wannasurf.com/spot/Asia/Bangladesh/Cox_s_Bazar/index.html"
samplespot="http://www.wannasurf.com/spot/Australia_Pacific/New_Caledonia/Nera_Rivermouth/index.html"
samplespot="http://www.wannasurf.com/spot/North_America/USA/Hawaii/Kauai/index.html"

#Find text between two strings
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
		
#Convert degree coordinates to decimal
def conversion(old):
    direction = {'N':-1, 'S':1, 'E': -1, 'W':1}
    new = old.replace('&deg;',' ').replace('\'',' ').replace('"',' ')
    new = new.split()
    new_dir = new.pop()
    new.extend([0,0,0])
    return (float(new[0])+float(new[1])/60.0+float(new[2])/3600.0) * direction[new_dir]

variabletexts=["Distance","Walk","Easy to find?","Public access?","Special access","Wave quality","Experience","Frequency","Type","Direction","Bottom","Power","Normal length","Good day length","Good swell direction","Good wind direction","Swell size","Best tide position","Best tide movement","Week crowd","Week-end crowd"]
variables={}

		
#Get variables based on a surf spot page
def getspotdetails(spoturl):
	url = urllib2.urlopen(spoturl)
	content = url.read()
	soup = BeautifulSoup(content)
	allp = soup.findAll("p")
	alla = soup.findAll("a")
	for a in alla:
		try:
			if a["class"]=="wanna-item-title-subtitle":
				print a.contents.split(",")[0]#country
				print a.contents.split(",")[1]#region
		except:
			pass
	for p in allp:
		if "Latitude:</span>" in str(p):
			Latitude=find_between(str(p),"Latitude:</span>","<br />")
			Latitude=Latitude.replace(" ","")
			Latitude=str(conversion(Latitude)*-1)
			Longitude=str(p).split('Longitude:</span>')[1]
			Longitude=Longitude.replace("</p>","")
			Longitude=Longitude.replace(" ","")
			Longitude=str(conversion(Longitude)*-1)
		for variabletext in variabletexts:
			if variabletext+"</span>" in str(p):
				variables[variabletext]=find_between(str(p).replace(',',';'),"</span>","</p>")
		#print variables
		"""
		if "Distance</span>" in str(p):
			Distance=find_between(str(p).replace(',',';'),"</span>","</p>")
		if "Walk</span>" in str(p):
			Walk=find_between(str(p),"</span>","</p>")
		if "Easy to find?</span>" in str(p):
			Easytofind=find_between(str(p),"</span>","</p>")
		if "Public access?</span>" in str(p):
			Publicaccess=find_between(str(p),"</span>","</p>")
		if "Special access</span>" in str(p):
			Specialaccess=find_between(str(p),"</span>","</p>")
		if "Wave quality</span>" in str(p):
			Wavequality=find_between(str(p),"</span>","</p>")
		if "Experience</span>" in str(p):
			Experience=find_between(str(p),"</span>","</p>")
		if "Frequency</span>" in str(p):
			Frequency=find_between(str(p),"</span>","</p>")
		if "Type</span>" in str(p):
			Type=find_between(str(p),"</span>","</p>")
		if "Direction</span>" in str(p):
			Direction=find_between(str(p),"</span>","</p>")
		if "Bottom</span>" in str(p):
			Bottom=find_between(str(p).replace(',',';'),"</span>","</p>")
		if "Power</span>" in str(p):
			Power=find_between(str(p).replace(',',';'),"</span>","</p>")
		if "Normal length</span>" in str(p):
			Normallength=find_between(str(p),"</span>","</p>")
		if "Good day length</span>" in str(p):
			Gooddaylength=find_between(str(p),"</span>","</p>")
		if "Good swell direction</span>" in str(p):
			Goodswelldirection=find_between(str(p).replace(',',';'),"</span>","</p>")
		if "Good wind direction</span>" in str(p):
			Goodwinddirection=find_between(str(p).replace(',',';'),"</span>","</p>")
		if "Swell size</span>" in str(p):
			Swellsize=find_between(str(p).replace(',',';'),"</span>","</p>")

"""	
	#print type(variables)
	#print len(variables)
	#print variables
	#print variables.keys
	#print type(variables.keys)
	for key in variables:
		#print key
		#print variables[key]
		try:
			fout.write(variables[key]+",")
		except:
			fout.write(",")
			print "Couldn't write variable"
		#print variable.key
		#print variable.value
"""	
	
	#print "Latitude: "+Latitude
	try:
		fout.write(Latitude+",")
	except:
		fout.write(",")
	#print "Longitude: "+Longitude
	try:
		fout.write(Longitude+",")
	except:
		fout.write(",")
	#print "Distance: "+Distance
	try:
		fout.write(Distance+",")
	except:
		fout.write(",")
	#print "Walk: "+Walk
	try:
		fout.write(Walk+",")
	except:
		fout.write(",")
	#print "Easytofind: "+Easytofind
	try:
		fout.write(Easytofind+",")
	except:
		fout.write(",")
	#print "Publicaccess: "+Publicaccess
	try:
		fout.write(Publicaccess+",")
	except:
		fout.write(",")
	#print "Specialaccess: "+Specialaccess
	try:
		fout.write(Specialaccess+",")
	except:
		fout.write(",")
	#print "Wavequality: "+Wavequality
	try:
		fout.write(Wavequality+",")
	except:
		fout.write(",")
	#print "Experience: "+Experience
	try:
		fout.write(Experience+",")
	except:
		fout.write(",")
	#print "Frequency: "+Frequency
	try:
		fout.write(Frequency+",")
	except:
		fout.write(",")
	#print "Type: "+Type
	try:
		fout.write(Type+",")
	except:
		fout.write(",")
	#print "Direction: "+Direction
	try:
		fout.write(Direction+",")
	except:
		fout.write(",")
	#print "Bottom: "+Bottom
	try:
		fout.write(Bottom+",")
	except:
		fout.write(",")
	#print "Power: "+Power
	try:
		fout.write(Power+",")
	except:
		fout.write(",")
	#print "Normallength: "+Normallength
	try:
		fout.write(Normallength+",")
	except:
		fout.write(",")
	#print "Gooddaylength: "+Gooddaylength
	try:
		fout.write(Gooddaylength)
	except:
		fout.write(",")
	try:
		fout.write(Goodswelldirection)
	except:
		fout.write(",")
	try:
		fout.write(Goodwinddirection)
	except:
		fout.write(",")
	try:
		fout.write(Swellsize)
	except:
		fout.write(",")
"""

#Get all country links and execute spot detail search
url = urllib2.urlopen("http://www.wannasurf.com/spot/index.html")
content = url.read()
soup = BeautifulSoup(content)
alllinks = soup.findAll("a")
countrylinks=[]
for link in alllinks:
	#print link["href"]
	if str(link).count('/')==5 and "index.html" in str(link):
		if "/spot/North_America" in str(link) or "/spot/South_America" in str(link) or "/spot/Middle_East" in str(link) or "/spot/Australia_Pacific" in str(link) or "/spot/Central_America" in str(link) or "/spot/Europe" in str(link) or "/spot/Africa" in str(link) or "/spot/Asia" in str(link):
			countrylinks.append("http://www.wannasurf.com"+str(link["href"]))
#print countrylinks


countries=0
fout=open("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/spotlevel.csv", "w")

#print len(variabletexts)
#print variabletexts
for variabletext in variabletexts: 
	fout.write(variabletext+",")
fout.write("\n")

for countrylink in countrylinks:
	#print countrylink
	spotlinks=[]
	countries+=1
	country=countrylink.split('/')[-2]
	print "Country= "+country
	try:
		url = urllib2.urlopen(countrylink)
		print countries
		content = url.read()
		soup = BeautifulSoup(content)
		alllinks = soup.findAll("a")
		for link in alllinks:
			try:
				#print link
				if link["class"]=="wanna-tabzonespot-item-title":
					#print "FOUND A SPOT"
					spotlink="http://www.wannasurf.com"+str(link["href"])
					#print spotlink
					spot=spotlink.split('/')[-2]
					fout.write(spot+","+country+",")
					getspotdetails(spotlink)
					fout.write("\n")
					print "Spot= "+spot
					
					spotlinks.append(link["href"])
			except:
				fout.write("\n")
	except:
		print "Country issue"
	print ""
fout.close()

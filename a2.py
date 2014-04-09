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

	try:
		fout.write(Latitude+",")
	except:
		fout.write(",")
	#print "Longitude: "+Longitude
	try:
		fout.write(Longitude+",")
	except:
		fout.write(",")
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


#Get all country links and execute spot detail search
def getcountrypages():
	url = urllib2.urlopen("http://www.wannasurf.com/spot/index.html")
	content = url.read()
	soup = BeautifulSoup(content)
	alllinks = soup.findAll("a")
	countrypages=[]
	for link in alllinks:
		if str(link).count('/')==5 and "index.html" in str(link):
			if "/spot/North_America" in str(link) or "/spot/South_America" in str(link) or "/spot/Middle_East" in str(link) or "/spot/Australia_Pacific" in str(link) or "/spot/Central_America" in str(link) or "/spot/Europe" in str(link) or "/spot/Africa" in str(link) or "/spot/Asia" in str(link):
				countrypages.append("http://www.wannasurf.com"+str(link["href"]))
	print "All country pages collected"
	return countrypages

#Open output file
fout=open("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/spotlevel.csv", "w")

#Write header for file
fout.write("Spot,Country,Latitude,Longitude,")
for variabletext in variabletexts: 
	fout.write(variabletext+",")
fout.write("\n")

countrypages=getcountrypages()
countrypagewithzonelinks=[]
countrypagewithspotlinks=[]

countries=0#This is just a counter for the first loop

for countrypage in countrypages:
	#If the link contains zones, add to correct list
	try:
		url = urllib2.urlopen(countrypage)
		content = url.read()
		if '<h3 class="wanna-item">Zones</h3>' in str(content):
			print "The below is a country page with zone links:"
			countrypagewithzonelinks.append(countrypage)
		if '<h3 class="wanna-item">Surf Spots</h3>' in str(content):
			print "The below is a country page with spot links:"
			countrypagewithspotlinks.append(countrypage)			
	except:
		pass
	countries+=1
	print str(countries)+": "+countrypage

zonepages=[]
zonepagewithsubzonelinks=[]
zonepagewithspotlinks=[]
	
for countrypagewithzonelink in countrypagewithzonelinks:
	#If the link contains subzones, add to subzonelinks list
	
	#GET THE SPOTS
	try:
		url = urllib2.urlopen(countrypagewithzonelink)
		content = url.read()
		soup = BeautifulSoup(content)
		alllinks = soup.findAll("a")
		
		for link in alllinks:
			if str(link).count('/')==6 and "index.html" in str(link):
				if "/spot/North_America" in str(link) or "/spot/South_America" in str(link) or "/spot/Middle_East" in str(link) or "/spot/Australia_Pacific" in str(link) or "/spot/Central_America" in str(link) or "/spot/Europe" in str(link) or "/spot/Africa" in str(link) or "/spot/Asia" in str(link):
					zonepages.append("http://www.wannasurf.com"+str(link["href"]))
	except:
		pass
zones=0		
for zonepage in zonepages:
	#If the link contains zones, add to correct list
	try:
		url = urllib2.urlopen(zonepage)
		content = url.read()
		if '<h3 class="wanna-item">Zones</h3>' in str(content):
			print "The below is a zone page with subzone links:"
			zonepagewithsubzonelinks.append(zonepage)
		if '<h3 class="wanna-item">Surf Spots</h3>' in str(content):
			print "The below is a zone page with spot links:"
			zonepagewithspotlinks.append(zonepage)			
	except:
		pass
	zones+=1
	print str(zones)+": "+zonepage
print zonepagewithsubzonelinks
	
"""
		if str(link).count('/')==6 and "index.html" in str(link):
			if "/spot/North_America" in str(link) or "/spot/South_America" in str(link) or "/spot/Middle_East" in str(link) or "/spot/Australia_Pacific" in str(link) or "/spot/Central_America" in str(link) or "/spot/Europe" in str(link) or "/spot/Africa" in str(link) or "/spot/Asia" in str(link):
				#BELOW MUST BE ADJUSTED
				countrylinks2.append("http://www.wannasurf.com"+str(link["href"]))
				
		
		
		if '<h3 class="wanna-item">Zones</h3>' in str(content):
			print "Subzonelink:"+zonelink
			subzonelinks.append(zonelink)
		if '<h3 class="wanna-item">Surf Spots</h3>' in str(content):
			print "Spotlink:"+zonelink
			spotlinks.append(zonelink)			
	except:
		pass

for subzonelink in subzonelinks:
	#If the link contains subzones, add to subzonelinks list
	#GET THE SPOTS
	pass
		
	#If the link contains spots, add to spots list
	
#for zones in zonelinks:
	#if the link contains subzones, add to subzone list
	#if the link contains spots, add to spots list
	
#for subzone in subzonelinks
"""
"""
for countrylink in countrylinks:
	#print countrylink
	spotlinks=[]
	zonelinks=[]
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
				if link["class"]=="wanna-tabzonespot-item-title":#AND IF THESE ARE SPOTS
					#print "FOUND A SPOT"
					spotlink="http://www.wannasurf.com"+str(link["href"])
					#print spotlink
					spot=spotlink.split('/')[-2]
					fout.write(spot+","+country+",")
					getspotdetails(spotlink)
					fout.write("\n")
					print "Spot= "+spot
					spotlinks.append(link["href"])
				if link["class"]=="wanna-tabzonespot-item-title" and '<h3 class="wanna-item">Zones</h3>' in str(content):#AND IF THESE ARE ZONES
					print "This is actually a zone page"
					#GET SPOTS< THEN RUN THE ABOVE
			except:
				fout.write("\n")
	except:
		print "Country issue"
	print ""
fout.close()
"""
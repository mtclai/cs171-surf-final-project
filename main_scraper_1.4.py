#cd C:\Users\Alexis\Documents\GitHub\cs171-surf-final-project
#ipython main_scraper_1.4.py

from BeautifulSoup import BeautifulSoup
import urllib2
import time

#Sample surf spots for testing of getspotdetails function
samplespot1="http://www.wannasurf.com/spot/Asia/Bangladesh/Cox_s_Bazar/index.html"
samplespot2="http://www.wannasurf.com/spot/Australia_Pacific/New_Caledonia/Nera_Rivermouth/index.html"
samplespot3="http://www.wannasurf.com/spot/North_America/USA/Hawaii/Kauai/index.html"
samplespot4="http://www.wannasurf.com/spot/Asia/Russia/Far_East/Sakhalin/Sakhalin/index.html"

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
#variabletexts.sort()
variables={}
		
#Get variables based on a surf spot page
def getspotdetails(spoturl):
	url = urllib2.urlopen(spoturl)
	content = url.read()
	soup = BeautifulSoup(content)
	allp = soup.findAll("p")
	alla = soup.findAll("a")
	"""
	for a in alla:
		try:
			if a["class"]=="wanna-item-title-subtitle":
				print a.contents.split(",")[0]#country
				print a.contents.split(",")[1]#zone
				print a.contents.split(",")[2]#subzone
				print a.contents.split(",")[3]#subsubzone
		except:
			pass
	"""
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
	for key in variabletexts:
		#print key
		#print variables[key]
		try:
			fout.write(variables[key]+",")
		except:
			fout.write(",")
			print "Couldn't write variable"

#Open output file
fout=open("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/spotlevel.csv", "w")

#Write header for file
fout.write("Spot,Continent,Country,Zone,Subzone,Subsubzone,Latitude,Longitude,")
for variabletext in variabletexts: 
	fout.write(variabletext+",")
fout.write("\n")


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
	duration=round((time.time()-starttime)*1.0/60,2)
	numberofcountries=len(countrypages)
	print "All "+str(numberofcountries)+" country pages collected in "+str(duration)+" minutes"
	return countrypages



#1A Get all country pages
starttime=time.time()
countrypages=getcountrypages()


#1B Classify country pages
starttime=time.time()
countrypagewithzonelinks=[]
countrypagewithspotlinks=[]

countries=0#This is just a counter for the first loop

for countrypage in countrypages:
	#If the link contains zones, add to correct list
	try:
		url = urllib2.urlopen(countrypage)
		content = url.read()
		if '<h3 class="wanna-item">Zones</h3>' in str(content):
			#print "The below is a country page with zone links:"
			countrypagewithzonelinks.append(countrypage)
		if '<h3 class="wanna-item">Surf Spots</h3>' in str(content):
			#print "The below is a country page with spot links:"
			countrypagewithspotlinks.append(countrypage)			
	except:
		pass
	countries+=1
	#print str(countries)+": "+countrypage
duration=round((time.time()-starttime)*1.0/60,2)
print "All country pages classified in "+str(duration)+" minutes"

	
#2A Get zone pages
starttime=time.time()
zonepages=[]
zonepagewithsubzonelinks=[]
zonepagewithspotlinks=[]

	
for countrypagewithzonelink in countrypagewithzonelinks:
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
duration=round((time.time()-starttime)*1.0/60,2)
numberofzones=len(zonepages)
print "All "+str(numberofzones)+" zone pages collected in "+str(duration)+" minutes"

#2B Classify zone pages
starttime=time.time()
zones=0
for zonepage in zonepages:
	#If the link contains zones, add to correct list
	try:
		url = urllib2.urlopen(zonepage)
		content = url.read()
		if '<h3 class="wanna-item">Zones</h3>' in str(content):
			#print "The below is a zone page with subzone links:"
			zonepagewithsubzonelinks.append(zonepage)
		if '<h3 class="wanna-item">Surf Spots</h3>' in str(content):
			#print "The below is a zone page with spot links:"
			zonepagewithspotlinks.append(zonepage)			
	except:
		pass
	zones+=1
	#print str(zones)+": "+zonepage
duration=round((time.time()-starttime)*1.0/60,2)
print "All zone pages classified in "+str(duration)+" minutes"

#3A Get subzone pages
starttime=time.time()
subzonepages=[]
subzonepagewithsubsubzonelinks=[]
subzonepagewithspotlinks=[]

for zonepagewithsubzonelink in zonepagewithsubzonelinks:
	try:
		url = urllib2.urlopen(zonepagewithsubzonelink)
		content = url.read()
		soup = BeautifulSoup(content)
		alllinks = soup.findAll("a")
		
		for link in alllinks:
			if str(link).count('/')==7 and "index.html" in str(link):
				if "/spot/North_America" in str(link) or "/spot/South_America" in str(link) or "/spot/Middle_East" in str(link) or "/spot/Australia_Pacific" in str(link) or "/spot/Central_America" in str(link) or "/spot/Europe" in str(link) or "/spot/Africa" in str(link) or "/spot/Asia" in str(link):
					subzonepages.append("http://www.wannasurf.com"+str(link["href"]))
	except:
		pass
duration=round((time.time()-starttime)*1.0/60,2)
numberofsubzones=len(subzonepages)
print "All "+str(numberofsubzones)+" subzone pages collected in "+str(duration)+" minutes"

#3B Classify subzone pages
starttime=time.time()
subzones=0		
for subzonepage in subzonepages:
	#If the link contains zones, add to correct list
	try:
		url = urllib2.urlopen(subzonepage)
		content = url.read()
		if '<h3 class="wanna-item">Zones</h3>' in str(content):
			#print "The below is a subzone page with subsubzone links:"
			subzonepagewithsubsubzonelinks.append(subzonepage)
		if '<h3 class="wanna-item">Surf Spots</h3>' in str(content):
			#print "The below is a zone page with spot links:"
			subzonepagewithspotlinks.append(subzonepage)			
	except:
		pass
	subzones+=1
	#print str(subzones)+": "+subzonepage	
duration=round((time.time()-starttime)*1.0/60,2)
print "All subzone pages classified in "+str(duration)+" minutes"


#4A Get subsubzone pages
starttime=time.time()
subsubzonepages=[]
subsubzonepagewithsubsubsubzonelinks=[]
subsubzonepagewithspotlinks=[]

for subzonepagewithsubsubzonelink in subzonepagewithsubsubzonelinks:
	try:
		url = urllib2.urlopen(subzonepagewithsubsubzonelink)
		content = url.read()
		soup = BeautifulSoup(content)
		alllinks = soup.findAll("a")
		for link in alllinks:
			if str(link).count('/')==8 and "index.html" in str(link):
				if "/spot/North_America" in str(link) or "/spot/South_America" in str(link) or "/spot/Middle_East" in str(link) or "/spot/Australia_Pacific" in str(link) or "/spot/Central_America" in str(link) or "/spot/Europe" in str(link) or "/spot/Africa" in str(link) or "/spot/Asia" in str(link):
					subsubzonepages.append("http://www.wannasurf.com"+str(link["href"]))
	except:
		pass
duration=round((time.time()-starttime)*1.0/60,2)
numberofsubsubzones=len(subsubzonepages)
print "All "+str(numberofsubsubzones)+" subsubzone pages collected in "+str(duration)+" minutes"

#4B Classify subsubzone pages
starttime=time.time()
subsubzones=0		
for subsubzonepage in subsubzonepages:
	#If the link contains zones, add to correct list
	try:
		url = urllib2.urlopen(subsubzonepage)
		content = url.read()
		if '<h3 class="wanna-item">Zones</h3>' in str(content):
			#print "The below is a subsubzone page with subsubsubzone links:"
			subsubzonepagewithsubsubsubzonelinks.append(subsubzonepage)
		if '<h3 class="wanna-item">Surf Spots</h3>' in str(content):
			#print "The below is a zone page with spot links:"
			subsubzonepagewithspotlinks.append(subsubzonepage)			
	except:
		pass
	subsubzones+=1
duration=round((time.time()-starttime)*1.0/60,2)
print "All subsubzone pages classified in "+str(duration)+" minutes"


print "countrypagewithzonelinks"
print countrypagewithzonelinks
print ""
print "countrypagewithspotlinks"
print countrypagewithspotlinks
print ""
print "zonepagewithsubzonelinks"
print zonepagewithsubzonelinks
print ""
print "zonepagewithspotlinks"
print zonepagewithspotlinks
print ""
print "subzonepagewithsubsubzonelinks"
print subzonepagewithsubsubzonelinks
print ""
print "subzonepagewithspotlinks"
print subzonepagewithspotlinks
print ""
print "subsubzonepagewithsubsubsubzonelinks"
print subsubzonepagewithsubsubsubzonelinks
print ""
print "subsubzonepagewithspotlinks"
print subsubzonepagewithspotlinks

	
allwithspotlinks=countrypagewithspotlinks+zonepagewithspotlinks+subzonepagewithspotlinks+subsubzonepagewithspotlinks

links=0
starttime=time.time()
for pagewithspotlink in allwithspotlinks:
	spotlinks=[]
	zonelinks=[]
	links+=1
	if pagewithspotlink in countrypagewithspotlinks:
		continent=pagewithspotlink.split('/')[-3]####
		country=pagewithspotlink.split('/')[-2]
		zone=''
		subzone=''
		subsubzone=''
	if pagewithspotlink in zonepagewithspotlinks:
		continent=pagewithspotlink.split('/')[-4]####
		country=pagewithspotlink.split('/')[-3]
		zone=pagewithspotlink.split('/')[-2]
		subzone=''
		subsubzone=''
	if pagewithspotlink in subzonepagewithspotlinks:
		continent=pagewithspotlink.split('/')[-5]####
		country=pagewithspotlink.split('/')[-4]
		zone=pagewithspotlink.split('/')[-3]
		subzone=pagewithspotlink.split('/')[-2]
		subsubzone=''
	if pagewithspotlink in subsubzonepagewithspotlinks:
		continent=pagewithspotlink.split('/')[-6]####
		country=pagewithspotlink.split('/')[-5]
		zone=pagewithspotlink.split('/')[-4]
		subzone=pagewithspotlink.split('/')[-3]
		subsubzone=pagewithspotlink.split('/')[-2]
	try:
		url = urllib2.urlopen(pagewithspotlink)
		print links
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
					fout.write(spot+","+continent+","+country+","+zone+","+subzone+","+subsubzone+",")
					getspotdetails(spotlink)
					fout.write("\n")
					print "Spot= "+spot
					spotlinks.append(link["href"])
				if link["class"]=="wanna-tabzonespot-item-title" and '<h3 class="wanna-item">Zones</h3>' in str(content):#AND IF THESE ARE ZONES
					print "This is actually a zone page"
					#GET SPOTS THEN RUN THE ABOVE
			except:
				pass
				#fout.write("\n")
	except:
		print "Country issue"
	print ""
duration=round((time.time()-starttime)*1.0/60,2)
print "All spot details gathered into csv in "+str(duration)+" minutes"

fout.close()
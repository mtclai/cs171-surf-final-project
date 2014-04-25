#cd C:\Users\Alexis\Documents\GitHub\cs171-surf-final-project
#ipython season_scraper_1.0.py

from BeautifulSoup import BeautifulSoup
import urllib2
import time

zonesample="http://www.wannasurf.com/spot/Australia_Pacific/Australia/QLD/Far_North_West/index.html"

#Find all zones
input_filename="C:/Users/Alexis/Documents/GitHub/cs171-surf-final-project/data/spotlevel_v1.csv"
linenumber=0
urls=[]
for line in open(input_filename):
	#print "line "+str(linenumber)
	if linenumber==0:
		#output_filename.write(str(line).replace("\n",",")+"forecast_day0_day,forecast_day0_mintemp,forecast_day0_maxtemp,forecast_day0_image,forecast_day1_day,forecast_day1_mintemp,forecast_day1_maxtemp,forecast_day1_image,forecast_day2_day,forecast_day2_mintemp,forecast_day2_maxtemp,forecast_day2_image,forecast_day3_day,forecast_day3_mintemp,forecast_day3_maxtemp,forecast_day3_image\n")
		pass
	else:
		line = line.rstrip().split(",")
		if line[2]=="":
			url="http://www.wannasurf.com/spot/"+str(line[1])+"/index.html"
			#print url
		elif line[3]==0:
			url="http://www.wannasurf.com/spot/"+str(line[1])+"/"+str(line[2])+"/index.html"
			#print url
		elif line[4]==0:
			url="http://www.wannasurf.com/spot/"+str(line[1])+"/"+str(line[2])+"/"+str(line[3])+"/index.html"
			#print url
		else:
			url="http://www.wannasurf.com/spot/"+str(line[1])+"/"+str(line[2])+"/"+str(line[3])+"/"+str(line[4])+"/index.html"
			#print url
	try:
		urls.append(url)
	except:
		pass
	linenumber+=1			

			
#Find text between two strings
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getzonedetails(zoneurl):
	url = urllib2.urlopen(zoneurl)
	content = url.read()
	soup = BeautifulSoup(content)
	alltable = soup.findAll("table")
	
	#Identify the table with seasons data
	for table in alltable:
		try:
			if table["id"]=="wanna-season-table":
				seasontable=table
		except:
			pass

	
	alltr = seasontable.findAll("tr")

	bestsurfingseason= alltr[2].findAll("td")
	typicalswellsize= alltr[3].findAll("td")
	surfequipment= alltr[4].findAll("td")
	watertemp= alltr[5].findAll("td")
	airtemp= alltr[6].findAll("td")
	climate= alltr[7].findAll("td")

	bestsurfingseason_janfeb=bestsurfingseason[1]
	if "1" in str(bestsurfingseason_janfeb):
		bestsurfingseason_janfeb=1
	if "2" in str(bestsurfingseason_janfeb):
		bestsurfingseason_janfeb=2
	if "3" in str(bestsurfingseason_janfeb):
		bestsurfingseason_janfeb=3
	if "4" in str(bestsurfingseason_janfeb):
		bestsurfingseason_janfeb=4
	if "5" in str(bestsurfingseason_janfeb):
		bestsurfingseason_janfeb=5
		
	bestsurfingseason_marapr=bestsurfingseason[2]
	if "1" in str(bestsurfingseason_marapr):
		bestsurfingseason_marapr=1
	if "2" in str(bestsurfingseason_marapr):
		bestsurfingseason_marapr=2
	if "3" in str(bestsurfingseason_marapr):
		bestsurfingseason_marapr=3
	if "4" in str(bestsurfingseason_marapr):
		bestsurfingseason_marapr=4
	if "5" in str(bestsurfingseason_marapr):
		bestsurfingseason_marapr=5
		
	bestsurfingseason_mayjun=bestsurfingseason[3]
	if "1" in str(bestsurfingseason_mayjun):
		bestsurfingseason_mayjun=1
	if "2" in str(bestsurfingseason_mayjun):
		bestsurfingseason_mayjun=2
	if "3" in str(bestsurfingseason_mayjun):
		bestsurfingseason_mayjun=3
	if "4" in str(bestsurfingseason_mayjun):
		bestsurfingseason_mayjun=4
	if "5" in str(bestsurfingseason_mayjun):
		bestsurfingseason_mayjun=5
		
	bestsurfingseason_julaug=bestsurfingseason[4]
	if "1" in str(bestsurfingseason_julaug):
		bestsurfingseason_julaug=1
	if "2" in str(bestsurfingseason_julaug):
		bestsurfingseason_julaug=2
	if "3" in str(bestsurfingseason_julaug):
		bestsurfingseason_julaug=3
	if "4" in str(bestsurfingseason_julaug):
		bestsurfingseason_julaug=4
	if "5" in str(bestsurfingseason_julaug):
		bestsurfingseason_julaug=5

	bestsurfingseason_septoct=bestsurfingseason[5]
	if "1" in str(bestsurfingseason_septoct):
		bestsurfingseason_septoct=1
	if "2" in str(bestsurfingseason_septoct):
		bestsurfingseason_septoct=2
	if "3" in str(bestsurfingseason_septoct):
		bestsurfingseason_septoct=3
	if "4" in str(bestsurfingseason_septoct):
		bestsurfingseason_septoct=4
	if "5" in str(bestsurfingseason_septoct):
		bestsurfingseason_septoct=5
		
	bestsurfingseason_novdec=bestsurfingseason[6]
	if "1" in str(bestsurfingseason_novdec):
		bestsurfingseason_novdec=1
	if "2" in str(bestsurfingseason_novdec):
		bestsurfingseason_novdec=2
	if "3" in str(bestsurfingseason_novdec):
		bestsurfingseason_novdec=3
	if "4" in str(bestsurfingseason_novdec):
		bestsurfingseason_novdec=4
	if "5" in str(bestsurfingseason_novdec):
		bestsurfingseason_novdec=5

		
	
	typicalswellsize_janfeb=typicalswellsize[1]
	if "1" in str(typicalswellsize_janfeb):
		typicalswellsize_janfeb=1
	if "2" in str(typicalswellsize_janfeb):
		typicalswellsize_janfeb=2
	if "3" in str(typicalswellsize_janfeb):
		typicalswellsize_janfeb=3
	if "4" in str(typicalswellsize_janfeb):
		typicalswellsize_janfeb=4
	if "5" in str(typicalswellsize_janfeb):
		typicalswellsize_janfeb=5
	if "4" in str(typicalswellsize_janfeb):
		typicalswellsize_janfeb=6
	if "5" in str(typicalswellsize_janfeb):
		typicalswellsize_janfeb=7
		
	typicalswellsize_marapr=typicalswellsize[2]
	if "1" in str(typicalswellsize_marapr):
		typicalswellsize_marapr=1
	if "2" in str(typicalswellsize_marapr):
		typicalswellsize_marapr=2
	if "3" in str(typicalswellsize_marapr):
		typicalswellsize_marapr=3
	if "4" in str(typicalswellsize_marapr):
		typicalswellsize_marapr=4
	if "5" in str(typicalswellsize_marapr):
		typicalswellsize_marapr=5
	if "4" in str(typicalswellsize_marapr):
		typicalswellsize_marapr=6
	if "5" in str(typicalswellsize_marapr):
		typicalswellsize_marapr=7
		
	typicalswellsize_mayjun=typicalswellsize[3]
	if "1" in str(typicalswellsize_mayjun):
		typicalswellsize_mayjun=1
	if "2" in str(typicalswellsize_mayjun):
		typicalswellsize_mayjun=2
	if "3" in str(typicalswellsize_mayjun):
		typicalswellsize_mayjun=3
	if "4" in str(typicalswellsize_mayjun):
		typicalswellsize_mayjun=4
	if "5" in str(typicalswellsize_mayjun):
		typicalswellsize_mayjun=5
	if "4" in str(typicalswellsize_mayjun):
		typicalswellsize_mayjun=6
	if "5" in str(typicalswellsize_mayjun):
		typicalswellsize_mayjun=7
		
	typicalswellsize_julaug=typicalswellsize[4]
	if "1" in str(typicalswellsize_julaug):
		typicalswellsize_julaug=1
	if "2" in str(typicalswellsize_julaug):
		typicalswellsize_julaug=2
	if "3" in str(typicalswellsize_julaug):
		typicalswellsize_julaug=3
	if "4" in str(typicalswellsize_julaug):
		typicalswellsize_julaug=4
	if "5" in str(typicalswellsize_julaug):
		typicalswellsize_julaug=5
	if "4" in str(typicalswellsize_julaug):
		typicalswellsize_julaug=6
	if "5" in str(typicalswellsize_julaug):
		typicalswellsize_julaug=7

	typicalswellsize_septoct=typicalswellsize[5]
	if "1" in str(typicalswellsize_septoct):
		typicalswellsize_septoct=1
	if "2" in str(typicalswellsize_septoct):
		typicalswellsize_septoct=2
	if "3" in str(typicalswellsize_septoct):
		typicalswellsize_septoct=3
	if "4" in str(typicalswellsize_septoct):
		typicalswellsize_septoct=4
	if "5" in str(typicalswellsize_septoct):
		typicalswellsize_septoct=5
	if "4" in str(typicalswellsize_septoct):
		typicalswellsize_septoct=6
	if "5" in str(typicalswellsize_septoct):
		typicalswellsize_septoct=7
		
	typicalswellsize_novdec=typicalswellsize[6]
	if "1" in str(typicalswellsize_novdec):
		typicalswellsize_novdec=1
	if "2" in str(typicalswellsize_novdec):
		typicalswellsize_novdec=2
	if "3" in str(typicalswellsize_novdec):
		typicalswellsize_novdec=3
	if "4" in str(typicalswellsize_novdec):
		typicalswellsize_novdec=4
	if "5" in str(typicalswellsize_novdec):
		typicalswellsize_novdec=5
	if "4" in str(typicalswellsize_novdec):
		typicalswellsize_novdec=6
	if "5" in str(typicalswellsize_novdec):
		typicalswellsize_novdec=7	

		

	surfequipment_janfeb=find_between(str(surfequipment[1]), "<td>", "</td>" )
	surfequipment_marapr=find_between(str(surfequipment[2]), "<td>", "</td>" )
	surfequipment_mayjun=find_between(str(surfequipment[3]), "<td>", "</td>" )
	surfequipment_julaug=find_between(str(surfequipment[4]), "<td>", "</td>" )
	surfequipment_septoct=find_between(str(surfequipment[5]), "<td>", "</td>" )
	surfequipment_novdec=find_between(str(surfequipment[6]), "<td>", "</td>" )
		

		
	watertemp_janfeb=find_between(str(watertemp[1]), "br />", "°" )
	watertemp_marapr=find_between(str(watertemp[2]), "br />", "°" )
	watertemp_mayjun=find_between(str(watertemp[3]), "br />", "°" )
	watertemp_julaug=find_between(str(watertemp[4]), "br />", "°" )
	watertemp_septoct=find_between(str(watertemp[5]), "br />", "°" )
	watertemp_novdec=find_between(str(watertemp[6]), "br />", "°" )

	
	
	airtemp_janfeb=find_between(str(airtemp[1]), "br />", "°" )
	airtemp_marapr=find_between(str(airtemp[2]), "br />", "°" )
	airtemp_mayjun=find_between(str(airtemp[3]), "br />", "°" )
	airtemp_julaug=find_between(str(airtemp[4]), "br />", "°" )
	airtemp_septoct=find_between(str(airtemp[5]), "br />", "°" )
	airtemp_novdec=find_between(str(airtemp[6]), "br />", "°" )

	
	
	climate_janfeb=find_between(str(climate[1]), "weather-", ".gif" )
	climate_marapr=find_between(str(climate[2]), "weather-", ".gif" )
	climate_mayjun=find_between(str(climate[3]), "weather-", ".gif" )	
	climate_julaug=find_between(str(climate[4]), "weather-", ".gif" )
	climate_septoct=find_between(str(climate[5]), "weather-", ".gif" )
	climate_novdec=find_between(str(climate[6]), "weather-", ".gif" )
	
	return bestsurfingseason_janfeb, bestsurfingseason_marapr, bestsurfingseason_mayjun, bestsurfingseason_julaug, bestsurfingseason_septoct, bestsurfingseason_novdec, typicalswellsize_janfeb, typicalswellsize_marapr, typicalswellsize_mayjun, typicalswellsize_julaug, typicalswellsize_septoct, typicalswellsize_novdec, surfequipment_janfeb, surfequipment_marapr, surfequipment_mayjun, surfequipment_julaug, surfequipment_septoct, surfequipment_novdec, watertemp_janfeb, watertemp_marapr, watertemp_mayjun, watertemp_julaug, watertemp_septoct, watertemp_novdec, airtemp_janfeb, airtemp_marapr, airtemp_mayjun, airtemp_julaug, airtemp_septoct, airtemp_novdec, climate_janfeb, climate_marapr, climate_mayjun, climate_julaug, climate_septoct, climate_novdec
				
for url in urls:
	print url
	seasonalinfo=getzonedetails(url)
	print seasonalinfo
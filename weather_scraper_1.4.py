import pandas as pd
import time

#Find text between two strings
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

#Set initial variables
wundergroundid="593a0a244701479b"
samplelatitude=30.00
samplelongitude=-20.00


def findweather(latitude,longitude,day):
	forecasturl="http://api.wunderground.com/api/593a0a244701479b/forecast/q/"+str(latitude)+","+str(longitude)+".json"
	forecastjson=pd.read_json(forecasturl)
	#forecastjson.to_csv("tempcsv.csv")
	forecast=forecastjson.loc["simpleforecast",0]
	#forecast=pd.read_json(forecast)
	forecast=str(forecast).split("'")
	data=[]
	for i in range(len(forecast)):
		if forecast[i]=="weekday":
			data.append(forecast[i+2])
		if forecast[i]=="fahrenheit":
			data.append(forecast[i+2])
		if "http" in forecast[i]:
			data.append(forecast[i])

	weekday=data[3+4*day]
	mintemp=data[2+4*day]
	maxtemp=data[1+4*day]
	image=data[0+4*day]
	time.sleep(7)#This is to avoid API limit
	print "One forecast fetched: "
	print weekday,mintemp,maxtemp,image
	return weekday,mintemp,maxtemp,image

input_filename="C:/Users/Alexis/Documents/GitHub/cs171-surf-final-project/data/spotlevel_v1.csv"
output_filename=open("C:/Users/Alexis/Documents/GitHub/cs171-surf-final-project/data/spotlevel_withforecast.csv", "w")

linenumber=0
print "test"
for line in open(input_filename):
	print "line "+str(linenumber)
	if linenumber==0:
		output_filename.write(str(line).replace("\n",",")+"forecast_day0_day,forecast_day0_mintemp,forecast_day0_maxtemp,forecast_day0_image,forecast_day1_day,forecast_day1_mintemp,forecast_day1_maxtemp,forecast_day1_image,forecast_day2_day,forecast_day2_mintemp,forecast_day2_maxtemp,forecast_day2_image,forecast_day3_day,forecast_day3_mintemp,forecast_day3_maxtemp,forecast_day3_image\n")
		pass
	else:
		line = line.rstrip().split(",")
		lat=line[5]
		lon=line[6]
		try:
			forecast_day0=findweather(lat,lon,0)
			forecast_day1=findweather(lat,lon,1)
			forecast_day2=findweather(lat,lon,2)
			forecast_day3=findweather(lat,lon,3)
		except:
			forecast_day0=['','','','']
			forecast_day1=['','','','']
			forecast_day2=['','','','']
			forecast_day3=['','','','']
		for element in line:
			output_filename.write(element+",")
		output_filename.write(forecast_day0[0]+","+forecast_day0[1]+","+forecast_day0[2]+","+forecast_day0[3]+","+forecast_day1[0]+","+forecast_day1[1]+","+forecast_day1[2]+","+forecast_day1[3]+","+forecast_day2[0]+","+forecast_day2[1]+","+forecast_day2[2]+","+forecast_day2[3]+","+forecast_day3[0]+","+forecast_day3[1]+","+forecast_day3[2]+","+forecast_day3[3])
		output_filename.write("\n")
		
	linenumber+=1
	
output_filename.close()
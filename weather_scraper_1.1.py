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

table=pd.read_csv("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/Site_table_dummy4.csv")	

def f(x):
	try:
		return findweather(x[5],x[6],0)
	except:
		return [0,0,0,0]
def g(x):
	try:
		return findweather(x[5],x[6],1)
	except:
		return [0,0,0,0]
def h(x):
	try:
		return findweather(x[5],x[6],2)
	except:
		return [0,0,0,0]
def i(x):
	try:
		return findweather(x[5],x[6],3)
	except:
		return [0,0,0,0]
table["weather_day0"]=table.apply(f, axis=1)
table["weather_day1"]=table.apply(g, axis=1)
table["weather_day2"]=table.apply(h, axis=1)
table["weather_day3"]=table.apply(i, axis=1)

#table=table.apply(lambda x: table["weather_day1"]=findweather(table["Latitude"],table["Longitude"],1)
table.to_csv("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/temptable.csv")
#print weather


#Get nearby country and station
#stationurl="http://api.wunderground.com/api/"+wundergroundid+"/geolookup/q/"+str(latitude)+","+str(longitude)+".json"
#stationjson=pd.read_json(stationurl)
#stationjson.to_csv("tempcsv.csv")
#nearbystations=stationjson.loc["nearby_weather_stations",0]
#nearbycity=find_between(str(nearbystations), "city': u'", "', u'country" )
#nearbycountry=find_between(str(nearbystations), "country': u'", "', u'lon" )
#print nearbycity
#print nearbycountry
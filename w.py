#import urllib2
#import json
#import simplejson
import pandas as pd

#Find text between two strings
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

wundergroundid="593a0a244701479b"
latitude=50.00
longitude=10.00

url="http://api.wunderground.com/api/"+wundergroundid+"/geolookup/q/"+str(latitude)+","+str(longitude)+".json"
#req = urllib2.Request(url)
#opener = urllib2.build_opener()
#f = opener.open(req)
#simplejson.load(f)

j=pd.read_json(url)
j.to_csv("tempcsv.csv")
print j.loc["nearby_weather_stations",0]
#print j.head(15)
#print ""
#print f

#json_data=open(url)
#data = json.load(json_data)
#print data
#json_data.close()

#page = urllib2.urlopen(url)
#page = page.read()
#print page

#Get closest stations
#http://api.wunderground.com/api/593a0a244701479b/geolookup/q/37.776289,-122.395234.json
#Get weather based on city
#http://api.wunderground.com/api/593a0a244701479b/forecast/q/CA/San_Francisco.json
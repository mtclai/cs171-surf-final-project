#Join 
import pandas as pd
import numpy as np
pd.set_option('display.width', 10000)
pd.set_option('display.max_colwidth', 10000)

firstpart = pd.read_csv("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/spotlevel_v2.csv",index_col=False)
secondpart = pd.read_csv("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/spotlevel_seasons.csv",index_col=False)

#Create the key in the left part for joining
firstpart["Key"]="http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/"+firstpart["Zone"]+"/"+firstpart["Subzone"]+"/"+firstpart["Subsubzone"]+"/index.html"
firstpart.ix[firstpart.Subsubzone.isnull(),"Key"] = "http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/"+firstpart["Zone"]+"/"+firstpart["Subzone"]+"/index.html"
firstpart.ix[firstpart.Subzone.isnull(),"Key"] = "http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/"+firstpart["Zone"]+"/index.html"
firstpart.ix[firstpart.Zone.isnull(),"Key"] = "http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/index.html"

firstpart=firstpart.set_index("Key", drop=True)
secondpart=secondpart.set_index("Zone url", drop=True)

#print firstpart.shape
#print secondpart.shape

merged=firstpart.join(secondpart)
merged=merged.replace("<td>&nbsp;</td>","")

merged["Distance_num"]=""
merged.ix[merged.Distance=="Sell the house; wife and kids","Distance_num"] = 1
merged.ix[merged.Distance=="Surf trip","Distance_num"] = 2
merged.ix[merged.Distance=="Week-end trip","Distance_num"] = 3
merged.ix[merged.Distance=="Day trip","Distance_num"] = 4
merged.ix[merged.Distance=="Take a car","Distance_num"] = 5
merged.ix[merged.Distance=="In the city","Distance_num"] = 6

merged.to_csv("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/spotlevel_withseason_filtered_ordinal.csv")



#create ordinal values
#filter


#firstpart.ix[firstpart.Country =="Algeria","Key"] = "http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/"+firstpart["Spot"]+"/index.html"
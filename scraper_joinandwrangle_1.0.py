#Join 
import pandas as pd
import numpy as np
pd.set_option('display.width', 10000)
pd.set_option('display.max_colwidth', 10000)

log=open("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/log.txt", "w")
firstpart = pd.read_csv("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/spotlevel_v2.csv",index_col=False)
secondpart = pd.read_csv("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/spotlevel_seasons_2.csv",index_col=False)

#Create the key in the left part for joining
firstpart["Key"]="http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/"+firstpart["Zone"]+"/"+firstpart["Subzone"]+"/"+firstpart["Subsubzone"]+"/index.html"
firstpart.ix[firstpart.Subsubzone.isnull(),"Key"] = "http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/"+firstpart["Zone"]+"/"+firstpart["Subzone"]+"/index.html"
firstpart.ix[firstpart.Subzone.isnull(),"Key"] = "http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/"+firstpart["Zone"]+"/index.html"
firstpart.ix[firstpart.Zone.isnull(),"Key"] = "http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/index.html"

firstpart=firstpart.set_index("Key", drop=True)
secondpart=secondpart.set_index("Zone url", drop=True)

#print firstpart["Key"].head(10)
#print secondpart["Zone url"].head(10)

print firstpart.shape
print secondpart.shape

#merged=firstpart.join(secondpart)

#merged=pd.merge(firstpart, secondpart, left_on="Key", right_on="Zone url", how='inner')
#merged.to_csv("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/temp.csv")

#log.write(str(firstpart["Key"].head(10)))

log.close()

#erase all <td>&nbsp;</td>



#firstpart.ix[firstpart.Country =="Algeria","Key"] = "http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/"+firstpart["Spot"]+"/index.html"
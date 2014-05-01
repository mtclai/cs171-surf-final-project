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

firstpart = firstpart.drop(['Unnamed: 29','Unnamed: 30','Unnamed: 31','Unnamed: 32','Unnamed: 33','Unnamed: 34'],1)
print firstpart.columns
#print firstpart.shape
#print secondpart.shape

merged=firstpart.join(secondpart)
merged=merged.replace("<td>&nbsp;</td>","")

#Turn categorial variables into ordinal ones for visualization
merged["Distance_num"]=np.nan
merged.ix[merged.Distance=="Sell the house; wife and kids","Distance_num"] = 1
merged.ix[merged.Distance=="Surf trip","Distance_num"] = 2
merged.ix[merged.Distance=="Week-end trip","Distance_num"] = 3
merged.ix[merged.Distance=="Day trip","Distance_num"] = 4
merged.ix[merged.Distance=="Take a car","Distance_num"] = 5
merged.ix[merged.Distance=="In the city","Distance_num"] = 6

merged["Wave quality_num"]=np.nan
merged.ix[merged["Wave quality"]=="Choss","Wave quality_num"] = 1
merged.ix[merged["Wave quality"]=="Sloppy","Wave quality_num"] = 2
merged.ix[merged["Wave quality"]=="Normal","Wave quality_num"] = 3
merged.ix[merged["Wave quality"]=="Regional Classic","Wave quality_num"] = 4
merged.ix[merged["Wave quality"]=="World Class","Wave quality_num"] = 5
merged.ix[merged["Wave quality"]=="Totally Epic","Wave quality_num"] = 6

merged["Experience_num"]=np.nan
merged.ix[merged.Experience=="Beginners wave","Experience_num"] = 1
merged.ix[merged.Experience=="All surfers","Experience_num"] = 2
merged.ix[merged.Experience=="Experienced surfers","Experience_num"] = 3
merged.ix[merged.Experience=="Pros or kamikaze only...","Experience_num"] = 4

merged["Frequency_num"]=np.nan
merged.ix[merged.Frequency=="Rarely break (5day/year)","Frequency_num"] = 1
merged.ix[merged.Frequency=="Sometimes break","Frequency_num"] = 2
merged.ix[merged.Frequency=="Regular","Frequency_num"] = 3
merged.ix[merged.Frequency=="Very consistent (150 day/year)","Frequency_num"] = 4

merged["Normal length_num"]=np.nan
merged.ix[merged["Normal length"]=="Short (&amp;lt; 50m)","Normal length_num"] = 1
merged.ix[merged["Normal length"]=="Normal (50 to 150m)","Normal length_num"] = 2
merged.ix[merged["Normal length"]=="Long (150 to 300 m)","Normal length_num"] = 3
merged.ix[merged["Normal length"]=="Very Long (300 to 500 m)","Normal length_num"] = 4

merged["Good day length_num"]=np.nan
merged.ix[merged["Good day length"]=="Short (&amp;lt; 50m)","Good day length_num"] = 1
merged.ix[merged["Good day length"]=="Normal (50 to 150m)","Good day length_num"] = 2
merged.ix[merged["Good day length"]=="Long (150 to 300 m)","Good day length_num"] = 3
merged.ix[merged["Good day length"]=="Very Long (300 to 500 m)","Good day length_num"] = 4
merged.ix[merged["Good day length"]=="Exceptional (&gt;500m)","Good day length_num"] = 5



#Filter out null values
merged = merged[np.isfinite(merged['Good day length_num'])]
merged = merged[np.isfinite(merged['Normal length_num'])]
merged = merged[np.isfinite(merged['Frequency_num'])]
merged = merged[np.isfinite(merged['Experience_num'])]
merged = merged[np.isfinite(merged['Wave quality_num'])]
merged = merged[np.isfinite(merged['Distance_num'])]

merged['Latitude'] = merged['Latitude'].astype(str)
merged['Longitude'] = merged['Longitude'].astype(str)
merged['TypicalSwell_MarApr'] = merged['TypicalSwell_MarApr'].astype(str)
merged = merged[merged.Longitude != "nan"]
merged = merged[merged.TypicalSwell_MarApr != "nan"]
merged = merged[merged.TypicalSwell_MarApr != ""]
merged = merged[merged.Latitude != "nan"]



merged.to_csv("K:/03. Academic/03. HKS/07. Year 2 Semester 2/03 - CS-171 - Data Visualization/Final project/spotlevel_withseason_filtered_ordinal.csv",index_label="Zone url")



#create ordinal values
#filter


#firstpart.ix[firstpart.Country =="Algeria","Key"] = "http://www.wannasurf.com/spot/"+firstpart["Continent"]+"/"+firstpart["Country"]+"/"+firstpart["Spot"]+"/index.html"
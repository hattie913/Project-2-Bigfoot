# -*- coding: utf-8 -*-
"""Locations&sightings.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pMRyFmZFG1eyIPBmHSo4xls86hevz7Ok
"""

!pip install geopandas

import pandas as pd
import geopandas 
import matplotlib.pyplot as plt

bigfoot_geo = pd.read_pickle('bigfoot_geo.pkl')
counties = pd.read_pickle('counties_clean.pkl')
bigfoot_geo.tail()

"""**Locations of Bigfoot:**


"""

county_labels = pd.read_pickle('/content/county_labels.pkl')
indexName = county_labels[county_labels.state.isin(['AK','HI','AS','GU','MP','PR','VI'])].index
continental_county_labels = county_labels.drop(index = indexName)

fig, ax = plt.subplots(figsize=(14, 14))
counties.plot(ax=ax, color =  "lightblue")
bigfoot_geo.plot(ax=ax, markersize= 6, marker='.', color = 'black')
plt.title("Locations of Bigfoot Sightings in the US", fontsize = 20)

plt.axis('off')

"""## **Bigfoot Sightings Per County**

"""

import numpy as np
from collections import Counter
import geopandas

county_labels = pd.read_pickle('/content/county_labels.pkl')
indexName = county_labels[county_labels.state.isin(['AK','HI','AS','GU','MP','PR','VI'])].index
continental_county_labels = county_labels.drop(index = indexName)

continental_county_labels.sort_values(by = ['fips'])

countyGeo = pd.merge(counties,continental_county_labels,left_on = 'GEOID',right_on = 'fips')
countyGeo.to_crs('EPSG:4326')

bigfoot_geo.rename(columns = {'FIPS':'fips'},inplace= True)
bigfoot_county= pd.merge(countyGeo,bigfoot_geo,on ='fips') 

bigfoot_county.sort_values(by = ['fips'])

dropcols = bigfoot_county.columns[0:9].insert(9,'number')

bigfoot_county.drop(columns= dropcols,inplace = True)  #3767 rows

sightCounts = bigfoot_county.groupby(by = ['fips']).size().reset_index(name = 'sightCounts')   
bigfoot_county  = pd.merge(bigfoot_county,sightCounts) #why after merge become not a geopandaDF?

columnNames = ['fips','county','state','state_name','sightCounts','geometry_x']
countyBF = bigfoot_county[columnNames]
countyBfGeo = geopandas.GeoDataFrame(countyBF, crs="EPSG:4326",geometry=countyBF.geometry_x).drop(columns = ['geometry_x'])
countyBfGeo.head()

countyBfGeo['plotcount'] = np.where(countyBfGeo.sightCounts>= 15, 15, countyBfGeo.sightCounts)
countyBfGeo.head()

moreSightings = countyBfGeo[countyBfGeo.sightCounts>=15]

moreSightingsCounty = pd.crosstab([moreSightings.state,moreSightings.county],columns = 'counts').sort_values(by = 'counts',ascending = False)
print(moreSightingsCounty)

fig, ax = plt.subplots(figsize=(18,18))
counties.plot(ax = ax, color='lightgrey', alpha=.8,edgecolor = 'white')
countyBfGeo.plot(ax = ax,column = 'plotcount',cmap = 'Blues',edgecolor = 'lightblue',legend=True,legend_kwds = {'shrink':.35,
                                                                                                                    'ticks':range(2,16,2)})                                                                                                      
cb = fig.axes[1]
cb.set_ylabel('Number of bigfoot Sightings',labelpad = 20,rotation = 270,fontsize = 16)
cb.tick_params(size = 8,labelsize =14)
plt.title("Bigfoot Sightings Per County in the US", fontsize = 20)
plt.axis('off')

top10seeings = pd.crosstab([countyBfGeo.county,countyBfGeo.fips, countyBfGeo.state],columns="counts").sort_values("counts", ascending=False)[:10]
print(top10seeings)
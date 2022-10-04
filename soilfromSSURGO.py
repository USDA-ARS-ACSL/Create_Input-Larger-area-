#This file used to generate the soil lyr.file From SSURGO
#Note: 
import numpy as np
import requests
import json
import xmltodict
import pandas as pd
import math

# Get soil profile from NRCS website
#lon = -80.33
#lat = 35.88
location = pd.read_csv('Location.csv')
#print(location)
for index, row in location.iterrows():
  point = (row['name'])
  lat = row['latitude']
  lon = row['longitude']

  lonLat = str(lon) + " " + str(lat)
  url="https://SDMDataAccess.nrcs.usda.gov/Tabular/SDMTabularService.asmx"
  headers = {'content-type': 'text/xml'}
  body = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sdm="http://SDMDataAccess.nrcs.usda.gov/Tabular/SDMTabularService.asmx">
            <soap:Header/>
            <soap:Body>
                <sdm:RunQuery>
                    <sdm:Query>SELECT co.cokey as cokey, ch.chkey as chkey, comppct_r as prcent, slope_r, slope_h as slope, hzname, hzdepb_r as depth, 
                               awc_r as awc, claytotal_r as clay, silttotal_r as silt, sandtotal_r as sand, om_r as OM, dbthirdbar_r as dbthirdbar, 
                               wthirdbar_r/100 as th33, (dbthirdbar_r-(wthirdbar_r/100)) as bd FROM sacatalog sc
                               FULL OUTER JOIN legend lg  ON sc.areasymbol=lg.areasymbol
                               FULL OUTER JOIN mapunit mu ON lg.lkey=mu.lkey
                               FULL OUTER JOIN component co ON mu.mukey=co.mukey
                               FULL OUTER JOIN chorizon ch ON co.cokey=ch.cokey
                               FULL OUTER JOIN chtexturegrp ctg ON ch.chkey=ctg.chkey
                               FULL OUTER JOIN chtexture ct ON ctg.chtgkey=ct.chtgkey
                               FULL OUTER JOIN copmgrp pmg ON co.cokey=pmg.cokey
                               FULL OUTER JOIN corestrictions rt ON co.cokey=rt.cokey
                               WHERE mu.mukey IN (SELECT * from SDA_Get_Mukey_from_intersection_with_WktWgs84('point(""" + lonLat + """)')) order by co.cokey, ch.chkey, prcent, depth
                    </sdm:Query>
                </sdm:RunQuery>
             </soap:Body>
             </soap:Envelope>"""

  response = requests.post(url,data=body,headers=headers)
          # Put query results in dictionary format
  my_dict = xmltodict.parse(response.content)
  #print(my_dict)
              


  #try:
  soil_df = pd.DataFrame.from_dict(my_dict['soap:Envelope']['soap:Body']['RunQueryResponse']['RunQueryResult']['diffgr:diffgram']['NewDataSet']['Table'])

  # Drop columns where all values are None or NaN
  soil_df = soil_df.dropna(axis=1, how='all')
  soil_df = soil_df[soil_df.chkey.notnull()]

  # Drop unecessary columns
  soil_df = soil_df.drop(['@diffgr:id', '@msdata:rowOrder', '@diffgr:hasChanges'], axis=1)

  # Drop duplicate rows
  soil_df = soil_df.drop_duplicates()

  # Convert prcent and depth column from object to float
  soil_df['prcent'] = soil_df['prcent'].astype(float)
  soil_df['depth'] = soil_df['depth'].astype(float)
  soil_df['Init'] = '\'m\''
  soil_df['no3'] = 25.0
  soil_df['nh4'] = 0.0
  soil_df['hnew'] = -200
  soil_df['tmpr'] = 25.0
  soil_df['th1500'] = -1
  soil_df['thr'] = -1
  soil_df['ths'] = -1
  soil_df['tha'] = -1
  soil_df['th'] = -1
  soil_df['Alfa'] = -1
  soil_df['n'] = -1
  soil_df['ks'] = -1
  soil_df['kk'] = -1
  soil_df['thk'] = -1

  soil_df['sand%'] = soil_df['sand'].astype(float)/100.0
  soil_df['silt%'] = soil_df['silt'].astype(float)/100.0
  soil_df['clay%'] = soil_df['clay'].astype(float)/100.0

  #set 3 decimal 
  soil_df['sand1'] = round(soil_df['sand%'], 3)
  soil_df['silt1'] = round(soil_df['silt%'], 3)
  soil_df['clay1'] = round(soil_df['clay%'], 3)
  soil_df['bd1'] = round(soil_df['bd'].astype(float), 3)
  #if soil_df['bd1'].values < 0.7:
     #soil_df['bd1'].values = 1.011

  soil_df['th33%'] = round(soil_df['th33'].astype(float), 3)
  #soil_df['clay1']=round(soil_df['clay%'], 2)
  #print(soil_df['clay1'])
  # Select rows with max prcent
  soil_df = soil_df[soil_df.prcent == soil_df.prcent.max()]

  # Sort rows by depth
  soil_df = soil_df.sort_values(by=['depth'])

  # Check for rows with NaN values
  soil_df_with_NaN = soil_df[soil_df.isnull().any(axis=1)]
  depth = ", ".join(soil_df_with_NaN["depth"].astype(str))
  if len(depth) > 0:
      #messageUser("Layers with the following depth " + depth + " were deleted.")
      soil_df = soil_df.dropna()
      
  if soil_df['bd1'].iloc[0] < 0.7:
      print(soil_df['depth'].iloc[0])
  if soil_df['clay1'].iloc[0] < 0.04:
      print(soil_df['depth'].iloc[0])
  if soil_df['silt1'].iloc[0] < 0.04:
      print(soil_df['depth'].iloc[0])   
  if soil_df['sand1'].iloc[0] < 0.04:
      print(soil_df['depth'].iloc[0]) 
      #soil_df = soil_df.dropna(axis=1, how='all')
      #soil_df = soil_df.dropna()
  #print(soil_df['depth'].iloc[0])
  newfile = open(point + '.lyr','w') 
  newfile.write('surface ratio    internal ratio: ratio of the distance between two neighboring nodes\n')
  newfile.write('1.6         0.05             2.100         2\n')
  newfile.write('Row Spacing\n')
  newfile.write('76\n')
  newfile.write('Planting Depth  X limit for roots      root weight per slab\n')
  newfile.write('10             23                           0.0275 \n')
  newfile.write('Boundary code for bottom layer (for all bottom nodes) 1 constant -2 seepage face\n')
  newfile.write('-2\n')
  newfile.write('Bottom depth Init Type  OM (%/100)  no3(ppm)   NH4  hNew  Tmpr  Sand   Silt    Clay     BD     TH33     TH1500  thr ths tha th  Alfa    n   Ks  Kk  thk\n')
  #soil_df[["depth", "clay"]]
  #print(soil_df)
  #print (soil_df[["depth", "clay","clay","clay","clay","clay","clay",]])
  newfile.close()
  print(point)
  soil_df[["depth", "Init", "OM", "no3", "nh4", "hnew", "tmpr", "sand1", "silt1", "clay1", "bd1", "th33%", "th1500", "thr", "ths", "tha", "th", "Alfa", "n", "ks", "kk", "thk"]].to_csv(point + '.lyr', header = False, mode = 'a', sep='\t', index=False)
#soil_df.to_csv('point.lyr', header = False, mode = 'a', sep='\t', index=False)
#print (soil_df.depth)




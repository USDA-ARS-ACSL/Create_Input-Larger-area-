# This file used to generate the 2dglycim input initial file 
import numpy as np
import pandas as pd

location = pd.read_csv('Location.csv')
#print(location)
for index, row in location.iterrows():
  point = (row['name'])
  lat = (row['latitude'])
  lon = (row['longitude'])
  sow = (row['sowing'])
  emergence = (row['emergence'])
  end = (row['end'])


  newfile = open(point + '.ini','w') 
  newfile.write('***Initialization data for location\n')
  newfile.write('POPROW  ROWSP  Plant Density      ROWANG  xSeed  ySeed         CEC    EOMult\n')
  newfile.write('26.3    76.0    20.0    0.0    0.0    195.0    0.55    0.5\n')
  newfile.write('Latitude longitude altitude\n')
  newfile.write(str(lat) + ' ' + str(lon) + '  200.0\n')
  newfile.write('AutoIrrigate\n')
  newfile.write('0.0\n')
  newfile.write('Sowing        Emergence      end        timestep\n')
  newfile.write(str(sow) + ' ' + str(emergence) + ' ' + str(end) + ' ' + '60\n')
  newfile.write('output soils data (g03, g04, g05 and g06 files) 1 if true\n')
  newfile.write('                      no soil files        output soil files\n')
  newfile.write('0                  1\n')

  newfile.close()
  print(point)
  
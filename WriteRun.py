#This file used to genenerate the 'run'file for 2dglycim
import numpy as np
import os,sys
import subprocess
import pandas as pd
#D:\GLYCIM-2DSOIL\FUTURE\RCP45\2091

base = "d:\\GLYCIM-2DSOIL\\FUTURE\\RCP45\\2091\\"


location = pd.read_csv('Location.csv')
#print(location)
for index, row in location.iterrows():
	point = (row['name'])

	d = str(point)
	pa = './'+ d +'/run.dat'
	if os.path.isfile(pa):
		os.remove(pa)
	with open(pa, 'a') as myfile:

		bd = base+d
		soi = point +'.soi'
		ini = point +'.ini'
		grd = point +'.grd'
		nod = point +'.nod'
		wea = point +'.wea'

		myfile.write(bd+f'\\{wea}'+'\n')
		myfile.write(bd+'\\time.tim\n')
		myfile.write(bd+'\\BiologyDefault.bio\n')
		myfile.write(bd+'\\climate.cli\n')
		myfile.write(bd+'\\nitro.nit\n')
		myfile.write(bd+'\\NitrogenDefault.sol\n')
		myfile.write(bd+f'\\{soi}'+'\n')
		myfile.write(bd+'\\Manage.man\n')
		myfile.write(bd+'\\Irri.drp\n')
		myfile.write(bd+'\\Water.DAT\n')
		myfile.write(bd+'\\WatMovParam.dat\n')
		myfile.write(bd+f'\\{ini}'+'\n')
		myfile.write(bd+'\\93B15.var\n')
		myfile.write(bd+f'\\{grd}'+'\n')
		myfile.write(bd+f'\\{nod}'+'\n')
		myfile.write(bd+'\\MassBI.dat\n')
		myfile.write(bd+'\\g01.g01\n')
		myfile.write(bd+'\\g02.g02\n')
		myfile.write(bd+'\\g03.G03\n')
		myfile.write(bd+'\\g04.G04\n')
		myfile.write(bd+'\\g05.G05\n')
		myfile.write(bd+'\\g06.G06\n')
		myfile.write(bd+'\\MassBI.out\n')
		myfile.write(bd+'\\runoffmassbl.txt\n')

		print(point)
	
_debug=True
# _debug=False

import os
from os import system as sh
from time import sleep as slp
import re

DFT='DEFAULT_FILE_NAME'
re_split=lambda s:r'[^\.]*'.join(['',]+list(s)+['$',])

def rename(name:str)->str:
	for s in ['rar','zip','7z']:
		if re.findall(re_split(s),name):
			return re.sub(re_split(s),s,name)
	return DFT

def mian(pth:str):
	for i in os.walk(pth):
		# if '0_' in i[0]:
		# 	continue
		for j in i[2]:
			j2=rename(j)
			if j2 not in [j,DFT]:
				od='move "'+os.path.join(i[0],j)+'" "'+os.path.join(i[0],j2)+'"'
				if _debug:
					print(od)
					open('1.sh','ab').write(od.encode(errors='backslashreplace')+b'\n')
				else:
					sh(od)


mian(r'G:\qwq')

_debug=True
_debug=False

import os
import re
from time import sleep as slp
import json
import base64


def logw(pth:str,s:str):
	return open(pth,'ab').write(s.encode(errors='backslashreplace')+b'\n')

sh_log=None
def sh(od:str,o_log:str=None)->int:
	od+=' 1>register_1.log 2>register_2.log'
	if not o_log:
		o_log=sh_log
	if o_log:
		logw(o_log,od)
	if _debug:
		print(od)
		input()
	return os.system(od)

def pwd(l:list,pth:str=None)->list:
	if not pth:
		pth=os.path.join(os.path.abspath(os.path.dirname(__file__)),'pwd.json')
	if isinstance(l,str):
		l=[l,]
	ans=['',]
	j=json.load(open(pth,'rb'))
	for i in l:
		ans+=j.get(str(i),list())
	return sorted(set(ans))

states=[b'',b'Data Error',b'CRC Failed',b'Unknown Error']
DONE='_0_decompressed'

re_split=lambda s:r'[^\.]*'.join(['',]+list(s)+['$',])
def getname(name:str)->str:
	for s in ['rar','zip','7z']:
		if re.findall(re_split(s),name):
			return re.sub(re_split(s),s,name)
	return DONE

def mian(pth:str,pwds:list):
	pth=os.path.abspath(pth)
	pth_recycle=os.path.join(pth,'0_decompress_recycle')
	len_pth=len(pth)+1

	if not os.path.exists(pth_recycle):
		sh('mkdir "'+pth_recycle+'"')

	_log=os.path.join(pth_recycle,'0_decompress_logs')
	log_sh=_log+'.sh'
	log_csv=_log+'.csv'
	log_if=_log+'.if'
	log_wp=_log+'.wp'

	if not isinstance(pwds,(list,tuple,set)):
		pwds=[pwds,]
	pwds=[(str(i),'_='+base64.b64encode(str(i).encode()).decode().replace('/','_')) for i in pwds]

	for l3 in os.walk(pth):
		for i in l3[2]:
			j=getname(i)
			if j in [i,DONE]:
				continue
			od='move "'+os.path.join(l3[0],i)+'" "'+os.path.join(l3[0],j)+'"'
			sh(od)

		if '0_' in l3[0]:
			continue

		for i in l3[2]:
			if re.findall(r'^[\s\S]+\.part[0-9]+\.rar$',i):
				if '.part1.rar' not in i:
					continue
			if re.findall(r'^[\s\S]+\.7z\.[0-9]{3}$',i):
				if '.7z.001' not in i:
					continue
			if re.findall(r'^[\s\S]+\.zip\.[0-9]{3}$',i):
				if '.zip.001' not in i:
					continue

			pth_file=os.path.join(l3[0],i)
			name_dir=pth_file[len_pth:].replace('/','_').replace('\\','_')
			pth_t=os.path.join(pth,name_dir+DONE)
			if os.path.exists(pth_t):
				print('"'+i+'" had been decompressed!')
				continue

			flg=False
			for j in pwds:
				od='7z x "'+pth_file+'" -p'+j[0]+' -y -o"'+pth_t+'"'
				state=sh(od)
				if state:
					err=open('register_2.log','r').read()
					if 'ERROR: Wrong password :' in err:
						state=9
					elif 'Can not open encrypted archive.' in err:
						flg=True
						print('File "'+i+'" is incomplete...')
						logw(log_csv,pth_file+',,Incomplete File')
						logw(log_if,pth_file)
						break
					elif 'ERROR: Data Error in encrypted file. Wrong password? :' in err:
						state=1
					elif 'ERROR: CRC Failed in encrypted file. Wrong password? :' in err:
						state=2
					elif 'ERROR: CRC Failed :' in err:
						state=2
					else:
						state=3

				if _debug:
					print('state',state)
					
				if state>7:
					print('Try to decompress "'+i+'" with password "'+j[0]+'", but WRONG.')
					pth_f=os.path.join(pth_recycle,name_dir+j[1])
					od='move "'+pth_t+'" "'+pth_f+'"'
					sh(od)
				else:
					flg=True
					print('Successfully decompressed "'+i+'" with password "'+j[0]+'"!')
					if state:
						print('But it has '+states[state].decode()+'...')
					logw(log_csv,pth_file+','+j[0]+','+states[state])
					logw(_log+'.'+j[1],pth_file)
					break
			if not flg:
				logw(log_csv,pth_file+',,Wrong Password')
				logw(log_wp,pth_file)
				print('Do you know the password of "'+i+'"?')
			print()

mian(r'G:\vmback_baidu',pwd('美少女黑洞+'))

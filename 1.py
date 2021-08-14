_debug=True
_debug=False

import os
from os import system as sh
from time import sleep as slp
import base64

enc=lambda x:'===='+base64.b64encode(str(x).encode()).decode().replace('/','_')
states=[b'',b'Data Error',b'CRC Failed',b'Unknown Error']

def mian(pth:str,pwds:list,pth_log:str=None):
	pth=os.path.abspath(pth)
	pth_recycle=os.path.join(pth,'000_decompressed_recycle')
	if not os.path.exists(pth_recycle):
		sh('mkdir "'+pth_recycle+'"')

	if not pth_log:
		pth_log=os.path.join(pth_recycle,os.path.basename(pth)+'.csv')

	if not isinstance(pwds,(list,tuple,set)):
		pwds=[pwds,]
	
	pwds=[(str(i),enc(i)) for i in pwds]

	for i in os.walk(pth):
		k=i[2]
		break
	for i in k:
		if re.findall(r'^[\s\S]+\.part[0-9]+\.rar$',i):
			if '.part1.rar' not in i:
				continue
		if re.findall(r'^[\s\S]+\.7z\.[0-9]{3}$',i):
			if '.7z.001' not in i:
				continue
		if re.findall(r'^[\s\S]+\.zip\.[0-9]{3}$',i):
			if '.zip.001' not in i:
				continue
		pth_file=os.path.join(pth,i)
		name_dir=os.path.splitext(i)[0]+'_decompressed'
		pth_dir=os.path.join(pth,name_dir)
		b_pth_file=pth_file.encode(errors='backslashreplace')
		if os.path.exists(pth_dir):
			print('"'+name_dir+'" already exists!')
			continue

		flg=False
		for j in pwds:
			od='7z x "'+pth_file+'" -p'+j[0]+' -y -o"'+pth_dir+'" 1>register_1.log 2>register_2.log'
			if _debug:
				# od='7z x "'+pth_file+'" -p'+j[0]+' -y -o"'+pth_dir+'"'
				print(od)
				input()

			state=sh(od)
			if state:
				err=open('register_2.log','r').read()
				if 'ERROR: Wrong password :' in err:
					state=9
				elif 'Can not open encrypted archive.' in err:
					flg=True
					print('File "'+i+'" is incomplete...')
					open(pth_log,'ab').write(b_pth_file+b',,Incomplete File\n')
					open(pth_log+'.if','ab').write(b_pth_file+b'\n')
					break
				elif 'ERROR: Data Error in encrypted file. Wrong password? :' in err:
					state=1
				elif 'ERROR: CRC Failed in encrypted file. Wrong password? :' in err:
					state=2
				else:
					state=3

			if _debug:
				print('state',state)
				
			if state>7:
				print('Try to decompress "'+i+'" with password "'+j[0]+'", but WRONG.')
				name_wa=os.path.splitext(i)[0]+'_'+j[1]
				pth_wa=os.path.join(pth_recycle,name_wa)
				od='move "'+pth_dir+'" "'+pth_wa+'" 1>register_1.log 2>register_2.log'
				if _debug:
					od='move "'+pth_dir+'" "'+pth_wa+'"'
					print(od)
					input()
				sh(od)
			else:
				flg=True
				print('Successfully decompressed "'+i+'" with password "'+j[0]+'"!')
				if state:
					print('But it has '+states[state].decode()+'...')
				open(pth_log,'ab').write(b_pth_file+b','+j[0].encode(errors='backslashreplace')+b','+states[state]+b'\n')
				open(pth_log+'.'+j[1],'ab').write(b_pth_file+b'\n')
				break
		if not flg:
			open(pth_log,'ab').write(b_pth_file+b',,Wrong Password\n')
			open(pth_log+'.wp','ab').write(b_pth_file+b'\n')
			print('Do you know the password of "'+i+'"?')
		print()
		
mian(r'G:\qwq',['password1','password2',''])

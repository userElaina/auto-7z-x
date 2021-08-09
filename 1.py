import os
from os import system as sh
from time import sleep as slp
import base64

enc=lambda x:'_'+base64.b64encode(str(x).encode()).decode().replace('/','')

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
			if sh(od):
				print('Try to decompress "'+i+'" with password "'+j[0]+'", but WRONG.')
				name_wa=os.path.splitext(i)[0]+'_'+j[1]
				pth_wa=os.path.join(pth_recycle,name_wa)
				od='move "'+pth_dir+'" "'+pth_wa+'" 1>register_1.log 2>register_2.log'
				sh(od)
			else:
				flg=True
				print('Successfully decompressed "'+i+'" with password "'+j[0]+'"!')
				open(pth_log,'ab').write(b_pth_file+b','+j[0].encode(errors='backslashreplace')+b'\n')
				open(pth_log+'.'+j[1],'ab').write(b_pth_file+b'\n')
				break
		if not flg:
			open(pth_log,'ab').write(b_pth_file+b',Wrong Password (salt:userElaina)\n')
			open(pth_log+'.err','ab').write(b_pth_file+b'\n')
			print('Do you know the password of "'+i+'"?')

mian(r'G:\qwq',['password1','password2',''])

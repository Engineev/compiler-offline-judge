#Code by TimerChen 
#Last Update: 5.29
last_test_log = 'http://blacko.cn:6002/Compiler/build/2161'


import urllib3
import re
import os
val2 =  os.system('rm testcase_*.txt')
http = urllib3.PoolManager()
r = http.request('GET', last_test_log)
str = r.data.decode("UTF-8")
rgx = re.compile(r'/Compiler/download/(testcase_[0-9]{3}.txt)')
l = rgx.findall(str)
#print(l)
for i in l:
	print("file "+i+" downloading...")
	r = http.request('GET', 'http://blacko.cn:6002/Compiler/download/'+i)
	str = r.data.decode("UTF-8")
	with open(i,'wb') as f:  
		f.write(r.data)

import os, numpy as np

def happycap(adb_shell_cmd_head='adb shell '):
	os.system(adb_shell_cmd_head + "screencap -p > curr.png")
	with open('curr.png', 'rb')  as f:
		con = f.read()
	con = con.replace(b'\r\r\n', b'\n')
	with open('curr.png', 'wb') as f:
		f.write(con)
		
def getimagesum(a1,a2):
	v1 = np.array(a1)*1.-np.array(a2)*1.
	dx = np.sum(v1**2, axis=2)**0.5
	co = np.sum(dx)/dx.size
	return co
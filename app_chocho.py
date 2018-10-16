# 932,454  -- 721,137	grid=4x3

import numpy as np
import time, winsound, os, sys
from PIL import Image

os.chdir("G:/")
from classInbattle1111 import *
from classAdbAssist import *
# emudpi = 1200x675
#from classInbattle import *

signal_declare = [
	's01.png,549-280-634-366,select_region,swipe 600 300 900 300',
	's02.png,367-189-465-285,icon_party,tap 500 78',
	's022.png,615-599-907-636,icon_request,request_select',
	's04.png,43-95-177-146,select_assist,tap 354 210',
	's700stopped.png,656-345-754-414,quitted,tap 584 401',
	's701title.png,656-345-754-414,title,tap 584 401',
	's702desk.png,656-345-754-414,desktop,shellstart',
	's05.png,154-24-324-92,confirm_team,tap 249 53',
	's10.png,505-614-702-627,result_confirm,tap 300 300',
	's06.png,392-16-578-110,in_battle,this_is_complex',
	's099.png,1021-605-1145-631,confirm_harvest,tap 1100 615',
	's011.png,555-287-625-360,select_region,swipe 600 300 900 300',
	's0222.png,460-291-548-370,icon_party,tap 460 291',
	's703continue.png,488-387-695-435,sc_continue,tap 643 411',
	's704getstone.png,536-506-662-558,getstone,tap 500 300',
	]

imgPriorPower = 0
imgNonCharacter = 0

os.chdir("G:/")
preloaded = {}
for signal_inst in signal_declare:
	print(signal_inst.split(','))
	fname, crops, tip, runfunc = signal_inst.split(',')
	preloaded[fname] = Image.open(fname)
	
adb_shell_cmd_head = 'adb shell '
xcmd_start_housamo = adb_shell_cmd_head +'am start '+ \
	'jp.co.lifewonders.housamo/com.google'+ \
	'.firebase.MessagingUnityPlayerActivity'

xcc = [x for x in sys.argv if 'port=' in x]
if xcc:
	xcc = xcc[0].replace('port=','')
else:
	os.system('adb devices')
	xcc = input("modify adb pointer?>")
if xcc:
	adb_shell_cmd_head = \
		adb_shell_cmd_head.replace('adb', 'adb -s 127.0.0.1:%s'%xcc)
	print('defined::', adb_shell_cmd_head)
xcc = xcc if xcc else '0'

os.system("mkdir device"+xcc)
os.chdir("device"+xcc)
controller_dir = "G:/"

def dzoomfunc(rf):
	rf = rf.split(' ')
	if len(rf)==5:
		x,y,a,b = list(map(int,rf[1:]))
		x,y = dzoom(x,y)
		a,b = dzoom(a,b)
		return rf[0]+' '+'%d %d %d %d'%(x,y,a,b)
	else:
		x,y = list(map(int,rf[1:]))
		x,y = dzoom(x,y)
		return rf[0]+' '+'%d %d'%(x,y)
		
class adbman:
	relist = []
	@staticmethod
	def send_adb_message(xcmd):
		adbman.relist.append(xcmd)
		print(xcmd)
		os.system(xcmd)
	@staticmethod
	def tick():
		adbman.relist.append('tick')
		adbman.checkErr()
	@staticmethod
	def checkErr():
		#adbman.relist[:-10]
		adbman.relist = adbman.relist[-10:]
		rff = adbman.relist
		rf = [x for x in adbman.relist if x!='tick']
		if len(rf)>4:
			if rf[0]==rf[1] and \
				rf[1]==rf[2] and \
				rf[2]==rf[3]:
				print('\n____RFF NO REFRESH\n')
				for i in range(4):
					winsound.Beep(1999+(i%2)*400,99)
			if rff[0]==rff[1] and\
				rff[1]==rff[2] and \
				rff[2]==rff[3]:
				print('\n____RFF TICK ONLY\n')
				for i in range(4):
					winsound.Beep(2999+(i%2)*400,99)
	
send_adb_message = adbman.send_adb_message
		
while 1:
	print('step into')
	controller_list = os.listdir(controller_dir)
	nextsleep = 5
	happycap()
	adbman.tick()
	imgstart = Image.open('curr.png')
	imgstart = imgstart.resize((1200,675))
	for signal_inst in signal_declare:
		fname, crops, tip, runfunc = signal_inst.split(',')
		crops = list(map(int, crops.split('-')))
		imgcropped = imgstart.crop(crops)
		imgcropped_1 = preloaded[fname].crop(crops)
		co = getimagesum(imgcropped, imgcropped_1)
		print('   ', '%4d'%int(co), tip)
		if co < 66:
			if 'select_region' in tip:
				os.system('del curr_state.png')
				os.system('rename curr.png curr_state.png')
			print('    sure =', tip)
			if 'tap' in runfunc or 'swipe' in runfunc:
				runfunc = dzoomfunc(runfunc)
				xcmd = adb_shell_cmd_head + 'input '+runfunc
				send_adb_message(xcmd)
			elif 'shellstart' in runfunc:
				send_adb_message(xcmd_start_housamo)
			elif 'request_select' in runfunc:
				runfunc = [x for x in controller_list
						if 'on_request_' in x]
				runfunc = runfunc[int(time.time()%len(runfunc))]
				runfunc = runfunc.replace('on_request_', '')
				print(runfunc)
				xcmd = adb_shell_cmd_head +'input '+dzoomfunc(runfunc)
				send_adb_message(xcmd)
			else:
				# --- in_battle ---
				#winsound.Beep(999,999)
				xcmd = onbattleop.inbattle_operation(imgstart, adb_shell_cmd_head)
				if xcmd: send_adb_message(xcmd)
				nextsleep = 5
	time.sleep(nextsleep)

	
# def getimagesum(img00, img11):
	# var1 = np.array(img00)-np.array(img11)
	# var1 = np.sum(np.abs(var1))/var1.size
	# return var1

import numpy as np, os, winsound, time
from PIL import Image

class onbattleop:
	@staticmethod
	def getimagesum(a1,a2):
		v1 = np.array(a1)*1.-np.array(a2)*1.
		dx = np.sum(v1**2, axis=2)**0.5
		co = np.sum(dx)/dx.size
		return co
	@staticmethod
	def preload_prior(imgTag='prior'):
		files = [x for x in os.listdir('.') if 's_'+imgTag in x]
		preloads = []
		for x in files:
			pre = Image.open(x)
			preloads.append(pre)
		return preloads
	@staticmethod
	def getrealposition(x,y):
		return gridx0+gridxxsc*x, gridy0+gridyysc*y
	@staticmethod
	def dzoom(x,y):
		return int(x/1200*1024), int(y/675*576)
	@staticmethod
	def set_movement(pos1, pos2, adb_shell_cmd_head):
		pos2 = (pos2[0], max(2.3, pos2[1]))
		x1,y1 = getrealposition(*pos1)
		x2,y2 = getrealposition(*pos2)
		x1,y1 = dzoom(x1,y1)
		x2,y2 = dzoom(x2,y2)
		x2+=10
		print('swipe', pos1, pos2)
		xcmd = adb_shell_cmd_head + 'input swipe %d %d %d %d 100'%(x1,y1,x2,y2)
		return xcmd
	@staticmethod
	def get12images(imgstart):
		gridimage12 = {}
		for y in range(4):
			for x in range(3):
				xx, yy = getrealposition(x,y)
				gridimage12[(x,y)] = imgstart.crop((xx-20,yy-20,xx+20,yy+20))
		return gridimage12
	@staticmethod
	def panduan_FindCategoryInst(categoryList, grid12):
		titanplaces = []
		for titanimg in categoryList:
			for y in range(4):
				for x in range(3):
					dsum = getimagesum(grid12[(x,y)], titanimg)
					if dsum<60:
						titanplaces.append((x,y))
		return titanplaces
	@staticmethod
	def inbattle_operation(imgstart, adb_shell_cmd_head):
		cropper = {}
		havecharacter = []
		grid12 = get12images(imgstart)
		if 'cmdcap' in os.listdir('.'):
			for x in grid12.keys():
				grid12[x].save('_battle_%d_%d.png'%x)
			os.system('rename curr.png _battle0.png')
			os.system('del cmdcap')
		haveprior = panduan_FindCategoryInst(priors, grid12)
		havetitan = panduan_FindCategoryInst(titans, grid12)
		haveblank = panduan_FindCategoryInst(blankenemy, grid12)
		haveblankT = panduan_FindCategoryInst(blankteam, grid12)
		print()
		print('prior::', haveprior)
		print('titan::', havetitan)
		print('blank::', haveblank)
		print('blankT::', haveblankT)
		mov_target = []
		if len(haveprior)>0:
			mov_start = haveprior[0]
		else:
			print('\n%s\n'%"warning: no prior found")
			for i in range(4): winsound.Beep(4999,59)
			bangs = [(x,y) for y in [3,2] for x in [0,1,2]]
			bangfan = [x for x in bangs if x not in haveblank+haveblankT]
			print('bangfan =', bangfan)
			mov_start = bangfan[int(time.time())%len(bangfan)]
			
		if len(havetitan)>0:
			pos_titan = havetitan[0]
			mov_target = pos_titan
		else:
			bulls = [(x,y) for y in range(2) for x in range(3)]
			bullfan = [x for x in bulls if x not in haveblank+haveblankT]
			print('bullfan =', bullfan)
			if bullfan:
				bullfan.sort(key=lambda pp: (pp[0]-mov_start[0])**2+
											(pp[1]-mov_start[1])**2)
				mov_target = bullfan[0]
			else:
				print('\n%s\n'%"warning no bullplace")
				for i in range(4): winsound.Beep(999,59)
		
		if mov_start and mov_target:
			return set_movement(mov_start, mov_target, adb_shell_cmd_head)
		else:
			return 0

getimagesum = onbattleop.getimagesum
preload_prior = onbattleop.preload_prior
getrealposition = onbattleop.getrealposition
dzoom = onbattleop.dzoom
set_movement = onbattleop.set_movement
get12images = onbattleop.get12images
panduan_FindCategoryInst = onbattleop.panduan_FindCategoryInst

priors = preload_prior('prior')
titans = preload_prior('titan')
blankenemy = [Image.open("s_blank.png")]
blankteam = [Image.open("s_blankT.png")]

gridxxsc = (932-721)/2
gridyysc = (454-137)/3
gridx0 = 721+gridxxsc/2
gridy0 = 137+gridyysc/2
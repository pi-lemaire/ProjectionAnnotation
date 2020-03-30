import numpy as np
import math
import cv2

#from tkinter import filedialog
#from tkinter import *

from tkinter import *
from tkinter import filedialog

import json

import sys


# this script is made for generating a simple interface for computing the homography from an image (to the left)
# to match the position of another image (to the right)



class OrthoRectificationAnnotate:



#global listPointsRectify   # pixel coordinates of points on the left image
#global listPointsOrtho  


#global selectedPoint # In case of editiing the position of a point.
					 # Positive is to the left, negative is to the right part of the image.
					 # Index starts with 1, 0 means none in selected

#global resultImg, rectifyImg, rectifyAnnotImg, orthoImg, orthoAnnotImg

#global lastDeletedPos, defaultDeletedPos


#global resultOrthoMat


#global RectifMethod

#global hsW, hsH 	#sizes of the half-size image that we will use for display

#global perspImgFilename, orthoImgFilename


	def __init__(self):
		# set of Parameters
		self.ParamSelectionDistance = 6.0
		self.ParamDeleteSecurityDist = 3.0
		self.ParamPointsOutsideWidth = 3
		self.ParamPointsInsideWidth = 1

		self.ParamDefaultRectifMethod = "None"


		# initialization stuff

		self.listPointsRectify = []
		self.listPointsOrtho = []
		self.selectedPoint = 0
		self.defaultDeletedPos = np.array((-10,-10))
		self.lastDeletedPos = self.defaultDeletedPos
		self.lastDeletedMap = ''

		self.RectifMethod = self.ParamDefaultRectifMethod

		#self.root = Tk()

		print('plop initialization')



	def drawMap(self):
		# Do the redrawing pretty much all the time when there's a mouse action

		#global rectifyAnnotImg, orthoAnnotImg
		#img = np.zeros((512,512,3), np.uint8)
		self.rectifyAnnotImg = self.rectifyImg.copy()
		self.orthoAnnotImg = self.orthoImg.copy()

		for i in range(0,len(self.listPointsRectify)):
			pair = self.listPointsRectify[i]
			colorOutside = (255,0,0)
			colorInside = (255,255,255)
			# pick a different color when selected
			if i == self.selectedPoint-1:
				colorInside = (255,128,0)
				colorOutside = (255,255,255)
			cv2.circle(self.rectifyAnnotImg,pair,self.ParamPointsOutsideWidth,colorOutside,-1)
			cv2.circle(self.rectifyAnnotImg,pair,self.ParamPointsInsideWidth,colorInside,-1)
			cv2.putText(self.rectifyAnnotImg,chr(ord('A')+i), (pair[0]+self.ParamPointsOutsideWidth, pair[1]-self.ParamPointsOutsideWidth), cv2.FONT_HERSHEY_PLAIN, 1, colorOutside)

		for i in range(0,len(self.listPointsOrtho)):
			pair = self.listPointsOrtho[i]
			colorOutside = (255,0,0)
			colorInside = (255,255,255)
			# pick a different color when selected
			if i == -self.selectedPoint-1:
				colorInside = (255,128,0)
				colorOutside = (255,255,255)
			cv2.circle(self.orthoAnnotImg,pair,self.ParamPointsOutsideWidth,colorOutside,-1)
			cv2.circle(self.orthoAnnotImg,pair,self.ParamPointsInsideWidth,colorInside,-1)
			cv2.putText(self.orthoAnnotImg,chr(ord('A')+i), (pair[0]+self.ParamPointsOutsideWidth, pair[1]-self.ParamPointsOutsideWidth), cv2.FONT_HERSHEY_PLAIN, 1, colorOutside)

		self.generateResultImg()



	def findClosest(self, listExistingPts, testedCoords):
		coords = np.array(testedCoords)
		minDist=999999.	# infinite distance
		bestIndex = -1
		for i in range(0,len(listExistingPts)):
			pair = np.array(listExistingPts[i])
			currDist= np.linalg.norm(pair-testedCoords)
			if currDist<minDist:
				bestIndex = i
				minDist = currDist

		return bestIndex, minDist




	def generateResultImg(self):

		#global resultImg, orthoImg, hsW, hsH
		#global resultOrthoMat

		h, w, c = self.orthoImg.shape

		if len(self.listPointsOrtho)>=4 and len(self.listPointsRectify)>=4 :
			#print('bla')
			minLength = len(self.listPointsOrtho)
			if len(self.listPointsRectify)<minLength:
				minLength = len(self.listPointsRectify)

			lpr = np.array(self.listPointsRectify[0:minLength])
			lpo = np.array(self.listPointsOrtho[0:minLength])

			if self.RectifMethod == "Ransac":
				self.resultOrthoMat, status = cv2.findHomography(lpr, lpo, method=cv2.RANSAC)
			elif self.RectifMethod == "Lmeds":
				self.resultOrthoMat, status = cv2.findHomography(lpr, lpo, method=cv2.LMEDS)
			elif self.RectifMethod == "Rho":
				self.resultOrthoMat, status = cv2.findHomography(lpr, lpo, method=cv2.RHO)
			elif self.RectifMethod == "None":
				self.resultOrthoMat, status = cv2.findHomography(lpr, lpo, method=0)
			

			print(self.resultOrthoMat)

			imRectified = cv2.warpPerspective(self.rectifyImg, self.resultOrthoMat, (self.hsW*2,self.hsH*2))

			self.resultImg[:,0:self.hsW,:] = cv2.resize(imRectified, (0,0), fx=0.5, fy=0.5)


		else:
			self.resultImg[:,0:self.hsW,:] = np.zeros((self.hsH, self.hsW, c), np.uint8)






	def AnnotateImgToRectify(self,event,x,y,flags,param):
		self.AnnotateImg(event,x,y,flags,param,'rectify')

	def AnnotateImgOrtho(self,event,x,y,flags,param):
		self.AnnotateImg(event,x,y,flags,param,'ortho')




	def AnnotateImg(self,event,x,y,flags,param,whichMap):
		#global mouseX, mouseY
		#global listPointsOrtho, listPointsRectify
		#global selectedPoint
		#global lastDeletedPos, defaultDeletedPos, lastDeletedMap

		doRedraw = False

		if event == cv2.EVENT_LBUTTONDOWN:
			# with the button pressed, we can move a previously annotated button
			#print("event button down")

			if self.lastDeletedMap!=whichMap or np.linalg.norm(self.lastDeletedPos-np.array((x,y)))>self.ParamDeleteSecurityDist:
				# reset the delete security stuff
				self.lastDeletedPos = self.defaultDeletedPos
				self.lastDeletedMap = ''

			# check if we have selected some point
			if whichMap=='rectify':
				idx, dist = self.findClosest(self.listPointsRectify, (x,y))

				if dist<self.ParamSelectionDistance:
					#set a point to selected
					self.selectedPoint = idx+1
					#print("selected point " + str(idx))
					doRedraw = True
			elif whichMap=='ortho':
				idx, dist = self.findClosest(self.listPointsOrtho, (x,y))

				if dist<self.ParamSelectionDistance:
					#set a point to selected
					self.selectedPoint = -idx-1
					#print("selected point " + str(idx))
					doRedraw = True


		if event == cv2.EVENT_LBUTTONDBLCLK:
			#print("event dbl click")
			doRedraw = True
			# double clicking close to a previously annotated point deletes it
			# check if we have selected some point

			if whichMap=='rectify':
				idx, dist = self.findClosest(self.listPointsRectify, (x,y))
				#print("found dist : " + str(dist) + " at index " + str(idx))

				if dist<self.ParamSelectionDistance:
					#set a point to selected
					del self.listPointsRectify[idx]
					#print("deleted point at index " + str(idx))
					self.lastDeletedPos = np.array((x,y))	# unfortunately, double clicking also throws a buttonUp event. We had to handle this a dummy way
					self.lastDeletedMap = whichMap
					self.selectedPoint = 0

					if len(self.listPointsOrtho)>idx:
						# assume the point that we just deleted was matched to a point to the corresponding map
						# lengths make it possible
						del self.listPointsOrtho[idx]

			if whichMap=='ortho':
				idx, dist = self.findClosest(self.listPointsOrtho, (x,y))
				#print("found dist : " + str(dist) + " at index " + str(idx))

				if dist<self.ParamSelectionDistance:
					#set a point to selected
					del self.listPointsOrtho[idx]
					#print("deleted point at index " + str(idx))
					self.lastDeletedPos = np.array((x,y))	# unfortunately, double clicking also throws a buttonUp event. We had to handle this a dummy way
					self.lastDeletedMap = whichMap
					self.selectedPoint = 0

					if len(self.listPointsRectify)>idx:
						# assume the point that we just deleted was matched to a point to the corresponding map
						# lengths make it possible
						del self.listPointsRectify[idx]



		if event==cv2.EVENT_LBUTTONUP:
			#print("event button up")

			#cv2.circle(img,(x,y),5,(255,0,0),-1)
			#mouseX,mouseY = x,y

			if whichMap!=self.lastDeletedMap or np.linalg.norm(self.lastDeletedPos-np.array((x,y)))>self.ParamDeleteSecurityDist:
				doRedraw = True

				if whichMap=='rectify':

					# we passed the security distance
					if self.selectedPoint==0:
						self.listPointsRectify.append((x,y))
						#print("created point at index " + str(len(listPointsLeft)-1))

					elif self.selectedPoint>0:
						self.listPointsRectify[self.selectedPoint-1] = (x,y)
						#print("modified point position at index " + str(selectedPoint-1))
						self.selectedPoint = 0

				elif whichMap=='ortho':

					# we passed the security distance
					if self.selectedPoint==0:
						self.listPointsOrtho.append((x,y))
						#print("created point at index " + str(len(listPointsLeft)-1))

					elif self.selectedPoint<0:
						self.listPointsOrtho[-self.selectedPoint-1] = (x,y)
						#print("modified point position at index " + str(selectedPoint-1))
						self.selectedPoint = 0

		if doRedraw:
			self.drawMap()





	def saveResults(self):
		print("saving procedure")

		saveFilename = filedialog.asksaveasfilename(initialdir = "/", title = "Select file", filetypes = (("json files","*.json"),("all files","*.*")))
		#saveFilename = '/Users/pierrelemaire/Documents/stationair/apps/code snippets/python homography calculator/test.json'


		print(saveFilename)

		RectifyData = { 'OrthoMat': self.resultOrthoMat.tolist(),
						'ImgFileToRectify' : self.perspImgFilename,
						'ImgFileToOrtho' : self.orthoImgFilename,
						'CoordsPtsToRectify' : self.listPointsRectify,
						'CoordsPtsOrtho' : self.listPointsOrtho }

		print(RectifyData)

		with open(saveFilename, 'w', encoding='utf-8') as f:
			json.dump(RectifyData, f, indent=4)



	def loadNewImageFiles(self):

		#global perspImgFilename, rectifyImg, orthoImgFilename, orthoImg, hsH, hsW, resultImg, listPointsRectify, listPointsOrtho

		del self.listPointsRectify[:]
		del self.listPointsOrtho[:]

		self.perspImgFilename = filedialog.askopenfilename(initialdir = "/",title = "Select the image file to rectify", filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
		#self.perspImgFilename = '/Users/pierrelemaire/Documents/stationair/apps/code snippets/python homography calculator/persp_img.jpg'
		print (self.perspImgFilename)

		self.rectifyImg = cv2.imread(self.perspImgFilename, flags=cv2.IMREAD_COLOR)


		self.orthoImgFilename = filedialog.askopenfilename(initialdir = "/",title = "Select the ortho image file", filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
		#self.orthoImgFilename = '/Users/pierrelemaire/Documents/stationair/apps/code snippets/python homography calculator/ortho_img.jpg'
		print(self.orthoImgFilename)

		self.orthoImg = cv2.imread(self.orthoImgFilename, flags=cv2.IMREAD_COLOR)

		#print(orthoImg.shape)
		h, w, c = self.orthoImg.shape

		#resultImg = np.zeros((h//2, w, c), np.uint8)
		#print(resultImg.shape)

		# result view initialization
		halfSizeImg = cv2.resize(self.orthoImg, (0,0), fx=0.5, fy=0.5)
		self.hsH, self.hsW, c = halfSizeImg.shape

		self.resultImg = np.zeros((self.hsH, self.hsW*2, c), np.uint8)
		self.resultImg[:,self.hsW:self.hsW*2,:] = halfSizeImg

		self.drawMap()





	def loop(self):
		cv2.namedWindow('ToRectify')
		cv2.setMouseCallback('ToRectify',self.AnnotateImgToRectify)

		cv2.namedWindow('OrthoImg')
		cv2.setMouseCallback('OrthoImg',self.AnnotateImgOrtho)

		while(1):
			cv2.imshow('ToRectify',self.rectifyAnnotImg)
			cv2.imshow('OrthoImg',self.orthoAnnotImg)
			cv2.imshow('Result', self.resultImg)

			k = cv2.waitKey(20) & 0xFF
			if k == 27:
				break
			elif k == ord('r'):
				self.RectifMethod = "Ransac"
				print("Robust method switched to RANSAC")
				self.generateResultImg()
			elif k == ord('l'):
				self.RectifMethod = "Lmeds"
				print("Robust method switched to LMEDS")
				self.generateResultImg()
			elif k == ord('p'):
				self.RectifMethod = "Rho"
				print("Robust method switched to RHO")
				self.generateResultImg()
			elif k == ord('0'):
				self.RectifMethod = "None"
				print("Robust method switched to None (all points taken into account equally)")
				self.generateResultImg()
			elif k == ord('s'):
				self.saveResults()
			elif k == ord('n'):
				self.loadNewImageFiles()







if __name__ == '__main__':
	oa = OrthoRectificationAnnotate()
	oa.loadNewImageFiles()
	oa.loop()

	#saveFilename = filedialog.asksaveasfilename(initialdir = "/", title = "Select file", filetypes = (("json files","*.json"),("all files","*.*")))
	#print(saveFilename)

#rectifyAnnotImg = rectifyImg.copy()
#orthoAnnotImg = orthoImg.copy()






#loadNewImageFiles()

#root = Tk()
#perspImgFilename =  filedialog.askopenfilename(initialdir = "/",title = "Select the image file to rectify", filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
#print (perspImgFilename)

#rectifyImg = cv2.imread(perspImgFilename, flags=cv2.IMREAD_COLOR)


#orthoImgFilename =  filedialog.askopenfilename(initialdir = "/",title = "Select the ortho image file", filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
#print(orthoImgFilename)

#orthoImg = cv2.imread(orthoImgFilename, flags=cv2.IMREAD_COLOR)







import os
import string
import shutil
import numpy as np
import GaitData as gd

jointDescriptors = ['Head', 'Shoulder-Center', 'Shoulder-Right', 'Shoulder-Left', 'Elbow-Right', 'Elbow-Left', 'Wrist-Right', 'Wrist-Left',
			   'Hand-Right', 'Hand-Left', 'Spine', 'Hip-centro', 'Hip-Right', 'Hip-Left', 'Knee-Right', 'Knee-Left',
			   'Ankle-Right', 'Ankle-Left', 'Foot-Right', 'Foot-Left']

class Filter:
	def __init__(self,path="/Users/niko/Documents/KinectGaitRecognition",n = 10):
		self.gaitData = gd.GaitData()
		self.points = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
		
		self.srcPath = path+"/Dataset/RawGaitDataset"
		self.dstPath = path+"/Dataset/FilteredGaitDataset"
		self.n = n
		if os.path.exists(self.dstPath):
			shutil.rmtree(self.dstPath)
			os.mkdir(self.dstPath)
		else:
			os.mkdir(self.dstPath)

	def clear(self):
		self.points = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

	def listdirNohidden(self,path):
		for f in os.listdir(path):
			if not f.startswith('.'):
				yield f

	def readData(self,personFilePath):
		person = open(personFilePath)
		personData = person.readlines()
		if len(personData) == 0:
			print "The data of file is empty:"
			print personFilePath
			return
		length = len(personData)
		for item in range(0,length/20):
			for seg in range(0,20):
				temp = personData[item*20 + seg].split(";")
		#need to append different kind of data into different lists
				point = [string.atof(temp[1]),string.atof(temp[2]),string.atof(temp[3].replace("\n",''))]
				self.points[seg].append(point)
		#print self.points

	def dataProcess(self):
		personDirectorsPath = self.srcPath
		personDirectors = self.listdirNohidden(personDirectorsPath)
		for personDirector in personDirectors:
			print "Filtering:",personDirector
			personDirectorPath = personDirectorsPath + '/' + personDirector
			personFiles = self.listdirNohidden(personDirectorPath)
			for personFile in personFiles:
				personFilePath = personDirectorPath + '/' + personFile
				self.clear()
				self.readData(personFilePath)
				self.armaFilter()
				writePersonDirectorPath = self.dstPath +'/' + personDirector + '/'
				if(os.path.exists(writePersonDirectorPath)):
					self.writeData(writePersonDirectorPath+personFile)
				else:
					os.mkdir(writePersonDirectorPath)
					self.writeData(writePersonDirectorPath+personFile)

	def arma3D(self,pastValues, futureValues,ai):
		values= []
		for v in futureValues:
			values.append(v)
		for v in pastValues:
			values.append(v)
		avgmeanX = 0
		avgmeanY = 0
		avgmeanZ = 0
		for x,y,z in values:
			avgmeanX = float(ai * x) + avgmeanX
			avgmeanY = float(ai * y) + avgmeanY
			avgmeanZ = float(ai * z) + avgmeanZ
		return [avgmeanX, avgmeanY, avgmeanZ]

#this function apply arma to raw data
# n value = past and future number of frames to look backwards and aftwards total:2n
	def armaFilter(self):
		size = len(self.points[0])
		for key in range(self.n+1, size - self.n):
			for limb in range(len(self.points)):
				pastValues = []
				futureValues = []

				for i in range(1,self.n+1):
					pastValues.append(self.points[limb][key-i])
					futureValues.append(self.points[limb][key+i])
				result = self.arma3D(pastValues, futureValues, 1/(2*float(self.n)))
				self.points[limb][key] = result

#this function use the physic law
	def speedFilter(self):
		data = np.array(self.points)
		shape = np.shape(data)

	def writeData(self,dstPersonFile):
		dstFile = open(dstPersonFile,'w')
		points = np.array(self.points)

		length = len(points[0])
		for frame in range(length):
			for limb in range(0,len(points)):
				point = jointDescriptors[limb]+ ";"
				for i in range(2):
					point += str(points[limb][frame][i]) + ";"
				point += str(points[limb][frame][2]) + '\n'
				dstFile.write(point)
		dstFile.close()

if __name__ == "__main__":
	flt = Filter(srcPath[2],dstPath[1],10)
	flt.dataProcess()

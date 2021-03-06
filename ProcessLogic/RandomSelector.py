import os
import string
import shutil
import random as rd
import numpy as np
from GaitData import GaitData

jointDescriptors = ['Head', 'Shoulder-Center', 'Shoulder-Right', 'Shoulder-Left', 'Elbow-Right', 'Elbow-Left', 'Wrist-Right', 'Wrist-Left',
			   'Hand-Right', 'Hand-Left', 'Spine', 'Hip-centro', 'Hip-Right', 'Hip-Left', 'Knee-Right', 'Knee-Left',
			   'Ankle-Right', 'Ankle-Left', 'Foot-Right', 'Foot-Left']

class RandomSelector:
	def __init__(self,path="/Users/niko/Documents/KinectGaitRecognition",p=0.7):
		self.gaitData = GaitData()
		self.points = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
		self.trainPath = path+"/Dataset/TrainDataset/TrainGaitDataset"
		self.testPath = path+"/Dataset/TestDataset/TestGaitDataset"
		self.srcPath = path+"/Dataset/FilteredGaitDataset"
		self.trainMatric = []
		self.testMatric = []
		self.p = p
		temp = self.trainPath.split('/')
		path = self.trainPath.replace(temp[len(temp)-1],'')

		if(os.path.exists(path)):
			shutil.rmtree(path)
			os.mkdir(path)
		else:
			os.mkdir(path)
		os.mkdir(self.trainPath)

		temp = self.testPath.split('/')
		path = self.testPath.replace(temp[len(temp)-1],'')
		if(os.path.exists(path)):
			shutil.rmtree(path)
			os.mkdir(path)
		else:
			os.mkdir(path)
		os.mkdir(self.testPath)

	def listdirNohidden(self,path):
		for f in os.listdir(path):
			if not f.startswith('.'):
				yield f

	def clear(self):
		self.points = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

	def writeSparseMatric(self):
		trainPath = self.trainPath + '/' + "y.txt"
		testPath = self.testPath + '/' + "y.txt"

		trainFile = open(trainPath,'w')
		testFile = open(testPath,'w')
		trainLength = len(self.trainMatric)
		testLength = len(self.testMatric)
		s = []
		for i in range(trainLength):
			s.append('0')
		for i in range(trainLength):
			for j in range(self.trainMatric[i]):
				s[i] = '1'
				for k in range(trainLength):
					trainFile.write(str(s[k]))
					trainFile.write(' ')
				trainFile.write('\n')
				s[i] = '0'
		s = []
		for i in range(testLength):
			s.append('0')
		for i in range(testLength):
			for j in range(self.testMatric[i]):
				s[i] = '1'
				for k in range(testLength):
					testFile.write(str(s[k]))
					testFile.write(' ')
				testFile.write('\n')
				s[i] = '0'
		trainFile.close()
		testFile.close()

	def dataProcess(self):
		personDirectorsPath = self.srcPath
		personDirectors = self.listdirNohidden(personDirectorsPath)
		temp = []
		for p in personDirectors:
			temp.append(p)
		sorted(temp,key= lambda x:int(x.replace("Person","")))
		personDirectors = []
		personDirectors = temp
		for personDirector in personDirectors:
			personDirectorPath = personDirectorsPath + '/' + personDirector
			if not os.path.isdir(personDirectorPath):
				continue
			print "Random Select:",personDirector
			personFiles = self.listdirNohidden(personDirectorPath)
			trainPoint = 0
			testPoint = 0
			tempList = []
			for personFile in personFiles:
				tempList.append(personFile)
			personFiles = tempList
			count = int(round(len(personFiles)*self.p))
			trainFiles = rd.sample(personFiles,count)
			testFiles = list(set(personFiles).difference(set(trainFiles)))
			#train
			writePersonDirectorPath = self.trainPath +'/' + personDirector + '/'
			for personFile in trainFiles:
				personFilePath = personDirectorPath + '/' + personFile
				self.clear()
				self.readData(personFilePath)
				#self.filter()
				trainPoint += 1
				if(os.path.exists(writePersonDirectorPath)):
					self.writeData(writePersonDirectorPath+personFile)
				else:
					os.mkdir(writePersonDirectorPath)
					self.writeData(writePersonDirectorPath+personFile)
			#test
			writePersonDirectorPath = self.testPath +'/' + personDirector + '/'
			for personFile in testFiles:
				personFilePath = personDirectorPath + '/' + personFile
				self.clear()
				self.readData(personFilePath)
				#self.filter()
				writePersonDirectorPath = self.testPath +'/' + personDirector + '/'
				testPoint += 1
				if(os.path.exists(writePersonDirectorPath)):
					self.writeData(writePersonDirectorPath+personFile)
				else:
					os.mkdir(writePersonDirectorPath)
					self.writeData(writePersonDirectorPath+personFile)

			self.trainMatric.append(trainPoint)
			self.testMatric.append(testPoint)
			self.writeSparseMatric()

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
				point = [string.atof(temp[1]),string.atof(temp[2]),string.atof(temp[3].replace("\n",''))]
				self.points[seg].append(point)
		person.close()

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

if __name__ == '__main__':
	rs = RandomSelector()
	rs.dataProcess()
#coding=utf-8

import os, sys, subprocess, time
class DevCompareMod: #First generate org file, others is generate unori file
	def __init__(self, TestCaseNo): #__init__ equal DevCompareMod()
		self.unori_cycle=1
		self.TestCaseNo = TestCaseNo
		self.original_file = self.TestCaseNo+"_DevCom_ori.txt"#"_original.txt"
		self.unoriginal_file = self.TestCaseNo+"_DevCom_unori.txt"#"_unoriginal.txt"
		self.log_file = self.TestCaseNo+"_DevCom_log.txt" #"_log.txt"	
		if not os.path.exists(self.original_file):
			self.devcon(self.original_file)	#get device list to file
		else:
			self.unoriginal_file = self.devcon(self.unoriginal_file)
			self.aryCheckDeviceLost(self.original_file,self.unoriginal_file) #ori file, unori file, Lost/Found
			self.aryCheckDeviceFound(self.original_file,self.unoriginal_file)	#[], ori, unori file

	def wLog(self, txtLog):
		if not os.path.exists(self.log_file):
			wLog=open(self.log_file, "w")
			wLog.write(txtLog)
			wLog.close()		
		else:
			wLog=open(self.log_file, "a")
			wLog.write(txtLog)
			wLog.close()

	def aryCheckDeviceLost(self, scr,tar):	#file to array
		scr = open(scr,"r")
		tar = open(tar,"r")
		scrArys = []
		tarArys =[]
		i=0
		diff=[]
		strLost=""
		for s in scr: #file to array
			scrArys.append(s)
		#print scrArys
		for t in tar:
			tarArys.append(t)

		scrArys.pop()   #remove xxx matching device(s) found.
		#tarArys.pop()
		#print tarArys
		for scrAry in scrArys:   #array compare for lost
			for tarAry in tarArys:
				if scrAry in tarArys:
					i+=1
					#print "find ",i," ", scrAry	 
					break
				else:
					print "Lost: ",i," ", scrAry   #check lost
					strLost = strLost + "Lost: "+str(i)+" "+str(scrAry)
					#wLog("Lost: "+str(i)+" "+str(scrAry))
					break
		self.wLog(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())+"  [Cycle: "+str(self.unori_cycle)+"]=======================================\n")
		self.wLog(strLost)

	def aryCheckDeviceFound(self, scr,tar):	#file to array
		scr = open(scr,"r")
		tar = open(tar,"r")
		scrArys = []
		tarArys =[]
		i=0
		diff=[]
		strFound = ""
		for s in scr: #file to array
			scrArys.append(s)
		#print scrArys
		for t in tar:
			tarArys.append(t)
		#print tarArys

		tarArys.pop()   #remove xxx matching device(s) found.

		for tarAry  in tarArys:   #array compare for find
			for scrAry in scrArys:
				if tarAry not in scrArys:
					i+=1
					print "Add: ",i," ", tarAry	 #check find
					strFound  = strFound + "Add: "+str(i)+" "+str(tarAry)
					#wLog("Add: "+str(i)+" "+str(tarAry))
					break
				else:
					#print "not find ", tarAry
					break
		self.wLog(strFound)
		self.wLog("\n")

	def devcon(self, filename):   #get device to file
		try:
			output = subprocess.Popen(["devcon","status","*"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)	#useing , not space in cmd
			stdout, stderr = output.communicate()
			#print "output: \n", output
			#print "stdout: \n", stdout  # output here if ok. 
			#print "stderr: \n", stderr		 
		except subprocess.CalledProcessError:
			print("Exception handled")

		if os.path.exists(self.TestCaseNo+"_DevCom_unori.txt"):
			i=2
			self.unori_cycle = self.devcon_recur(i)
			filename = filename.replace(".txt", "_" + str(self.unori_cycle) + ".txt")

		wFile=open(filename,"w")
		wFile.write(stdout) # write stdout to file
		return filename

	def devcon_recur(self,i): #if file exists i=i+1
		if os.path.exists(self.TestCaseNo+"_DevCom_unori_"+str(i)+".txt"):
			i=i+1
			return self.devcon_recur(i)
		else:
			return i



if __name__ == '__main__':
	if len(sys.argv) < 2:
		TestCaseNo="My"
	else:
		TestCaseNo = sys.argv[1]
	
	unori_cycle=1
	DevCompareMod(TestCaseNo)

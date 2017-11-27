# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import os, subprocess, time

def wLog(txtLog):
    if not os.path.exists(log_file):
        wLog=open(log_file, "w")
        wLog.write(txtLog)
        wLog.close()
    else:
        wLog=open(log_file, "a")
        wLog.write(txtLog)
        wLog.close()

def aryCheckDeviceLost(scr,tar):    #file to array
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

    wLog(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"=======================================\n")
    wLog(strLost)

def aryCheckDeviceFound(scr,tar):    #file to array
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
                print "Add: ",i," ", tarAry     #check find
                strFound  = strFound + "Add: "+str(i)+" "+str(tarAry)
                #wLog("Add: "+str(i)+" "+str(tarAry))
                break
            else:
                #print "not find ", tarAry
                break
    wLog(strFound)
    wLog("\n")

def devcon(filename):   #get device to file
    try:
        output = subprocess.Popen(["devcon","status","*"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)    #useing , not space in cmd
        stdout, stderr = output.communicate()
        #print "output: \n", output
        #print "stdout: \n", stdout  # output here if ok.
        #print "stderr: \n", stderr
    except subprocess.CalledProcessError:
        print('Exception handled')

    if os.path.exists("unoriginal.txt"): #To add file un_1,un_2...N.
        i=1
        x = devcon_recur(i)
        filename = filename.replace(".txt", "_" + str(x) + ".txt")

    wFile=open(filename,"w")
    wFile.write(stdout) # write stdout to file
    return filename

def devcon_recur(i): #if file exists i=i+1
    if os.path.exists("unoriginal_"+str(i)+".txt"):
        i=i+1
        return devcon_recur(i)
    else:
        return i

if __name__ == "__main__":
    original_file = "original.txt"
    unoriginal_file = "unoriginal.txt"
    log_file = "log_DevCompare.txt"

    if not os.path.exists(original_file):
        devcon(original_file)    #get device list to file

    else:
        unoriginal_file = devcon(unoriginal_file) #return modify filename
        aryCheckDeviceLost(original_file,unoriginal_file) #ori file, unori file, Lost/Found
        aryCheckDeviceFound(original_file,unoriginal_file)    #[], ori, unori file


# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 17:41:06 2022
Last edited : Feb 19 , 5:28 AM
@author: Mahbub islam




"""

import cv2
import numpy as np
import math
import operator
from time import time

global ROI_DEPTH,kernel_size,clusterDepth,minAngle,maxAngle , clusters
global  changedV, initV,minAngle,maxAngle

kernel_size =7#7#9#5
ROI_DEPTH = 200 #400 #410
clusterDepth=13 # 10,15,20,30,50 <-- check output
minAngle=38.0
maxAngle=48.0

clusters = {}
counter = 0
img = cv2.imread('lab3d2.png', cv2.IMREAD_GRAYSCALE)
uniqueClusterKey = - 1
drawnList = []

# Initialize output
out1 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
out2 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
out3 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
from datetime import datetime
dt=datetime.now()
dtstr=str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)+"-"+str(dt.hour)+"-"+str(dt.minute)+"-"+str(dt.second)
dataLog=open("MasterStageLog"+dtstr+".csv","a")
dataLog.write("dateTime,clusterBetween,Difference,kernelSize,ROI_DEPTH,clusterDepth,minAngle,maxAngle\n")
def callMain():
    # main1(gray,out1)
    h=0


def findOverlap(minX1, maxX1, minX2, maxX2):
    overLappingX = - 1
    if minX1 <= minX2 <= maxX1:
        overLappingX=minX2
    elif minX2<=minX1<=maxX2: 
        overLappingX=minX1
    elif minX1<=maxX2<=maxX1:
        overLappingX=maxX2
    elif minX2<=maxX1<=maxX2:
        overLappingX=maxX1
        
    
    return overLappingX

def printText(img,x,y,text,clusterId,fontWeight):
    position = (int(x),int(y))
    color=changeColor(clusterId)
    rgb=getRGBColor(color)
    cv2.putText( img,str(text), position,
                cv2.FONT_HERSHEY_SIMPLEX,  0.4, rgb, fontWeight) 


def printInitParams():
    params='@@@@ clusterDepth= '+str(clusterDepth)+'  ROI_DEPTH= '+str(ROI_DEPTH)+'  '
    clusters={}

def getDistance(lines):
 lineArray = []
 for i in range(len(lines[0])):
     if i < (len(lines)-1):
         line1 = lines[i]
         line2 = lines[i+1]
         distance = getDistanceBetween2Lines(line1, line2)
         print(str(distance)+"= distance between "+line1+" and "+line2)


def getDistanceBetween2Lines(line1, line2):
    xDist = line1[0]-line2[0]
    yDist = line1[1]-line2[1]
    distance = math.sqrt(abs(xDist)*abs(xDist)+abs(yDist)*abs(yDist))
    return distance


def showLines(lines):
    counter = 0
    for a in range(0, (len(lines)), 2):

        line1 = lines[a]
        line2 = lines[a+1]
        x1 = line1[0][0]
        y1 = line1[0][1]
        x2 = line1[0][2]
        y2 = line1[0][3]
        counter += 1
        angle = np.rad2deg(np.arctan(y2/y1))
        if angle == 45:  # and angle <= 50:
            di = getDistanceBetween2Lines(line1, line2)
            cv2.line(out1, (x1, y1), (x2, y2), (0, 0, 255), 1)
            print(str(di)+"["+str(a)+","+str(a+1)+"]")


def findSlope(x1, y1, x2, y2):
    x = (x2 - x1)
    m = float("nan")
    if x != 0:
        m = (y2 - y1) / x
    return m


def findYIntercept(x1, y1, m):
    c = float("nan")
    if math.isnan(m) == False:
        c = y1-m*x1
    return c


def isAngleInRange(line1, low, high):
    
    y1 = line1[0][1]
    y2 = line1[0][3]
    if y1<ROI_DEPTH :
        return False
    angle = np.rad2deg(np.arctan(y2/y1))

    if angle >= low and angle <= high:
        return True
    return False


def detectLinesFromImage(gray):

    # Read input
    # img = cv2.imread('lab3d.png')

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # out = gray
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
    detected_lines = cv2.morphologyEx(
        blur_gray, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    edges = cv2.Canny(detected_lines, 0, 255)
    lines = cv2.HoughLinesP(edges, rho=0.25, theta=np.pi / 180, threshold=20,
                            lines=np.array([]), minLineLength=50,
                            maxLineGap=100)
    return lines

global linesWritten

def drawLinesOnImage(gray,lines,minAngle,maxAngle):
    global linesWritten
    linesWritten     = 0
    for line in lines:
        for x1, y1, x2, y2 in line:
            #print(line)
            angle = np.rad2deg(np.arctan(y2/y1))
            if angle >= minAngle and angle <= maxAngle and y2 > ROI_DEPTH:
             #   print(angle)
                cv2.line(gray, (x1, y1), (x2, y2), (0, 0, 255), 1)
                linesWritten += 1
   

    return linesWritten

def printLine(out,x1,y1,x2,y2,currentColor , lineThickness):
              
              # DRAW ROI_DEPTH  
              printText(out, 4,ROI_DEPTH-5, 'ROI _ DEPTH___'+str(ROI_DEPTH), 100, 1)
              cv2.line(out, (4, ROI_DEPTH), (200, ROI_DEPTH), (255, 255, 255), 1)

              rgb=getRGBColor(currentColor)
              cv2.line(out, (x1, y1), (x2, y2), rgb, lineThickness)
           
            
def getRGBColor(currentColor):
    rgb=(0,0,0)
    if currentColor=="GREEN":
        rgb= (0, 255, 0)
    elif currentColor=="RED":
        rgb=  (0, 0,255)
    elif currentColor=="BLUE":
        rgb=(204,179,255)
    elif currentColor=="PERSIAN_GREEN":
         rgb= (191,0,230)#(0,179,149)#(121, 85, 72)
    elif currentColor=="YELLOW":
         rgb= (255,255,0)
    elif currentColor=="SKY":
         rgb=  (0 , 255,247)
    elif currentColor=="GOLDEN":
         rgb=  (255,137,0)
    elif currentColor=="MAGENTA":
          rgb=  ( 179,0,255)
    elif currentColor=="PINK":
          rgb=  (255 , 0, 145)
    elif currentColor=="TARQIZ":
          rgb= (0,154,255)
    elif currentColor=="LIGHT_GREEN":
          rgb= (0 , 255, 60)
    elif currentColor=="BROWN":
          rgb= ( 84, 3, 30)
    elif currentColor=="GREEN_2":
        rgb=  (66, 84, 3)
    elif currentColor=="WHITE":
          rgb= (5, 255, 237)
    return rgb

def drawEqualizedLineLength(lines,out,clusterList):
    cMinx =9999
    cMaxX=-1
    counter =0
    for v in clusterList:
        if counter==0:
            cMinX=v.minX
        if v.minX<cMinx:
            cMinX=v.minX
        if v.maxX>cMaxX : 
            cMaxX=v.maxX
        counter+=1            
    for k in clusters.keys():
        v=clusters[k]
        minX,maxX=getMinXMaxX(lines,      v.clusterIndexList)
        indexList=v.clusterIndexList
        currentColor=changeColor(v.clusterId)
        minY=min(v.yList)
        maxY=max(v.yList)
        meanY=math.floor((minY+maxY)/2)
        printLine(out,cMinX,meanY,cMaxX,meanY ,currentColor,2)



def drawSummaryLine(lines, out,clusterList):
    cMinx =9999
    cMaxX=-1
    counter =0
    
    for v in clusterList:
        if counter==0:
            cMinX=v.minX
        if v.minX<cMinx:
            cMinX=v.minX
        if v.maxX>cMaxX : 
            cMaxX=v.maxX
        counter+=1            
    # for k in clusters.keys():
        # v=clusters[k]
    cl=0
    for v in clusterList:
        minX,maxX=getMinXMaxX(lines,v.clusterIndexList)
        currentColor=changeColor(cl)
        minY=min(v.yList)
        maxY=max(v.yList)
        meanY=math.floor((minY+maxY)/2)
        # printLine(v.minX,meanY,v.maxX,meanY ,currentColor,3)
        # printLine(cMinX,meanY,cMaxX,meanY ,currentColor,1)
        # printLine(out,minX,meanY,maxX,meanY ,currentColor,2)
        printLine(out,minX,maxY,maxX,maxY ,currentColor,2)
        printText(out, minX-30, meanY, 'C-'+str(counter-cl), cl,1)
        cl+=1        



def printClusterDistance(lines, out, clusterList,tString):
    clusterCounter =0;
    distance=-1
    
    
    overlay = out.copy()
    cv2.rectangle(overlay, (650,0), (900,930), (0,0,0),-1);
    alpha = 0.4  # Transparency factor.
    cv2.addWeighted(out, alpha, overlay, 1 - alpha,0.0, out)
    
    cv2.putText( out,"TIME: "+str(tString), (700,40),cv2.FONT_HERSHEY_SIMPLEX,  .5, (0, 255,0), 1) 

    for v1 in clusterList:
        
        cLen=len(clusterList)
        if clusterCounter+1<cLen:
            minX1, maxX1 = getMinXMaxX(lines, v1.clusterIndexList)
            currentColor1 = changeColor(v1.clusterId)
            minY1 = min(v1.yList)
            maxY1 = max(v1.yList)
            meanY1 = math.floor((minY1 + maxY1) / 2)
            v2=clusterList[clusterCounter+1]
            minX2, maxX2 = getMinXMaxX(lines, v2.clusterIndexList)
            currentColor2 = changeColor(v2.clusterId)
            minY2 = min(v2.yList)
            maxY2 = max(v2.yList)
            meanY2 = math.floor((minY2 + maxY2) / 2)
            overLappingX=findOverlap(minX1, maxX1, minX2, maxX2)
            #DOC3: Draw distance only if the two closest adjacent
            #clusters have an overlapping point
            if overLappingX!=-1:
                # distance=abs(meanY1-meanY2)
                distance=abs(maxY1-maxY2)
                if clusterCounter==0:
                    y=1
                else:
                    y=clusterCounter+2                        
                printText(out, 700,
                          150+y*15,
                          # 30*y+1, 
                          'C ['+str(cLen-clusterCounter)+'-'
                          +str(cLen-clusterCounter-1)+']  '+str(distance),
                          clusterCounter,1)
                print(str(getTimeHMS())+' '+'C ['+str(cLen-clusterCounter)+'-'
                +str(cLen-clusterCounter-1)+']  '+str(distance))
#dataLog.write("dateTime,clusterBetween,Difference,kernelSize,ROI_DEPTH,clusterDepth,minAngle,maxAngle")

                dataLog.write(
                    str(tString)+','+
                    'C['+str(cLen-clusterCounter)+'-'+str(cLen-clusterCounter-1)+'],'+
                    str(distance)+','+
                    str(kernel_size)+','+
                    str(ROI_DEPTH)+','+
                    str(clusterDepth)+','+
                    str(minAngle)+','+
                    str(maxAngle)+'\n')
            # else:
            #DOC3 todo :
                # for each next adjacnet cluster, 
                #find an overlap, if overlap found ,
                #calculate & draw distance
              
                
        clusterCounter+=1
        

def drawEachLine(lines,out,clusterList):
    global drawnList
    # for k in clusters.keys():
      # v=clusters[k]
    for v in clusterList:
        
      print('--- '+' '+str(v))
      indexList=v.clusterIndexList
      currentColor=changeColor(v.clusterId)
      
      minY=min(v.yList)
      maxY=max(v.yList)
      meanY=math.floor((minY+maxY)/2)
      
      for cli in indexList:
          if cli not in drawnList:
              line = lines[cli]
              drawnList.append(cli)
              for x1, y1, x2, y2 in line:
                  drawnYList.append(y1)
                  printLine(out,x1,y1,x2,y2,currentColor,1)
  
def getMinXMaxX(lines,indexList):
    xMin=0 
    xMax=0
    for k in indexList:
        if k <len(lines):
            line =lines[k]
            for x1,y1,x2,y2 in line:
                if xMin==0:
                    xMin=x1
                elif x1<xMin:
                    xMin=x1
                if xMax==0:
                    xMax=x2
                elif x2>xMax:
                    xMax=x2
        
    return (xMin,xMax)
    



def changeColor(k):
    global currentColor, prevK, firstCall
   
    colorDict={
               0:"PERSIAN_GREEN",
               1:"GREEN",
               2:"RED",
               3:"BLUE",
               4:"YELLOW", # 255,255,0
               5:"SKY", # 0 , 255,247
               6:"GOLDEN", # 255,137,0
               7:"MAGENTA", # 179,0,255
               8:"PINK" , # 255 , 0, 145
               9:"TARQIZ",  # 0,154,255
               10:"LIGHT_GREEN", # 0 , 255, 60
               11:"BROWN" ,# 84, 3, 30
               12:"GREEN_2", # 66, 84, 3
               13:"PERSIAN_GREEN",
               14:"GREEN",
               15:"RED",
               16:"BLUE",
               17:"YELLOW", # 255,255,0
               18:"SKY", # 0 , 255,247
               19:"GOLDEN", # 255,137,0
               20:"MAGENTA", # 179,0,255
               21:"PINK" , # 255 , 0, 145
               22:"TARQIZ",  # 0,154,255
               23:"LIGHT_GREEN", # 0 , 255, 60
               24:"BROWN" ,# 84, 3, 30
               25:"GREEN_2", # 66, 84, 3
               26:"GREEN_2", # 66, 84, 3
               27:"PERSIAN_GREEN",
               28:"GREEN",
               29:"RED",
               30:"BLUE",
               31:"YELLOW", # 255,255,0
               32:"SKY", # 0 , 255,247
               33:"GOLDEN", # 255,137,0
               34:"MAGENTA", # 179,0,255
               35:"PINK" , # 255 , 0, 145
               36:"TARQIZ",  # 0,154,255
               37:"LIGHT_GREEN", # 0 , 255, 60
               38:"BROWN" ,# 84, 3, 30
               39:"GREEN_2", # 66, 84, 3
               40:"PERSIAN_GREEN",
               41:"GREEN",
               42:"RED",
               43:"BLUE",
               44:"YELLOW", # 255,255,0
               45:"SKY", # 0 , 255,247
               46:"GOLDEN", # 255,137,0
               47:"MAGENTA", # 179,0,255
               48:"PINK" , # 255 , 0, 145
               49:"TARQIZ",  # 0,154,255
               50:"LIGHT_GREEN", # 0 , 255, 60
               51:"BROWN" ,# 84, 3, 30
               52:"GREEN_2", # 66, 84, 3
               53:"BLUE",
               54:"YELLOW", # 255,255,0
               55:"SKY", # 0 , 255,247
               56:"GOLDEN", # 255,137,0
               57:"MAGENTA", # 179,0,255
               58:"PINK" , # 255 , 0, 145
               59:"TARQIZ",  # 0,154,255
               60:"LIGHT_GREEN", # 0 , 255, 60
               61:"GREEN",
               62:"RED",
               63:"BLUE",
               64:"YELLOW", # 255,255,0
               65:"SKY", # 0 , 255,247
               66:"GOLDEN", # 255,137,0
               67:"MAGENTA", # 179,0,255
               68:"PINK" , # 255 , 0, 145
               69:"TARQIZ",  # 0,154,255
               70:"LIGHT_GREEN", # 0 , 255, 60
               71:"BROWN" ,# 84, 3, 30
               72:"GREEN_2", # 66, 84, 3
               73:"PERSIAN_GREEN",
               74:"GREEN",
               75:"RED",
               76:"BLUE",
               77:"YELLOW", # 255,255,0
               78:"SKY", # 0 , 255,247
               79:"GOLDEN", # 255,137,0
               80:"MAGENTA", # 179,0,255
               81:"PINK" , # 255 , 0, 145
               82:"TARQIZ",  # 0,154,255
               83:"LIGHT_GREEN", # 0 , 255, 60
               84:"BROWN" ,# 84, 3, 30
               85:"GREEN_2", # 66, 84, 3
               86:"GREEN_2", # 66, 84, 3
               87:"PERSIAN_GREEN",
               88:"GREEN",
               89:"RED",
               90:"BLUE",
               91:"YELLOW", # 255,255,0
               92:"SKY", # 0 , 255,247
               93:"GOLDEN", # 255,137,0
               94:"MAGENTA", # 179,0,255
               95:"PINK" , # 255 , 0, 145
               96:"TARQIZ",  # 0,154,255
               97:"LIGHT_GREEN", # 0 , 255, 60
               98:"BROWN" ,# 84, 3, 30
               99:"GREEN_2", # 66, 84, 3
               100:"PERSIAN_GREEN",
               
               }
    if k>=0 and k<=100:
        return colorDict[k]
    else : 
        return "WHITE"
   
drawnYList=[]

                

def getMean(yList):
    yList=getDistictList(yList)
    tot = 0
    meanY=0
    for y in yList:
        tot+=y
    if len(yList)>0:
        meanY=tot/len(yList)
    return meanY


def copyDistictList(srcList, destList):
    for src in srcList:
        if src not in destList:
            destList.append(src)
    return destList


def addToDistictList(indexList, value):
    value=getSingleValue(value)
    indexList = getDistictList(indexList)
    if value not in indexList:
        indexList.append(value)
    return indexList    

def getDistictList(yList):
    dest=[]
    for l in yList:
        if isinstance(l, list):
            for x in l:
                dest.append(x)
        else:
            dest.append(l)
    return dest

class DistInfo:

    clusterId=-1
    minX = 0
    maxX = 0
    yList = []
    meanY=0
    maxY=0
    clusterIndexList=[]

    def getClusterIndexList(self):
        return self.clusterIndexList

    def addToClusterIndexList(self, v):
        self.clusterIndexList = addToList(v, self.clusterIndexList)

    def __str__(self):
        
        strA = 'ClusterId= '+str(self.clusterId) +" minX="+str(self.minX)+", maxX= "+str(self.maxX)+\
            " Y-Mean= "+str(self.meanY)+"  maxY= "+str(self.maxY)+\
            " minY= "+str(np.min(self.yList))+" yList= "+str(self.yList)+\
            " , clusterIndexList= "+str(self.clusterIndexList)
        return strA


def decomposeList(lst):
    yList = []
    for li in lst:
        if isinstance(li, list):
            for it in li:
                if not it in yList:
                    yList.append(it)
        else:
            if li not in yList:
                yList.append(li)
    return yList


def findMean(list1):
    tot=0
    cnt=0
    for l in list1:
        
        if isinstance(l, list):
                for li in l:
                    tot+=li
                    cnt+=1
        else:
            tot+=l
            cnt+=1
    mean =np.nan
    if cnt!=0:
        mean=math.floor(tot/cnt)
    return mean

globalMinX=0
globalMaxX=0
def addSingleIndexToCluster(line1Y, index,line1):
    global uniqueClusterKey , clusters, globalMinX, globalMaxX
    indexAdded=False
    for key in clusters.keys():
        
        v = clusters[key]
        
        yList = decomposeList(v.yList)
        maxY=max(yList)
        minY=min(yList)
        clusterIndexList=v.clusterIndexList
        if index in clusterIndexList: 
            return
        if (line1Y>=maxY and  line1Y-minY<=clusterDepth )or (line1Y<maxY and maxY-line1Y<=clusterDepth):
            if index not in clusterIndexList:
                clusterIndexList=addToDistictList(clusterIndexList, index)
                v.clusterIndexList=clusterIndexList
                # ADD Y 
                v.yList=addToDistictList(v.yList, line1Y)
                # CALC GLOBAL MinX
                x1=getSingleValue(line1[0][0])
                x2=getSingleValue(line1[0][2])
                if globalMinX==0:
                    globalMinX=x1
                elif x1 <globalMinX:
                    globalMinX=x1
                #ADD MinX
                if x1<v.minX:
                    v.minX=x1
                    # CALC GLOBAL MaxX
                if globalMaxX==0:
                    globalMaxX=x2
                elif x2 >globalMaxX:
                    globalMaxX=x2
                #ADD MaxX
                if x2>v.maxX:
                    v.maxX=x2
                #ADD meanY
                meanY=findMean(v.yList)
                v.meanY=meanY
                #ADD maxY
                v.maxY=max(yList)
                clusters[key]=v
                indexAdded=True
                addedIndex=index
                addedY=line1Y
                addedCluster=key
                break
   
    if indexAdded==False:
        # create a new Cluster and add the index to it
        minX=getSingleValue(line1[0][0])
        maxX=getSingleValue(line1[0][2])
        yList=[line1Y]
        newDistInfo = DistInfo()
        newDistInfo.minX=minX
        newDistInfo.maxX=maxX
        newDistInfo.clusterIndexList=[index]
        newDistInfo.yList=[getSingleValue(line1Y)]
        #ADD maxY
        newDistInfo.maxY=max(yList)
        uniqueClusterKey+=1
        newDistInfo.clusterId=uniqueClusterKey
        clusters[uniqueClusterKey]=newDistInfo
   
        print("\n\n==== added new Cluster = "+str(uniqueClusterKey)\
             +" index = "+str(index)\
                 +" lin1Y= "+str(line1Y) \
                     + " new yList= "+str(yList)\
                         +" new indexList= "+str(newDistInfo.clusterIndexList))
    
    
   
       
def addToExistigCluster(minX, maxX, k, h, line1Y, line2Y, line1,line2):
    
    linY1=getSingleValue(line1Y)
    linY2=getSingleValue(line2Y)
    addSingleIndexToCluster(linY1, k,line1)
    addSingleIndexToCluster(linY2, h,line2)

def addToList(v, lst):
    l = len(lst)
    if isinstance(v, list):
        lst.extend(decomposeList(v))
    else:
        lst.append(v)

    return lst

def processClustering(lines,minAngle, maxAngle, clusterDepth):
    global clusters
    clusters={}
    for k in range(len(lines)-1):
        line1 = lines[k]
        if isAngleInRange(line1, minAngle, maxAngle) and line1[0][1] > ROI_DEPTH:
            c1 = np.nan # type(np.nan)=> float
            m1 = findSlope(line1[0][0], line1[0][1], line1[0][2], line1[0][3])

            if math.isnan(m1) == False:
                c1 = findYIntercept(line1[0][0], line1[0][1], m1)

            if not math.isnan(c1):
                for h in range(k+1, len(lines)-1):
    
                    line2 = lines[h]
                    if line2[0][3] > ROI_DEPTH:
                        m2 = findSlope(line2[0][0], line2[0][1],
                                       line2[0][2], line2[0][3])
                        if not math.isnan(m1) and not math.isnan(m2):
                            floorM1 = math.floor(m1)
                            floorM2 = math.floor(m2)
                            c2 = findYIntercept(line2[0][0], line2[0][1], m2)
                            minDist = abs(c2-c1)/math.sqrt(1+m1*m1)
                            if minDist<0:
                                minDist=0
                            if minDist <= clusterDepth:
                                minX = line1[0][0] if line1[0][0] < line2[0][0] else line2[0][0]
                                maxX = line1[0][2] if line1[0][2] > line2[0][2] else line2[0][2]
                                addToExistigCluster(minX, maxX, k, h,
                                           getSingleValue(line1[0][3]), getSingleValue(line2[0][3]), line1,line2)

   
def getSingleValue(valOrList):
     retVal=-1
     if isinstance(valOrList,list):
         retVal=valOrList.pop(0)
     else:
         retVal=valOrList
     return retVal 


def drawCluster(out1,lines,tString):
    global  drawnList , clusters

    clusterList=sorted(clusters.values(),key=operator.attrgetter('maxY'))
    
    drawSummaryLine(lines,out1,clusterList)
    # drawEachLine(lines,out2,clusterList)
    drawEqualizedLineLength(lines,out3,clusterList)
    printClusterDistance(lines, out1, clusterList,tString)

    
def main1(gray, out1,tString):
    global  drawnList , clusters
    simulateROI_DEPTHChange(tString)

    printInitParams()
    lines = detectLinesFromImage(gray)

    processClustering(lines,minAngle, maxAngle, clusterDepth)
    totalLineCount=drawLinesOnImage(gray,lines,minAngle, maxAngle)
    drawCluster(out1,lines,tString)
    clusterSize=len(clusters.keys())
    
    
    overlay = out1.copy()
    
    cv2.rectangle(overlay, (0,0), (170,230), (0,0,0),-1);
  
    alpha = 0.5  # Transparency factor.
    
    # Following line overlays transparent rectangle over the image
    cv2.addWeighted(out1, alpha, overlay, 1 - alpha,0.0, out1)
    
    printText(out1, 4,25, "lines detected: "+str(lines.size), 2, 1)
    printText(out1, 4,40, "clusterSize: "+str(clusterSize), 4, 1)
    #printText(out1, 4,100, "Time: "+str(tString), 100, 1)
    printText(out1, 4, 70, "ClusterDepth: " + str(clusterDepth), 100, 1)
    printText(out1, 4,95, "MinAngle: "+str(minAngle), 100, 1)
    printText(out1, 4,115, "MaxAngle: "+str(maxAngle), 100, 1)
 
    printText(out1, 4,130, "kernel_size: "+str(kernel_size), 4, 1)
    printText(out1, 4,150, "totalLineCount: "+str(totalLineCount), 5, 1)
    printText(out1, 4,175, "Frame Per Second: "+str(framePerSecond), 6, 1)
    printText(out1, 4,195, "FrameCount: "+str(frameCount), 6, 1)

    # print(' EndSecond= '+str(endSecond)+' startSecond= '+str(startSecond)+' framePerSecon= '+str(frameCount))
    
   
 
    
    printText(out1, 4,ROI_DEPTH-5, 'ROI _ DEPTH', 100, 1)
    cv2.line(out1, (4, ROI_DEPTH), (200, ROI_DEPTH), (255, 255, 255), 1)

    

    # print("====== num of lines detected  ="+str(lines.size))
    # print(" num of lines written="+str(len(drawnList)))
    # print(lines[0])
    # print(lines[len(lines)-1])
    # for kc in clusters.keys():
    #     distInfo = clusters[kc]
    #     print(distInfo)
   # cv2.imshow('Unified clustered lines', out1)
    # cv2.imshow('Clustered Lines', out2)
    # cv2.imshow('Lines read ', gray)
    # cv2.imshow('Equalized line length+ Unified lines ', out3)
    print("DrawnIndexList= "+str(sorted(drawnYList)))

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


callMain()

global mainImage

def setInitV(img):
    global initV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    initV=v

def increase_brightness(img, value=30):
    global initV,changedV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    if initV==-999999:
        initV=v

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    changedV=final_hsv
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img
changedV=0

def onChangeV(v):
    global changedV
    changedV=cv2.getTrackbarPos('V', 'wqualized')
    increase_brightness(mainImage,changedV)

    # todo:  Fix HSV to adjust brightness
def getTimeMillis(h,m,s,mss)    :
   return  mss+s*1000+m*60*1000+h*3600*1000

def  simulateROI_DEPTHChange(tString): # simulateROIDEPTHCHANGE
    global ROI_DEPTH

    tHmss=str(tString).split(':')
    h=int(tHmss[0])
    m=int(tHmss[1])
    s=int(tHmss[2])
    mss=int(tHmss[3])
    print(tHmss)
    tms=getTimeMillis(h, m, s, mss)
    
    if tms in range(getTimeMillis(0,0,0,0),getTimeMillis(0, 0, 48, 0)):
     ROI_DEPTH=400
    # 0:0:48:269= 390
   
   
    elif tms in range(getTimeMillis(0, 0, 48, 1),getTimeMillis(0,1,38,232)):
     ROI_DEPTH=390

   
    # 0:1:50:232 = 360
    #elif tms in range(90233,145000):
    
    elif tms in range(getTimeMillis(0, 1, 38, 233),getTimeMillis(0,2,28,000)):
     ROI_DEPTH=363
    # 0:2:25:000 = 338

    elif tms in range(getTimeMillis(0,2,28,1),getTimeMillis(0, 3, 28, 499)):
       ROI_DEPTH=344
  # 0:2:25:000 = 338

  
   # 0:6:55:555 = pause
  
     # 0:9:7:400 = ON
     # 0:10:14:147 = 315
  #  elif tms in range(getTimeMillis(0,3,10,500),getTimeMillis(0, 4, 0, 0)):
   #   ROI_DEPTH=500

    elif tms in range(getTimeMillis(0,4,1,1),getTimeMillis(0, 5, 14, 130)):
        ROI_DEPTH=315
   
     # 0:12:33:131 = 279
    elif tms in range(getTimeMillis(0,4,59, 131),getTimeMillis(0, 5, 14, 000)):
    
        ROI_DEPTH=304
    elif tms in range(getTimeMillis(0, 5,14, 131),getTimeMillis(0, 6, 0, 000)):
        
            ROI_DEPTH=294
    elif tms in range(getTimeMillis(0, 6,0, 1),getTimeMillis(0, 7, 14, 000)):
       
           ROI_DEPTH=280
   
        
   # 0:14:32:00 = 269
    elif tms>=getTimeMillis(0,7,14,1):
        ROI_DEPTH=270
     
    print("***********change****roidepth="+str(ROI_DEPTH))

    
     


def onChangeROI(v):
    global ROI_DEPTH
    ROI_DEPTH=400
    ROI_DEPTH=cv2.getTrackbarPos('ROI_DEPTH', 'Frame')

def onChangeMinAngle(v):
    global minAngle
    minAngle=cv2.getTrackbarPos('minAgnle', 'gray')

def onChangeMaxAngle(v):
    global maxAngle
    maxAngle=cv2.getTrackbarPos('maxAgnle', 'gray')

def onChangeClusterDepth(v):
    global clusterDepth
    clusterDepth=cv2.getTrackbarPos('clusterDepth', 'wqualized')


def onChangeKernel(v):
    global kernel_size

    
    tempKernel=cv2.getTrackbarPos('kernel', 'gray')

    if  tempKernel%2==0:
        tempKernel+=1
        cv2.setTrackbarPos('kernel', 'gray', tempKernel)
        kernel_size=tempKernel
    else:
        kernel_size=tempKernel
        
def getTimeHMS():
    ms=int((time())*divisor)-t
    mss=int(ms%divisor/1000)
    s = (int) (ms // divisor) % 60 ;
    m = (int) ((ms // (divisor*60)) % 60);
    h   = (int) ((ms // (divisor*60*60)) % 24);
    return (h,m,s,mss)
        
        
cap = cv2.VideoCapture(
    #'lab3d.mp4'
    'lab3d_converted.mp4'
    # 'coverModified.mp4'
    ,cv2.IMREAD_GRAYSCALE)

divisor=1000000
t=(int)(time()*divisor)


cv2.imshow('gray', out1)
cv2.imshow('wqualized', out1)
cv2.imshow('Frame', out1)

cv2.createTrackbar('kernel', 'gray', 7,12,onChangeKernel)
cv2.createTrackbar('minAgnle', 'gray', 38,90,onChangeMinAngle)
cv2.createTrackbar('maxAgnle', 'gray', 48,90,onChangeMaxAngle)
cv2.createTrackbar('clusterDepth', 'wqualized', 13,40,onChangeClusterDepth)
# cv2.createTrackbar('V', 'wqualized', 0,900,onChangeV)
cv2.createTrackbar('ROI_DEPTH', 'Frame', 400,900,onChangeROI)

# cv2.createTrackbar('kernel', 'gray', 1,12,onChangeKernel)
global framePerSecond, startSecond , endSecond, frameCount
framePerSecond=0

startSecond=0 
endSecond=0
frameCount=0
processFPS=0
while (True):
    if cap.isOpened():
        
 
        ret, frame =cap.read( )
        
        frameCount=frameCount+1;
        if ret==True:
            # frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0, interpolation = cv2.INTER_CUBIC)
            #gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            processFPS+=1    
            # out1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            uniqueClusterKey=0
            clusters=0
            globalMinX=0
            globalMaxX=0
            
            h,m,s,mss=getTimeHMS()
            if startSecond==0:
                startSecond=s
            endSecond=s
            if endSecond-startSecond==1:
                startSecond=s
                framePerSecond=frameCount
                frameCount=1
        
            # if frameCount<5:
                
            tString=str(h)+":"+str(m)+":"+str(s)+":"+str(mss)
            mainImage=frame.copy()
            out3=frame.copy()
            # setInitV(mainImage)
    
            main1(mainImage,frame,tString)
            # printText(frame, 4,95, "initV: "+str(initV), 100, 1)
            # printText(out3, 4,105, "changedV: "+str(changedV), 100, 1)
    
    
    
            cv2.imshow('Frame', frame)
            cv2.imshow('gray', mainImage)
            cv2.imshow('wqualized', out3)
    
            # out2=cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
            # out3=cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
            # gray=cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
            # if cv2.waitKey(35) & 0xFF == ord('q'):
            #         break
            key = cv2.waitKey(22)

            if key == 32:
                cv2.waitKey()
            elif key == ord('q') or not cap.isOpened():
                break
# release the video capture object
dataLog.close();
cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()

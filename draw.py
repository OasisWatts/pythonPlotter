import sys
import matplotlib.pyplot as plt
import os.path as os
import numpy as np
import math
import json

# 그리기 형식 - plot에 따라 알맞게 변경
def start_plot():
    plt.figure(figsize=(8,5))
    plt.rcParams.update({
        'axes.labelsize': 15,
        'axes.titlesize': 18,
        "xtick.labelsize": 12,
        "ytick.labelsize": 15,
        "lines.linewidth": 3,
    })

def draw(xList, yList):
    plt.clf()
    if not xList:
        plt.plot(yList)
    else: plt.plot(xList, yList)

def scatter(xList, yList):
    plt.clf()
    plt.scatter(xList, yList)

def bar(xList, yList):
    plt.clf()
    if type(xList[0]) == type(""):
        xLenList = [len(i) for i in xList]
        maxLen = np.max(xLenList)
        for idx, i in enumerate(xList):
            leftLen = maxLen-len(i)
            front = " " * math.floor(leftLen/2)
            rear = " " * math.floor(leftLen/2)
            if leftLen % 2 == 1:
                rear += " "
            xList[idx] = front + i + rear
    plt.bar([i for i in range(len(xList))], yList)
    plt.xticks([i for i in range(len(xList))], xList)

def hist(xList, yList):
    plt.clf()
    plt.hist(xList, bins=len(xList), weights=yList)

def finish_plot(xlabel, ylabel, title, filename):
    plt.xlabel(xlabel, labelpad=10)
    plt.ylabel(ylabel, labelpad=10)
    plt.title(title, pad=15)
    plt.grid(True)
    plt.margins(x=0,y=0)
    plt.tight_layout()
    if os.isfile(filename+".png"):
        save_plot(filename, 1)
    else:
        plt.savefig(filename+".png")

def save_plot(title, number):
    newFn = title + "_"+ str(number)+".png"
    if os.isfile(newFn):
        save_plot(title, number+1)
    else:
        plt.savefig(newFn)  

def tilt_label():
    plt.xticks(rotation=45)


if __name__ == "__main__":
    drawMethod = sys.argv[1]
    xFile = sys.argv[2] # x 데이터 파일명 (따로 없으면 "False")
    yFile = sys.argv[3] # y 데이터 파일명 (따로 없으면 "False")
    xLabel = sys.argv[4] # x 라벨
    yLabel = sys.argv[5] # y 라벨
    title = sys.argv[6] # title
    outputFile = sys.argv[7] # plot filename
    print(sys.argv[8])
    option = json.loads(sys.argv[8])
    xStringTo = False
    if "xStringTo" in option: # x 데이터를 숫자 (int/float etc)로 바꿔야 하면 각각 int/float
        xStringTo = option["xStringTo"]
    xSort = False
    if "xSort" in option: # x 데이터 기준으로 sorting
        xSort = option["xSort"]
    ySort = False
    if "ySort" in option: # y 데이터 기준으로 sorting
        ySort = option["ySort"]
    dist = False
    if "dist" in option: # x 데이터의 unique의 갯수를 세서 y 데이터를 만듦. x 데이터는 자연스럽게 sorting됨. x 데이터를 세는 구간 값(예-1000, 0~1000을 0번째 구간으로 센다)
        dist = option["dist"]
    cdf = False
    if "cdf" in option: # "distribution"과 같으나, cdf를 구함.
        cdf = option["cdf"]
    yRatio = False
    if "yRatio" in option: # y 데이터 비율로 반영하기. y 데이터 / y 총합
        yRatio = option["yRatio"]
    xTilt = False
    if "xTilt" in option: # x 라벨 기울기기
        xTilt = option["xTilt"]
    xLog = False
    if "xLog" in option: # x scale = log
        xLog = option["xLog"]
    yLog = False
    if "yLog" in option: # x scale = log
        yLog = option["yLog"]

    xList = []
    yList = []

    # x 데이터 열기
    if drawMethod != "False":
        fx = open(xFile, "r")
        if xStringTo == "int":
            while True:
                line = fx.readline()
                if not line:
                    break
                xList.append(int(line))
        else:
            while True:
                line = fx.readline()
                if not line:
                    break
                xList.append(line[:-1])
        fx.close()

    # y 데이터 열기
    if yFile != "False":
        fy = open(yFile, "r")
        while True:
            line = fy.readline()
            if not line:
                break
            yList.append(int(line))
        fy.close()

    # option (데이터 가공)
    if dist:
        Max = np.max(xList)
        yList = [0 for i in range(math.ceil(Max/dist)+1)]
        for i in xList:
            yList[math.ceil(i/dist)]+=1
        xList = []
    
    if cdf:
        Max = np.max(xList)
        yList = [0 for i in range(math.ceil(Max/cdf)+1)]
        for i in xList:
            yList[math.ceil(i/cdf)]+=1
        xList = []
        yList = np.cumsum(yList)/np.sum(yList)

    if xSort:
        oldYList = yList
        oldXList = xList
        xList.sort(reverse=True)
        for xidx, x in enumerate(xList):
            oldIdx = oldXList.index(x)
            yList[xidx] = oldYList[oldIdx]

    if ySort:
        oldYList = yList
        oldXList = xList
        yList.sort(reverse=True)
        for yidx, y in enumerate(yList):
            oldIdx = oldYList.index(y)
            xList[yidx] = oldXList[oldIdx]

    if yRatio:
        sum = np.sum(yList)
        yList = [i/sum for i in yList]

    # 그리기 설정
    start_plot()

    # 그리기
    if drawMethod == "plot":
        draw(xList, yList)
    elif drawMethod == "scatter":
        scatter(xList, yList)
    elif drawMethod == "bar":
        bar(xList, yList)
    elif drawMethod == "hist":
        hist(xList, yList)

    # option (후처리)
    if xTilt:
        tilt_label()

    if xLog:
        plt.xscale("log")

    if yLog:
        plt.yscale("log")

    # 마무리
    finish_plot(xLabel.replace("_", " "), yLabel.replace("_", " "), title.replace("_", " "), outputFile)
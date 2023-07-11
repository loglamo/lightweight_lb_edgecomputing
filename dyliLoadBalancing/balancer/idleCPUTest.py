import jsons
import sys

def takeLatestCPUUtilization(fileDir):
    fileReading = open(fileDir, 'r')
    lastLine = ""
    for line in fileReading: 
        lastLine = line
        continue
    fileReading.close()
    return lastLine

def getIdleCPU():
    cpu2 = takeLatestCPUUtilization('../collection/cpu_utilization_2.csv')
    cpu2 = float(cpu2)
    cpu3 = takeLatestCPUUtilization('../collection/cpu_utilization_3.csv')
    cpu3 = float(cpu3)
    cpu4 = takeLatestCPUUtilization('../collection/cpu_utilization_4.csv')
    cpu4 = float(cpu4)
    cpu5 = takeLatestCPUUtilization('../collection/cpu_utilization_5.csv')
    cpu5 = float(cpu5)
    cpu6 = takeLatestCPUUtilization('../collection/cpu_utilization_6.csv')
    cpu6 = float(cpu6)
    idleCPU = [cpu2, cpu3, cpu4, cpu5, cpu6]
    return idleCPU

idleCPU = getIdleCPU()
print(idleCPU)

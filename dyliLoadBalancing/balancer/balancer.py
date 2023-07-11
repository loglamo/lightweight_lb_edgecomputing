from kafka import KafkaProducer
from kafka import KafkaConsumer
import jsons
import json
import time
import random
import numpy as np
#from queue import *
#from confluent_kafka.avro import AvroConsumer 

# producer class
class MessageProducer:
    broker = ""
    topic = ""
    producer = None
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.broker, value_serializer=lambda v: jsons.dumps(v).encode('utf-8'), acks='all', retries=3)


    def sendMsg(self, msg):
        print("Controller is sending assignments to Kafka broker...")
        try:
            future = self.producer.send(self.topic, msg)
            self.producer.flush()
            future.get(timeout=60)
            print("Done with sending assignments...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex

def generateTasks(numTypes, numTasks):
    taskList = [random.randint(1, numTypes) for x in range(numTasks)]
    return taskList

def getTaskPriority(taskList):
    taskPriorityList = [None]*len(taskList)
    tmp = 0
    while tmp < len(taskList):
        if taskList[tmp] == 1:
           taskPriorityList[tmp] = 0.2
        elif taskList[tmp] == 2:
            taskPriorityList[tmp] = 0.3
        else: taskPriorityList[tmp] = 0.5
        tmp += 1
    return taskPriorityList

def takeLatestCPUUtilization(fileDir):
    fileReading = open(fileDir, 'r')
    lastLine = ""
    for line in fileReading:
        lastLine = line
        continue
    fileReading.close()
    return lastLine

def getIdleCPU():
    cpu2 = takeLatestCPUUtilization('../collection/cpu_utilization_rr/cpu_utilization_2_p50.csv')
    cpu2 = 100 - float(cpu2)
    cpu3 = takeLatestCPUUtilization('../collection/cpu_utilization_rr/cpu_utilization_3_p50.csv')
    cpu3 = 100 - float(cpu3)
    cpu4 = takeLatestCPUUtilization('../collection/cpu_utilization_rr/cpu_utilization_4_p50.csv')
    cpu4 = 100 - float(cpu4)
    cpu5 = takeLatestCPUUtilization('../collection/cpu_utilization_rr/cpu_utilization_5_p50.csv')
    cpu5 = 100 - float(cpu5)
    cpu6 = takeLatestCPUUtilization('../collection/cpu_utilization_rr/cpu_utilization_6_p50.csv')
    cpu6 = 100 - float(cpu6)
    idleCPU = [cpu2,cpu3,cpu4,cpu5,cpu6]
    return idleCPU

def proposalBalancer(taskPriorityList, idleCPU):
    indexPrioritySortList = np.argsort(taskPriorityList)
    indexIdleCPUSortList = np.argsort(idleCPU)
    bestPairs = [indexPrioritySortList, indexIdleCPUSortList]
    bestPairs = np.array(bestPairs)
    return bestPairs

# find best pairs in round robin
def roundrobinBalancer():
    indexPrioritySortList = [0, 1, 2, 3, 4]
    indexIdleCPUSortList = [0, 1, 2, 3, 4]
    bestPairs = [indexPrioritySortList, indexIdleCPUSortList]
    bestPairs = np.array(bestPairs)
    return bestPairs

# create msg for round robin sending to broker
def roundrobinMSG(taskList):
    assignment = {2: 'None', 3: 'None', 4: 'None', 5: 'None', 6: 'None'}
    numberEdgeNodes = 5
    for i in range(5):
        allocatedID = i%numberEdgeNodes
        assignment[allocatedID+2] = taskList[i]
    return assignment

def getAssignment(taskList, bestPairs):
    assg = [taskList, bestPairs]
    return assg 

def writeServingValue2File(servingValue, fileDir):
    fileWriting = open(fileDir, 'a')
    value = str(servingValue) + "\n"
    fileWriting.write(value)
    fileWriting.close()
    print("Serving value was written...")

def calculateServingValue(priorityList, idleCPUList, bestPairs):
    value = 0
    for i in range(5):
        priorityIndexI = bestPairs[0][i]
        idleIndexI = bestPairs[1][i]
        value += priorityList[priorityIndexI]*idleCPUList[idleIndexI]/100
    return value

def makeAssignmentMSG(bestPairs, taskList):
    assignment = {2:'None', 3:'None', 4:'None', 5:'None', 6:'None'}
    for i in range(5):
        edgeIndexI = bestPairs[1][i]
        priorityIndexI = bestPairs[0][i]
        assignmentI = taskList[priorityIndexI]
        assignment[edgeIndexI+2] = assignmentI
    return assignment


# config broker

broker = '165.194.35.87:9092'
topic = 'assignments'
assignmentProducer = MessageProducer(broker, topic)

for i in range(100):
   taskList = generateTasks(3,5)
   priorityList = getTaskPriority(taskList)
   idleCPUList = getIdleCPU()
   #bestPairs = proposalBalancer(priorityList, idleCPUList)
   bestPairsRR = roundrobinBalancer()
   servingvalue = calculateServingValue(priorityList, idleCPUList, bestPairsRR)
   print("Best pairs are ",bestPairsRR)
   print("Current serving value is ",servingvalue)
   writeServingValue2File(servingvalue, './serving_value_result/serving_value_rr_p50.csv')
   #msg = makeAssignmentMSG(bestPairs, taskList)
   msgRR = roundrobinMSG(taskList)
   print(msgRR)
   assignmentProducer.sendMsg(msgRR)
   print("Already sent assignment...")
   time.sleep(5)


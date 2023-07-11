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
    cpu2 = takeLatestCPUUtilization('../collection/cpu_utilization_proposal/cpu_utilization_2_p5.csv')
    cpu2 = 100 - float(cpu2)
    cpu3 = takeLatestCPUUtilization('../collection/cpu_utilization_proposal/cpu_utilization_3_p5.csv')
    cpu3 = 100 - float(cpu3)
    cpu4 = takeLatestCPUUtilization('../collection/cpu_utilization_proposal/cpu_utilization_4_p5.csv')
    cpu4 = 100 - float(cpu4)
    cpu5 = takeLatestCPUUtilization('../collection/cpu_utilization_proposal/cpu_utilization_5_p5.csv')
    cpu5 = 100 - float(cpu5)
    cpu6 = takeLatestCPUUtilization('../collection/cpu_utilization_proposal/cpu_utilization_6_p5.csv')
    cpu6 = 100 - float(cpu6)
    idleCPU = [cpu2,cpu3,cpu4,cpu5,cpu6]
    return idleCPU

def proposalBalancer(taskPriorityList, idleCPU):
    indexPrioritySortList = np.argsort(taskPriorityList)
    indexIdleCPUSortList = np.argsort(idleCPU)
    bestPairs = [indexPrioritySortList, indexIdleCPUSortList]
    bestPairs = np.array(bestPairs)
    return bestPairs

def roundrobinMSG(taskList): # not consider both these things
    assignment = {2:'None', 3:'None', 4:'None', 5:'None', 6:'None'}
    numberEdgeNodes = 5
    for i in range(5):
        allocatedID = i%numberEdgeNodes
        assignment[allocatedID+2] = taskList[i]
    return assignment

def roundrobinBalancer():
    indexPrioritySortList = [0, 1, 2, 3, 4]
    indexIdleCPUSortList = [0, 1, 2, 3, 4]
    bestPairs = [indexPrioritySortList, indexIdleCPUSortList]
    bestPairs = np.array(bestPairs)
    return bestPairs

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
    # because indexes of cluster in use from cluster2 to cluster6
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

taskList = generateTasks(3,5)
priorityList = getTaskPriority(taskList)
idleCPUList = getIdleCPU()
start_time_proposal = time.time()
bestPairs = proposalBalancer(priorityList, idleCPUList)
computation_time_proposal = time.time() - start_time_proposal
print("Computation time of proposal is ", computation_time_proposal)

# rr
start_time_rr = time.time()
bestPairsRR = roundrobinBalancer()
computation_time_rr = time.time() - start_time_rr
print("Computation time of rr is ", computation_time_rr)
print("Best pairs from rr are ", bestPairsRR)

servingvalue = calculateServingValue(priorityList, idleCPUList, bestPairs)
servingvalueRR = calculateServingValue(priorityList, idleCPUList, bestPairsRR)
#print("Best pairs are ",bestPairs)
print("Current serving value of proposal is ",servingvalue)
print("Current serving value of RR is ",servingvalueRR)
msgRR = roundrobinMSG(taskList)
print(msgRR)
#writeServingValue2File(servingvalue, './serving_value_result/serving_value_proposal_p5.csv')
msg = makeAssignmentMSG(bestPairs, taskList)
print(msg)
#assignmentProducer.sendMsg(msg)
#print("Already sent assignment...")


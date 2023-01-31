from operator import index
from confluent_kafka import Consumer
from more_itertools import consume
import psutil 
from scipy import optimize 
import math
import numpy as np 
import random

# config broker servers
conf = {'bootstrap.servers': 'localhost:9092',
            'group.id': 'sensornode',
            'auto.offset.reset': 'smallest'}
#create a consumer
consumer = Consumer(conf)
#consumer subs topics 
consumer.subscribe(['sensordata1','sensordata2','sensordata3'])



temp_serving_value = 0 #store the temporary serving value 
temp_allocation = []
def hill_balancer(sensordata, CPUidle): #sensordata is an array of the sensor data type, CPUidle is an array of idle CPU of edge nodes
    global temp_serving_value
    global temp_allocation
    lenData = len(sensordata) 
    listIndex = range(0, lenData) 
    allocationIndex = random.sample(listIndex, lenData) #take indexes of allocated edge nodes 
    allocationArray = [0]*lenData       #create array of CPUidle of edge nodes
    for i in range(lenData):
        allocationArray[i] = CPUidle[allocationIndex[i]]       #take idleCPU into array of idleCPU
    products = [a*b for a, b in zip(sensordata, allocationArray)]
    current_serving_value = sum(products)
    if (current_serving_value > temp_serving_value):
        temp_serving_value = current_serving_value 
        temp_allocation = allocationIndex
    else:
        allocationIndex = temp_allocation
    return allocationIndex        #return list of edge nodes' indexes

# sensordata = [0.5, 0.5, 0.4]
# CPU = [0.1, 0.6, 0.7]
# a = hill_balancer(sensordata, CPU)
# print("the result is: ")
# print(a)
    

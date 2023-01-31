from operator import index
from confluent_kafka import Consumer
from more_itertools import consume
import psutil 
from scipy import optimize 
import math
import numpy as np

conf = {'bootstrap.servers': 'localhost:9092',
            'group.id': 'sensornode',
            'auto.offset.reset': 'smallest'}
#create a consumer
consumer = Consumer(conf)
#consumer subs topics 
consumer.subscribe(['sensordata1','sensordata2','sensordata3'])

def balancer_round_robin(clock, E):#send the current clock, the number of edge nodes
    id_allocated_server = clock%E 
    return id_allocated_server

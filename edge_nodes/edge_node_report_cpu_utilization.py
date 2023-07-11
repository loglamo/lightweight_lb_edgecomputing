from kafka import KafkaProducer
from kafka import KafkaConsumer
import jsons
import time
import numpy as np
import random
import psutil
import os

# producer class
class MessageProducer:
    broker = ""
    topic = ""
    producer = None
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.broker, value_serializer=lambda v: jsons.dumps(v).encode('utf8'), acks='all', retries = 5)

    def sendMsg(self, msg):
        print("Reporting cpu-utilization per-period")
        try:
            future = self.producer.send(self.topic, msg)
            self.producer.flush()
            future.get(timeout=60)
            print("Done reporting...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex

# take cpu utilization
def takeCPUUtilization():
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage = (load15/os.cpu_count())*100
    print('CPU usage now is: ',cpu_usage)
    return cpu_usage

# config broker
broker = '165.194.35.87:9092'
topicName = 'reports-2'
reportProducer = MessageProducer(broker, topicName)

# the period of reporting can be in 50, 30, 15, 5s
while True:
    msg = takeCPUUtilization()
    reportProducer.sendMsg(msg)
    time.sleep(5)

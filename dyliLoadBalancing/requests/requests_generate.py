from kafka import KafkaProducer
from kafka import KafkaConsumer
import jsons
import time
import numpy as np
import random
# producer class
class MessageProducer:
    broker = ""
    topic = ""
    producer = None
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.broker, value_serializer=lambda v: jsons.dumps(v).encode('utf-8'), acks='all', retries = 5)

    def sendMsg(self,msg):
        print("Controller is sending messages to Kafka broker...")
        try:
            future = self.producer.send(self.topic, msg)
            self.producer.flush()
            future.get(timeout=60)
            print("Done with sending messages...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex

# num_types: the number of task types, num_tasks: the number of tasks(reading, writing, learning)
def generateTasks(num_types, num_tasks):
    tasks_list = [random.randint(1, num_types) for x in range(num_tasks)]
    return tasks_list

broker = '165.194.35.87:9092'
topic_name = 'requests'
request_producer = MessageProducer(broker, topic_name)

num_types = 3
num_tasks = 5
#tasks = generateTasks(num_types, num_tasks)
#print(tasks)

while True:
    # this producer sends request information to topic 'requests' on Kafka broker
    msg = generateTasks(num_types, num_tasks)
    request_producer.sendMsg(msg)
    time.sleep(5)

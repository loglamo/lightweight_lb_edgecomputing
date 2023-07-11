# edge node 2 consumes assigments from broker

from kafka import KafkaConsumer, KafkaProducer                                                                                                                                                         
import sys
import os
import jsons                                                                                                                                                                                           
from json import loads     
import threading


sys.path.insert(1, '/home/syslab/workspace_la/edge_nodes/tasks/')

bootstrap_servers = ['165.194.35.87:9092']                                                                                                                                                             
assignmentTopic = ['assignments']                                                                                                                                                         

def processMSG(msg):
    print("Start task...")
    assignment = msg
    if assignment == 1:
        print("Running task1...")
        os.system('python3 /home/syslab/workspace_la/edge_nodes/tasks/task1.py')
    elif assignment == 2:
        print("Running task2...")
        os.system('python3 /home/syslab/workspace_la/edge_nodes/tasks/task2.py')
    else:
        print("Running task3...")
        os.system('python3 /home/syslab/workspace_la/edge_nodes/tasks/task3.py')


def consume():
    consumer2 = KafkaConsumer(client_id='edge node 2', bootstrap_servers = bootstrap_servers, auto_offset_reset = 'latest', value_deserializer=lambda x: loads(x.decode('utf-8')))                          
    consumer2.subscribe(topics=assignmentTopic)
    while True:
        print("Waiting for assignments...")
        records = consumer2.poll(timeout_ms=10000)
        for _, consumer_records in records.items():
            for consumer_record in consumer_records:
                print(consumer_record.value)
                value = consumer_record.value
                msg = value['2']
                print("assignment is ", msg)
                t = threading.Thread(target=processMSG, args=(msg,))
                t.daemon = True
                t.start()

consume()

from kafka import KafkaProducer                                                                                                                                                                        
from kafka import KafkaConsumer
import jsons
import time
import numpy as np
# producer class
class MessageProducer:
     broker = ""
     topic = ""
     producer = None  
     def __init__(self, broker, topic):
          self.broker = broker
          self.topic = topic
          self.producer = KafkaProducer(bootstrap_servers=self.broker, value_serializer=lambda v: jsons.dumps(v).encode('utf-8'), acks='all', retries = 5)
   
     def send_msg(self, msg):
          print("Controller is sending message to edge nodes...")
          try:
              future = self.producer.send(self.topic, msg)
              self.producer.flush()
              future.get(timeout=60)
              print("Message done ...")
              return {'status_code':200, 'error':None}
          except Exception as ex:
              return ex
   
# procedure
broker = '165.194.35.81:9092'
topic0 = 'users_requests0'
topic1 = 'users_requests1'
topic2 = 'users_requests2'
topic3 = 'users_requests3'
topic4 = 'users_requests4'
topic5 = 'users_requests5'
request_producer0 = MessageProducer(broker, topic0)
while True:
# request_producer0.send_msg("testing...")
     request_producer0.send_msg("lalala")
     time.sleep(5)

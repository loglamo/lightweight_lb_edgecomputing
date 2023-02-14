from email import message 
from pykafka import KafkaClient
from kafka import KafkaProducer
import jsons
from datetime import datetime
import time
import numpy as np 
#generate sensor data for sensor node 1 from sensordata1 light  file
file_dir = './datasets/sensordata1.txt'
id_data = [1,2] #1: temp, 2: light
id_node = [1,2,3,4,5] #id of 5 sensor nodes: 1,2,3,4,5
id_data_now = id_data[1] #data is light data
id_node_now = id_node[0] #sensor node 1
def generate_data(file_dir, id_node_now, id_data_now):
    id_node = id_node_now
    id_data = id_data_now 
    input_file = open(file_dir, 'r')      #open file to read
    lines = input_file.readlines()        #read all lines in file
    lines.pop(0)                          #remove the first line of properties name
    sensorData = []
    for item in lines:
        line_i = item.split(',')          #read one by line with removing the comma 
        line_i.pop(0)                     #remove time
        line_i.pop(0)                     #remove mode id 
        line_i.pop(0)                     #remove fault type
        line_i.pop(0)                     #remove temp 
        line_i_array = np.array(line_i)   #convert list into array
        line_i_array = [float(item) for item in line_i_array]    #str into float 
        line_i_array = [id_node,id_data] + line_i_array 
        sensorData = sensorData + [line_i_array]
    return sensorData
class MessageProducer:
      broker = ""
      topic = ""
      producer = None

      def __init__(self, broker, topic):
          self.broker = broker
          self.topic = topic
          self.producer = KafkaProducer(bootstrap_servers=self.broker, value_serializer=lambda v: jsons.dumps(v).encode('utf-8'), acks='all', retries = 3)

      def send_msg(self,msg):
          print("sending message ...")
          try:
              future = self.producer.send(self.topic,msg)
              self.producer.flush()
              future.get(timeout=60)
              print("message done ...")
              return {'status_code':200, 'error':None}
          except Exception as ex:
              return ex
broker = '165.194.35.81:9092'
topic = 'sensordata1'
message_producer = MessageProducer(broker,topic)
#send messages to the topic 
sensor_data = generate_data(file_dir,id_node_now,id_data_now)
for item in range(len(sensor_data)):
    data_item = {}
    data_item['time'] = str(datetime.utcnow())   #add timestamp
    data_item['id'] = item
    data_item['idnode'] = sensorData[item][0]
    data_item['iddata'] = sensorData[item][1]
    data_item['value'] = sensorData[item][2]
    message = json.dumps(data_item) #make message in json format
    print('Message now is: \n')
    print(message)
    resp = message_producer.send_msg(message)
    print(resp)



#data = {'id':'test1', 'data':'lalalala from cluster2'}
#resp = message_producer.send_msg(data)
#print(resp
